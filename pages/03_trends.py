import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np


st.set_page_config(page_title="Trends",
                   page_icon="📑")

# lazy load data. cache the data
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


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """clean and preprocess the hdi trends data.

    Args:
        df (pd.dataFrame): the input dataframe

    Returns:
        pd.DataFrame: the cleaned dataframe
    """

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
    df[numeric_columns] = df[numeric_columns].replace(
        "..", np.nan).astype(float)

    # rename columns for clarity
    rename_dict = {
        "hdi_rank": "rank based on hdi",
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
    df.rename(columns=rename_dict, inplace=True)

    return df


def transform_to_long_format(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the data to a long format for visualization.

    Args:
        df (pd.DataFrame): initial dataframe to be transformed into long format.

    Returns:
        pd.DataFrame: the output dataframe that is in long format.
    """

    long_df = pd.melt(
        df,
        id_vars=["country"],
        value_vars=[col for col in df.columns if col.startswith("hdi_")],
        var_name="year",
        value_name="hdi"
    )

    long_df["year"] = long_df["year"].str.extract(r"(\d{4})").astype(int)

    return long_df


def plot_hdi_trends(data: pd.DataFrame, countries: list) -> None:
    """Generate and display the hdi trends chart

    Args:
        data (pd.DataFrame): the initial data
        countries (list): list of countries to be shown
    """

    # filter data based on selected countries
    filtered_data = data[data["country"].isin(countries)]

    # create the plotly line chart
    fig = px.line(
        filtered_data,
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


# main workflow
if __name__ == "__main__":
    # load data from the session state of streamlit.
    if "data" in st.session_state:
        raw_data=st.session_state["data"]["HDI trends"]
    else:
        st.warning("No data loaded! Please upload an excel file on the EDA page!")
    clean_data = preprocess_data(raw_data)
    # st.write(clean_data)
    long_data = transform_to_long_format(clean_data)

    # get the top 5 countries for default option of the visualization
    default_countries = clean_data.sort_values(
        "rank based on hdi")["country"].head(5).tolist()

    # streamlit app's title
    st.title("HDI trends visualization")

    # multi-select widget for countries
    st.info("Default is top 5 countries 🗺️")

    selected_countries = st.multiselect(
        "Select countries to display:",
        options=long_data["country"].unique(),
        default=default_countries)

    # generate and plot the visual
    plot_hdi_trends(long_data, selected_countries)
