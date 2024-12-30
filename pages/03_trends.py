import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np

# read the excel file's "HDI trends sheet".
df_unclean=pd.read_excel("HDR23-24_Statistical_Annex_Tables_1-7.xlsx",sheet_name="HDI trends")

# make the columns type as str for processing.
df_unclean.columns=df_unclean.columns.astype(str)

# now let's remove the columns containing "Unnamed" in their names
df_unclean=df_unclean.loc[:,~df_unclean.columns.str.contains("^Unnamed")]

# there is a column named "a". drop it
df_unclean.drop(["a"],inplace=True,axis=1)

