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


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame,pd.Index]:
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
    df [numeric_columns_to_convert] = df[numeric_columns_to_convert].apply(pd.to_numeric, errors="coerce")
    # drop the HDI rank column. it was redundant.
    if "HDI rank" in df.columns:
        df.drop("HDI rank", inplace=True, axis=1)
    # get rid rows with missing values
    df = df.dropna()
    # get the numeric columns only
    numeric_columns = df.select_dtypes(include="float64").columns
    # exclude the last column
    numeric_columns=numeric_columns[:-1]
    return df,numeric_columns


def plot_histogram(df:pd.DataFrame,selected_column_x,selected_column_y,histfunc="avg") ->None:
    fig = px.histogram(df, x=selected_column_x,
                       y=selected_column_y, template="seaborn", histfunc="avg")
    st.plotly_chart(fig)




if __name__ == "__main__":

    st.title("📌 Human Development Reports (HDR)")

    st.markdown(
        "<style>div.clock-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

    # read the file from streamlit app
    fl = st.file_uploader(":file_folder: Upload a file", type=(["xlsx"]))

    # create the df_hdi dataframe
    if fl is not None:
        file_name = fl.name
        # create the dataframe
        raw_data = load_data(file_name)
        st.write("Data Frame is created.")

    # create the pop_gnipc dataframe
    pop_gnipc_df = load_data(os.path.join(
        os.getenv("data_path"), "pop_gnipc.xlsx"))
    # multiply the poplulation column by one million.
    pop_gnipc_df["Population"] = pop_gnipc_df["Population"] * 1000000
    
    clean_data,numeric_columns=preprocess_data(raw_data)
    
    # create 2 columns
    col1,col2=st.columns(2)
    
    with col1:
        selected_column_x=st.selectbox(
            "Choose a column for x axis:",options=numeric_columns,key="x"
        )
        selected_column_y=st.selectbox(
            "Choose a column for y axis:",options=numeric_columns,key="y"
        )
        st.subheader(f"{selected_column_x} vs. {selected_column_y}")
        plot_histogram(clean_data,selected_column_x,selected_column_y)