from typing import Tuple
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
import warnings

st.set_page_config(page_title="EDA",
                   page_icon="📊",
                   layout="wide")

warnings.filterwarnings("ignore")
load_dotenv("config.env")


@st.cache_data
def load_data(file: str, sheet_name: str | None = None) -> dict[str, pd.DataFrame] | pd.DataFrame:
    """
    Load data from an Excel file into a DataFrame or a dictionary of DataFrames, and cache it.

    Args:
        file (str): The path or file-like object of the Excel file.
        sheet_name (str | None): The name of the sheet to load. If None, all sheets are loaded.

    Returns:
        dict[str, pd.DataFrame] | pd.DataFrame:
        - A dictionary of DataFrames if sheet_name is None.
        - A single DataFrame if a specific sheet_name is provided.
    """
    return pd.read_excel(file, sheet_name=sheet_name)



def merge_dataframes(df_1: pd.DataFrame, df_2: pd.DataFrame, on: str = "Country", how: str = "left") -> pd.DataFrame:
    """Merge two dataframes on a specified column.

    Args:
        df_1 (pd.DataFrame): the first dataframe
        df_2 (pd.DataFrame): the second dataframe
        on (str, optional): _description_. Defaults to "Country".
        how (str, optional): _description_. Defaults to "left".

    Returns:
        pd.DataFrame: the output dataframe that is merged.
    """
    return df_1.merge(df_2, on=on, how=how).reset_index(drop=True)


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Index]:
    """Preprocess the dataframe by renaming columns, converting data types, and handling missing values.

    Args:
        df (pd.DataFrame): the raw dataframe

    Returns:
        Tuple[pd.DataFrame, pd.Index]: return a dataframe and pandas index
    """

    # filter and remove the columns that their names contain "unnamed".
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    # rename columns for clarity
    rename_dict = {"Human Development Index (HDI) ": "HDI",
                   "HDI rank.1": "HDI_rank"}
    # rename the columns to have better namings
    df.rename(columns=rename_dict, inplace=True)
    # Convert specified columns to numeric values
    numeric_columns = [
        "HDI",
        "Expected years of schooling",
        "Mean years of schooling",
        "Gross national income (GNI) per capita",
        "GNI per capita rank minus HDI rank",
        "HDI_rank"
    ]
    # cast the specified columns to the numeric values
    df[numeric_columns] = df[numeric_columns].apply(
        pd.to_numeric, errors="coerce")

    # drop the HDI rank column. it was redundant.
    if "HDI rank" in df.columns:
        df.drop("HDI rank", inplace=True, axis=1)

    # get rid rows with missing values
    df = df.dropna()
    # get the numeric columns only
    numeric_columns = df.select_dtypes(include="float64").columns[:-1]
    return df, numeric_columns


# visualization functions
def histogram_plot(df: pd.DataFrame, numeric_columns: pd.Index, histfunc: str = "avg") -> None:
    """Render a histogram plot based on user-selected columns.

    Args:
        df (pd.DataFrame): _description_
        histfunc (str, optional): _description_. Defaults to "avg".
    """

    st.title("Histogram Plot")

    x_column = st.selectbox(
        "Choose a column for x axis:", options=numeric_columns, key="x_histogram"
    )

    y_column = st.selectbox(
        "Choose a column for y axis:", options=numeric_columns, key="y_histogram"
    )

    st.subheader(f"{x_column} vs. {y_column}")

    fig = px.histogram(df, x=x_column,
                       y=y_column, template="seaborn", histfunc=histfunc)
    st.plotly_chart(fig)


def pie_plot(df: pd.DataFrame, numeric_columns: pd.Index) -> None:
    """Render a pie chart based on user-selected columns.

    Args:
        df (pd.DataFrame): _description_
    """
    st.title("Pie Chart")
    selected_column = st.selectbox("Choose a column:", options=numeric_columns)

    fig = px.pie(
        df.head(10),
        names="Country",
        values=selected_column,
        height=600,
        hover_data=selected_column,
        title=f"Top 10 countries vs. {selected_column}", hole=0.3
    )

    # modify to show the exact values on the pie chart
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig)


def scatter_plot(df: pd.DataFrame, numeric_columns: pd.Index) -> None:
    """Render a scatter plot to visualize relationships between two columns."""
    x_column = st.selectbox(
        "Choose a column for x axis:", options=numeric_columns, key="x_scatter"
    )

    y_column = st.selectbox(
        "Choose a column for y axis:", options=numeric_columns, key="y_scatter"
    )

    st.title(f"Scatter plot of {x_column} vs. {y_column}")
    st.markdown(
        f"This scatter plot visualizes the relationship between {x_column} and {y_column}")

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        size=x_column,
        hover_data="HDI",
        color=x_column
    )
    st.plotly_chart(fig)


