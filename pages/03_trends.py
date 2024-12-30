import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# read the excel file's "HDI trends sheet".
df_unclean = pd.read_excel(
    "HDR23-24_Statistical_Annex_Tables_1-7.xlsx", sheet_name="HDI trends")

# make the columns type as str for processing.
df_unclean.columns = df_unclean.columns.astype(str)

# now let's remove the columns containing "Unnamed" in their names
df_unclean = df_unclean.loc[:, ~df_unclean.columns.str.contains("^Unnamed")]

# there is a column named "a". drop it
df_unclean.drop(["a"], inplace=True, axis=1)

# standardize column names
df_unclean.columns = df_unclean.columns.str.strip().str.lower().str.replace(' ', '_')

# get the numeric columns
numeric_columns = df_unclean.columns[2:]

# replace ".." with Numpy's NaN
df_unclean[numeric_columns] = df_unclean[numeric_columns].replace(
    "..", np.nan).astype("float")

# rename columns for clarity
df_unclean.rename(columns={"1990": "hdi_1990", "2000": "hdi_2000", "2010": "hdi_2010", "2015": "hdi_2015",
                           "2019": "hdi_2019",
                           "2020": "hdi_2020", "2021": "hdi_2021", "2022": "hdi_2022",
                           "2015-2022": "change in hdi rank 2015-2022",
                           "1990-2000": "avg hdi growth (%) 1990-2000",
                           "2000-2010": "avg hdi growth (%) 2000-2010",
                           "2010-2022": "avg hdi growth (%) 2010-2022",
                           "1990-2022": "avg hdi growth (%) 1990-2022"}, inplace=True)


# now let's create a visual for trends
# reshape data from wide to long format
df_long=pd.melt(
    df_unclean,
    id_vars=["country"],
    value_vars=["hdi_1990", "hdi_2000", "hdi_2010", "hdi_2015", "hdi_2019", "hdi_2020", "hdi_2021", "hdi_2022"],
    var_name="year",
    value_name="hdi"
)

# clean your name column
df_long["year"]=df_long["year"].str.extract(r"(\d{4})").astype(int)

# create the plotly line chart
fig=px.line(
    df_long,
    x="year",
    y="hdi",
    color="country",
    title="HDI Trends Over Time",
    labels={"hdi":"HDI","year":"Year","country":"Country"}
)

# add interactivity
fig.update_traces(mode="lines+markers")
fig.update_layout(legend_title="Countries")

st.plotly_chart(fig)