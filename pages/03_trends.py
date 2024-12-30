import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np


st.set_page_config(page_title="Trends",
                   page_icon="📑")

# TODO: lazy load data. cache teh data


@st.cache_data
def load_df(filename: str, sheet: str) -> pd.DataFrame:
    """Load data from an excel file.

    Args:
        filename (str): name of the excel file to be read
        sheet (str): name of the sheet of the excel file

    Returns:
        pd.DataFrame: a pandas df is created. streamlit caches the data.
    """
    return pd.read_excel(filename, sheet_name=sheet)


def preprocess_data(df: pd.dataFrame) -> pd.DataFrame:

    # standardize column names snd types
    df.columns = df.columns.astype(str)
    # remove the columns containing "Unnamed" in their names
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    # there is a column named "a". drop it
    df.drop(["a"], inplace=True, axis=1)
    # standardize column names
    df.columns = (df.columns.str.strip()
                  .str.lower()
                  .str.replace(' ', '_'))

    # handle numeric columns
    numeric_columns = df.columns[2:]
    # replace ".." with Numpy's NaN
    df[numeric_columns] = df[numeric_columns].replace("..", np.nan).astype(float)

    # rename columns for clarity
    rename_dict = {
        "1990": "hdi_1990", "2000": "hdi_2000", "2010": "hdi_2010", "2015": "hdi_2015",
        "2019": "hdi_2019",
        "2020": "hdi_2020", "2021": "hdi_2021", "2022": "hdi_2022",
        "2015-2022": "change in hdi rank 2015-2022",
        "1990-2000": "avg hdi growth (%) 1990-2000",
        "2000-2010": "avg hdi growth (%) 2000-2010",
        "2010-2022": "avg hdi growth (%) 2010-2022",
        "1990-2022": "avg hdi growth (%) 1990-2022"
    }
    
    # rename columns
    df.rename(columns=rename_dict,inplace=True)
    
    return df


# # read the excel file's "HDI trends sheet".
# df_unclean = load_df(
#     "HDR23-24_Statistical_Annex_Tables_1-7.xlsx", "HDI trends")

# # make the columns type as str for processing.
# df_unclean.columns = df_unclean.columns.astype(str)

# # remove the columns containing "Unnamed" in their names
# df_unclean = df_unclean.loc[:, ~df_unclean.columns.str.contains("^Unnamed")]

# # there is a column named "a". drop it
# df_unclean.drop(["a"], inplace=True, axis=1)

# # standardize column names
# df_unclean.columns = df_unclean.columns.str.strip().str.lower().str.replace(' ', '_')

# # get the numeric columns
# numeric_columns = df_unclean.columns[2:]

# # replace ".." with Numpy's NaN
# df_unclean[numeric_columns] = df_unclean[numeric_columns].replace(
#     "..", np.nan).astype("float")

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
df_long = pd.melt(
    df_unclean,
    id_vars=["country"],
    value_vars=["hdi_1990", "hdi_2000", "hdi_2010", "hdi_2015",
                "hdi_2019", "hdi_2020", "hdi_2021", "hdi_2022"],
    var_name="year",
    value_name="hdi"
)

# clean your name column
df_long["year"] = df_long["year"].str.extract(r"(\d{4})").astype(int)

# get the top 10 countries for default option
top_5_countries = df_unclean.sort_values(
    "hdi_rank")["country"].head(5).tolist()

# streamlit app's title
st.title("HDI trends visualization")

# multi-select widget for countries
st.info("Default is top 5 countries 🗺️")
selected_countries = st.multiselect("Select countries to display:",
                                    options=df_long["country"].unique(),
                                    default=top_5_countries)

# filter data based on selected countries
filtered_df = df_long[df_long["country"].isin(selected_countries)]

# create the plotly line chart
fig = px.line(
    filtered_df,
    x="year",
    y="hdi",
    color="country",
    title="HDI Trends Over Time",
    labels={"hdi": "HDI", "year": "Year", "country": "Country"}
)

# update traces to make all lines dashed
fig.for_each_trace(lambda trace: trace.update(
    line=dict(dash="dash", width=1), opacity=0.5))

# add interactivity
fig.update_traces(mode="lines+markers")
fig.update_layout(legend_title="Countries",
                  width=2000,
                  height=700)

st.plotly_chart(fig, use_container_width=True)
