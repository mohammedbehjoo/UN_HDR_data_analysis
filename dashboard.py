import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
    # write the file's name to the app to make sure it is uploaded.
    st.write(filename)
    # create the dataframe
    df=pd.read_excel(filename)
    st.write("Data Frame is read.")

