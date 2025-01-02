import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Statistical Analysis",
    page_icon="💡"
)

def foo():
    pass


if __name__ =="__main__":
    # load data from the session state of streamlit.
    if "data" in st.session_state:
        raw_data = st.session_state["data"]["HDI"]
        st.dataframe(raw_data)
    else:
        st.warning("No data loaded! Please upload an Excel file on the EDA page.")
    
