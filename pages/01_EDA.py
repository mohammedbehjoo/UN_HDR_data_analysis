from typing import Tuple
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
import io
from dotenv import load_dotenv
import warnings

st.set_page_config(page_title="EDA",
                   page_icon="📊", layout="wide")

warnings.filterwarnings("ignore")

load_dotenv("config.env")

# loading data and cache it.


@st.cache_data
def load_data(file_name: str) -> pd.DataFrame:
    return pd.read_excel(file_name)


def merge_dataframes(df_1: pd.DataFrame, df_2: pd.DataFrame, on: str = "Country", how: str = "left") -> pd.DataFrame:
    df_merged = df_1.merge(df_2, on="Country", how="left")
    df_merged = df_merged.reset_index(drop=True)
    return df_merged


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Index]:
    # filter and remove the columns that their names contain "unnamed".
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    # rename columns for clarity
    rename_dict = {"Human Development Index (HDI) ": "HDI",
                   "HDI rank.1": "HDI_rank"}
    # rename the columns to have better namings
    df.rename(columns=rename_dict, inplace=True)
    # Convert specified columns to numeric values
    numeric_columns_to_convert = [
        "HDI",
        "Expected years of schooling",
        "Mean years of schooling",
        "Gross national income (GNI) per capita",
        "GNI per capita rank minus HDI rank",
        "HDI_rank"
    ]
    # cast the specified columns to the numeric values
    df[numeric_columns_to_convert] = df[numeric_columns_to_convert].apply(
        pd.to_numeric, errors="coerce")
    # drop the HDI rank column. it was redundant.
    if "HDI rank" in df.columns:
        df.drop("HDI rank", inplace=True, axis=1)
    # get rid rows with missing values
    df = df.dropna()
    # get the numeric columns only
    numeric_columns = df.select_dtypes(include="float64").columns
    # exclude the last column
    numeric_columns = numeric_columns[:-1]
    return df, numeric_columns


def histogram_plot(df: pd.DataFrame, x_column, y_column, histfunc: str = "avg") -> None:
    fig = px.histogram(df, x=x_column,
                       y=y_column, template="seaborn", histfunc="avg")
    st.plotly_chart(fig)


def pie_plot(df: pd.DataFrame, names, selected_column) -> None:
    fig = px.pie(
        df.head(10),
        names=names,
        values=selected_column,
        height=600,
        hover_data=selected_column,
        title=f"Top 10 countries vs. {selected_column}", hole=0.3
    )

    # modify to show the exact values on the pie chart
    fig.update_traces(textinfo="label+value")

    st.plotly_chart(fig)


def scatter_plot(df: pd.DataFrame, x_column, y_column) -> None:
    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        size=x_column,
        hover_data="HDI",
        color=x_column
    )
    st.plotly_chart(fig)


def parallel_coordinates_plot(df: pd.DataFrame, selected_column, color_column) -> None:
    if selected_column:
        fig = px.parallel_coordinates(
            df,
            dimensions=selected_column,
            color=color_column,
            labels={col: col.replace("_", "") for col in selected_column},
            color_continuous_scale=px.colors.sequential.Purples
        )

        # update the plot. add margins
        fig.update_layout(
            margin=dict(
                l=100,
                r=100,
                t=50,
                b=50
            )
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please select at least one dimension to create the plot.")


def treemap_plot(df:pd.DataFrame)->None:
    fig = px.treemap(
    df,
    path=["Country"],  # hierarchy (only Country here)
    values="Population",  # Box size
    color="GNIPC",  # color based on GNI per capita
    labels={"GNIPC": "GNI per capita (USD)"},
    title="GNI per capita treemap"
)
    st.plotly_chart(fig)
    

def correlation_heatmap_plot(df:pd.DataFrame)->None:
    # correlation matrix heatmap
    # calculate the correlation matrix
    # first we have to get the numeric columns
    numeric_df=df.select_dtypes(include=["float64"])
    
    # exclude the HDI_rank from the numeric columns
    numeric_df=numeric_df[numeric_df.columns[~numeric_df.columns.isin(["HDI_rank"])]]

    # calculate the correlation matrix of numeric_df
    correlation_matrix=numeric_df.corr()

    # melt the correlation matrix to long format
    correlation_melted=correlation_matrix.reset_index().melt(id_vars="index")
    correlation_melted.columns=["Variable 1","Variable 2","Correlation"]

    fig = px.imshow(
        correlation_matrix,
        labels={"color": "Correlation Coefficient"},
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )

    # Add interactivity to hover
    fig.update_traces(
        hovertemplate="Correlation between %{x} and %{y}: %{z:.2f}<extra></extra>"
    )

    # Add title and layout adjustments
    fig.update_layout(
        
        xaxis_title="Indicators",
        yaxis_title="Indicators",
        width=800,
        height=600,
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    st.title("📌 Human Development Reports (HDR)")

    # read the file from streamlit app
    uploaded_file = st.file_uploader(
        ":file_folder: Upload a file", type=(["xlsx"]))

    # create the df_hdi dataframe
    if uploaded_file:
        # load and preprocess raw data
        raw_data = load_data(uploaded_file.name)
        st.success("Data is loaded successfully.")
        clean_data, numeric_columns = preprocess_data(raw_data)
        # load population and GNI data
        pop_gnipc_df = load_data(os.path.join(
            os.getenv("data_path"), "pop_gnipc.xlsx"))
        # multiply the poplulation column by one million.
        pop_gnipc_df["Population"] *= 1_000_000

        # merge two dataframes
        merged_df=merge_dataframes(clean_data,pop_gnipc_df)
        
        # create 2 columns
        col1, col2 = st.columns(2)

        with col1:
            x_column = st.selectbox(
                "Choose a column for x axis:", options=numeric_columns, key="x"
            )
            y_column = st.selectbox(
                "Choose a column for y axis:", options=numeric_columns, key="y"
            )
            st.title("Histogram Plot")
            st.subheader(f"{x_column} vs. {y_column}")
            histogram_plot(clean_data, x_column, y_column)

            st.title(f"Scatter plot of {x_column} vs. {y_column}")
            st.markdown(
                f"This scatter plot visualizes the relationship between {x_column} and {y_column}")
            scatter_plot(clean_data, x_column, y_column)

        with col2:
            st.title("Pie Chart")
            selected_column = st.selectbox(
                "Choose a column:", options=numeric_columns)
            pie_plot(clean_data, "Country", selected_column)
            
            st.title("Correlation matrix heatmap")
            correlation_heatmap_plot(clean_data)

    st.title("Parallel coordinates plot")
    st.markdown(
        "Analyze multiple dimensions simultaneously using a parallel coordinates plot.")

    # select columns for the plot
    selected_column = st.multiselect(
        "Select dimensions to include in the plot:",
        options=clean_data.columns[1:-1],
        default=["HDI", "Life expectancy at birth",
                 "Expected years of schooling"]
    )

    # dropdown menu for color scale customization
    color_column = st.selectbox(
        "Select a column for the color scale:",
        options=selected_column,
        index=0  # Default to the first dimension
    )

    parallel_coordinates_plot(clean_data, selected_column, color_column)

        # create a treemap
    st.title("Tree map of GNI per capita")
    st.markdown("This treemap represents the proportional income levels of countries, with box sizes indicating populationand colors representing GNI per capita")

    treemap_plot(merged_df)