def parallel_coordinates_plot(df: pd.DataFrame) -> None:
    """Render a parallel coordinates plot to analyze multiple dimensions."""

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


def treemap_plot(df: pd.DataFrame) -> None:

    st.title("Tree map of GNI per capita")
    st.markdown("This treemap represents the proportional income levels of countries, with box sizes indicating populationand colors representing GNI per capita")

    fig = px.treemap(
        df,
        path=["Country"],  # hierarchy (only Country here)
        values="Population",  # Box size
        color="GNIPC",  # color based on GNI per capita
        labels={"GNIPC": "GNI per capita (USD)"},
        title="GNI per capita treemap"
    )
    st.plotly_chart(fig)


def correlation_heatmap_plot(df: pd.DataFrame) -> None:

    st.title("Correlation matrix heatmap")

    # correlation matrix heatmap
    # calculate the correlation matrix
    # first we have to get the numeric columns
    numeric_df = df.select_dtypes(include=["float64"])

    # exclude the HDI_rank from the numeric columns
    numeric_df = numeric_df[numeric_df.columns[~numeric_df.columns.isin([
                                                                        "HDI_rank"])]]

    # calculate the correlation matrix of numeric_df
    correlation_matrix = numeric_df.corr()

    # melt the correlation matrix to long format
    correlation_melted = correlation_matrix.reset_index().melt(id_vars="index")
    correlation_melted.columns = ["Variable 1", "Variable 2", "Correlation"]

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


def bar_chart_plot(df: pd.DataFrame) -> None:

    st.title("Bar chart of HDI rankings")
    st.markdown("Explore top or bottom 10 countries based on HDI rank")
    toggle = st.radio("View:", ["Top 10", "Bottom 10"], horizontal=True)

    if toggle == "Top 10":
        filtered_df = df.nsmallest(10, "HDI_rank")
        title = "Top 10 countries by HDI rank"
    else:
        filtered_df = df.nlargest(10, "HDI_rank")
        title = "Bottom 10 countries by HDI rank"

    # create bar chart
    fig = px.bar(filtered_df,
                 x="Country",
                 y="HDI",
                 text="HDI_rank",
                 title=title,
                 labels={"HDI": "Human Development Index",
                         "Country": "Country"},
                 color="HDI",
                 color_continuous_scale="Viridis")

    fig.update_traces(
        texttemplate="Rank: %{text}", textposition="outside"
    )

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="HDI",
        coloraxis_showscale=False,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig)


if __name__ == "__main__":
    st.title("📌 Human Development Reports (HDR)")

    # read the file from streamlit app
    uploaded_file = st.file_uploader(
        ":file_folder: Upload a file", type=(["xlsx"]))

    # create the df_hdi dataframe
    if uploaded_file:
        # Store the uploaded file in session state
        st.session_state["uploaded_file"] = uploaded_file

        # Load and cache the data
    if "data" not in st.session_state:
        st.session_state["data"] = load_data(uploaded_file)

    # Display sheet names
    sheet_names = list(st.session_state["data"].keys())
    st.write(f"Available Sheets: {sheet_names}")

    # Option to preview a sheet
    selected_sheet = st.selectbox(
        "Select a sheet for raw data", options=sheet_names)

    # load and preprocess raw data
    raw_data = load_data(uploaded_file.name, selected_sheet)
    st.success("Data is loaded successfully.")
    clean_data, numeric_columns = preprocess_data(raw_data)
    
    # load population and GNI data
    pop_gnipc_df = load_data(os.path.join(
        os.getenv("data_path"), "pop_gnipc.xlsx"),sheet_name="Sheet1")
    # multiply the poplulation column by one million.
    pop_gnipc_df["Population"] *= 1_000_000
    
    # merge two dataframes
    merged_df = merge_dataframes(clean_data, pop_gnipc_df)

    # create 2 columns
    col1, col2 = st.columns(2)
    with col1:
        histogram_plot(clean_data, numeric_columns)
        scatter_plot(clean_data, numeric_columns)

    with col2:
        pie_plot(clean_data, numeric_columns)
        correlation_heatmap_plot(clean_data)

    # parallel coordinates
    parallel_coordinates_plot(clean_data)
    # create a treemap
    treemap_plot(merged_df)
    # bar chart
    bar_chart_plot(clean_data)
