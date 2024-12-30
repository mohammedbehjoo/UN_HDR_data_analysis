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


def plot_histogram(df: pd.DataFrame, x_column, y_column, histfunc: str = "avg") -> None:
    fig = px.histogram(df, x=x_column,
                       y=y_column, template="seaborn", histfunc="avg")
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

        # create 2 columns
        col1, col2 = st.columns(2)

        with col1:
            x_column = st.selectbox(
                "Choose a column for x axis:", options=numeric_columns, key="x"
            )
            y_column = st.selectbox(
                "Choose a column for y axis:", options=numeric_columns, key="y"
            )
            st.subheader(f"{x_column} vs. {y_column}")
            plot_histogram(clean_data, x_column, y_column)