import pandas as pd
from typing import Tuple
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(
    page_title="Statistical Analysis",
    page_icon="💡"
)


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


def convert_df_to_csv(df: pd.DataFrame, file_name: str):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )

# descriptive statistics


def histogram_plot(df: pd.DataFrame) -> None:

    # Add a dropdown to select which column to plot
    column = st.selectbox(
        "Select a column to view summary stats:", options=df.columns[1:-1])

    nbins = st.select_slider(
        "Select number of bins of the histogram plot:", options=range(0, 51))

    st.subheader(f"Histogram of {column}")
    fig = px.histogram(
        df,
        x=column,
        nbins=nbins,
        labels={column: column},
        color_discrete_sequence=['skyblue']
    )
    st.plotly_chart(fig)


def box_plot(df: pd.DataFrame) -> None:

    # Add a dropdown to select which column to plot
    column = st.selectbox(
        "Select a column to view summary stats:", options=df.columns[1:-1], key="boxplot")

    # Plot a Box Plot
    st.subheader(f"Box Plot of {column}")

    fig = px.box(
        df,
        y=column,
        labels={column: column},
        color_discrete_sequence=['lightcoral']
    )

    # TODO: Update hover template to show only the value and remove fences. It does not work now
    fig.update_traces(
        hovertemplate="<br>Value: %{y}<extra></extra>"
    )

    st.plotly_chart(fig)


if __name__ == "__main__":
    # load data from the session state of streamlit.
    if "data" in st.session_state:
        raw_data = st.session_state["data"]["HDI"]
    else:
        st.warning("No data loaded! Please upload an Excel file on the EDA page.")

    clean_data, _ = preprocess_data(raw_data)

    st.title("Summary Statistics")

    summary_stats = clean_data.describe(
        percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
    st.write(summary_stats)
    # download it as csv
    convert_df_to_csv(summary_stats, "summary_stats.csv")

    column = st.selectbox(
        "Select a column to view summary stats:", options=clean_data.columns[1:-1], key="summary_stats")
    st.subheader(f"Summary statistics of {column} column")
    summary_stats = clean_data[column].describe()
    st.write(summary_stats)
    convert_df_to_csv(summary_stats, f"summary stats of {column} column.csv")

    # data distribution analysis
    st.title("Data Distribution Analysis")
    #  call histogram andd boxplot functions
    histogram_plot(clean_data)
    box_plot(clean_data)
