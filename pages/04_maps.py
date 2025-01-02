import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
from typing import Tuple

load_dotenv("config.env")

st.set_page_config(
    page_title="Map",
    page_icon="🌍️",
    layout="wide")


@st.cache_data
def load_data(filename: str, sheet: str) -> pd.DataFrame:
    """Load data from an excel file.

    Args:
        filename (str): name of the excel file to be read
        sheet (str): name of the sheet of the excel file

    Returns:
        pd.DataFrame: a pandas df is created. streamlit caches the data.
    """
    return pd.read_excel(filename, sheet_name=sheet)


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

# visualization functions


def choropleth_plot(df: pd.DataFrame) -> None:

    st.header("HDI Across Countries")
    fig = go.Figure(data=go.Choropleth(
        locations=merged_df["Country"],
        locationmode="country names",
        z=merged_df["HDI"],
        colorscale="Blues",
        colorbar_title="HDI"
    ))

    fig.update_layout(
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type="natural earth",
        )
    )
    st.plotly_chart(fig, use_container_width=True)


def bubblemap_plot(df: pd.DataFrame) -> None:
    
    st.header("Bubble map: Population size across countries")
    fig = px.scatter_geo(
        merged_df,
        locations="Country",
        locationmode="country names",
        size="Population",
        color="HDI",
        hover_name="Country",
        hover_data={"Population": False, "Formatted Population": True},
        projection="natural earth",
        size_max=50
    )

    st.plotly_chart(fig, use_container_width=True)


# main workflow
if __name__ == "__main__":
    # load data from the session state of streamlit.
    if "data" in st.session_state:
        raw_data_hdi = st.session_state["data"]["HDI"]
    else:
        st.warning("No data loaded! Please upload an excel file on the EDA page!")

    clean_data_hdi, _ = preprocess_data(raw_data_hdi)
    pop_gnipc_df = load_data(os.path.join(
        os.getenv("data_path"), "pop_gnipc.xlsx"), "Sheet1")
    # multiply the poplulation column by one million.
    pop_gnipc_df["Population"] *= 1_000_000
    # merge two dataframes
    merged_df = merge_dataframes(clean_data_hdi, pop_gnipc_df)

    # Format population with commas
    merged_df["Formatted Population"] = merged_df["Population"].apply(
        lambda x: f"{x:,.0f}")

    col1,col2=st.columns(2)
    
    with col1:
        choropleth_plot(merged_df)
    with col2:
        bubblemap_plot(merged_df)
