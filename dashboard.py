import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
import io
import warnings

# loading data and cache it.
@st.cache_data
def load_data(file_name):
    return pd.read_excel(file_name)
    
warnings.filterwarnings("ignore")

st.set_page_config(page_title="HDR",
                   page_icon="📊", layout="wide")

st.title("📌 Human Development Reports (HDR)")

st.markdown(
    "<style>div.cclock-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

# read the file from streamlit app
fl=st.file_uploader(":file_folder: Upload a file",type=(["xlsx"]))

if fl is not None:
    file_name=fl.name
    # create the dataframe
    df_hdi=load_data(file_name)
    st.write("Data Frame is created.")

# create 2 columns for the app
col1,col2=st.columns(2)


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

# create a piechart
with col2:
    top_10_countries=df_hdi_clean.head(10)
    selected_column=st.selectbox("Choose a column:",options=numeric_columns)
    fig=px.pie(top_10_countries,names="Country",values=selected_column,height=550,hover_data=selected_column,title=f"Top 10 countries vs. {selected_column}",hole=0.3)
    # modify to show the exact values on the pie chart
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig)

# let's creat two columns layout again
col1_row2,col2_row2=st.columns(2)

with col1_row2:
    selected_column=st.selectbox("Choose a column:",options=numeric_columns,key="global heatmap")
    if selected_column=="HDI_rank":
        pass
    # global HDI heatmap
    st.title(f"Global {selected_column} Heatmap")
    st.markdown(f"This heatmap visualizes the distribution of {selected_column} across countries.")

    # choropleth map
    fig=px.choropleth(df_hdi_clean,
                    locations="Country",
                    locationmode="country names",
                    color=selected_column,
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Purples,
                    title=f"{selected_column}")

    # customize layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="natural earth"
        )
    )

    st.plotly_chart(fig)
    
with col2_row2:
    selected_column_x=st.selectbox("Choose a column:",options=numeric_columns,key="col2_row2_x")
    selected_column_y=st.selectbox("Choose a column:",options=numeric_columns,key="col2_row2_y")
    
    st.title(f"Scatter plot of {selected_column_x} vs. {selected_column_y}")
    st.markdown(f"This scatter plot visualizes the relationship between {selected_column_x} and {selected_column_y}")
    
    fig=px.scatter(
        df_hdi_clean,
        x=selected_column_x,
        y=selected_column_y,
        size=selected_column_x,
        hover_data="HDI",
        color=selected_column_x
    )
    st.plotly_chart(fig)
    