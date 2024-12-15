import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title="HDR",
                   page_icon="📊", layout="wide")

st.title("📌 Human Development Reports (HDR)")

st.markdown(
    "<style>div.cclock-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

# read the file from streamlit app
fl=st.file_uploader(":file_folder: Upload a file",type=(["xlsx"]))

if fl is not None:
    filename=fl.name
    # create the dataframe
    df_hdi=pd.read_excel(filename)
    st.write("Data Frame is created.")

# create 2 columns for the app
col1,col2=st.columns((2))


# let's filter and remove the columns that their names contain "unnamed".
df_hdi = df_hdi.loc[:, ~df_hdi.columns.str.contains("^Unnamed")]

# let's rename the columns to have better namings
df_hdi.rename(columns={"Human Development Index (HDI) ": "HDI",
              "HDI rank.1": "HDI_rank"}, inplace=True)

# cast the specified columns to the numeric values
df_hdi[["HDI", "Expected years of schooling", "Mean years of schooling", "Gross national income (GNI) per capita", "GNI per capita rank minus HDI rank", "HDI_rank"]] = df_hdi[[
    "HDI", "Expected years of schooling", "Mean years of schooling", "Gross national income (GNI) per capita", "GNI per capita rank minus HDI rank", "HDI_rank"]].apply(pd.to_numeric, errors="coerce")

# drop the HDI rank column. it was redundant.
df_hdi.drop("HDI rank", inplace=True, axis=1)

# get rid rows with missing values
df_hdi_clean = df_hdi.dropna()

# get the numeric columns only
numeric_columns=df_hdi_clean.select_dtypes(include="float64").columns

# select a column for y value of the following chart

# let's show the histogram relationship between columns
with col1:
    selected_column_x=st.selectbox("Choose a column for x axis:",options=numeric_columns,key="x")
    selected_column_y=st.selectbox("Choose a column for y axis:",options=numeric_columns,key="y")
    st.subheader(f"{selected_column_x} vs. {selected_column_y}")
    fig=px.histogram(df_hdi_clean,x=selected_column_x,y=selected_column_y,template="seaborn",histfunc="avg")
    st.plotly_chart(fig,use_container_width=True)
