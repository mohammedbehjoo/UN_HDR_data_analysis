import streamlit as st

st.set_page_config(
    page_title="Introduction to HDR",
    page_icon="🗺️"
)

# title and subtitle of the page
st.title("Human Development Report (HDR) Dashboard 📰")
st.subheader("Exploring Global Development Indicators and Trends")


st.subheader(":material/check_small: Did You Know?")
# facts
col1,col2,col3=st.columns(3)

with col1:
    st.write("🇳🇴 Norway has consistently ranked as the country with the highest HDI in recent years.")
with col2:
    st.write("6️⃣0️⃣ More than 60% of countries have seen an improvement in HDI since 1990.")
with col3:
    st.write("👵🏿 Life expectancy at birth ranges from over 80 years in developed countries to under 60 in developing regions.")

# an inriguing chart


# intro to HDR and its significance
st.markdown("# Introduction to HDR")

# what
st.markdown("## :material/double_arrow: What is HDR?")
st.write("The Human Development Report (HDR) is an annual Human Development Index report published\
    by the Human Development Report Office of the United Nations Development Programme (UNDP).")

# why
st.markdown("## :material/double_arrow: Why does it matter?")
st.write("The 2023/24 Human Development Report assesses the dangerous gridlock resulting\
    from uneven development progress, intensifying inequality, and escalating political polarization,\
        that we must urgently tackle. The report emphasizes how global interdependence is being reconfigured\
            and proposes a path forward where multilateralism plays a pivotal role.")
st.write("Why does pursuing the ambitions of the 2030 Agenda for Sustainable Development and the Paris Agreement feel like a half-hearted slog through quicksand?\
    Why in many places does restoring peace, even pauses or ceasefires as hopeful preludes to peace, feel so elusive? \
        Why are we immobilized on digital governance while artificial intelligence races ahead in a data goldrush?\
        In short, why are we so stuck? And how do we get unstuck without resorting myopically to violence or isolationism? These questions motivate the Human Development Report.")

# key indicators
st.markdown(
    "## :material/double_arrow: What are the key indicators in the dataset?")
st.markdown(
    "- HDI (Human Development Index)\n- Life Expectancy\n- Education\n- GNI per capita\n- etc.")


# features of teh dashboard
st.markdown("## :material/double_arrow: What to expect from this dashboard?")
st.markdown("- Interactive Visualizations\n -Comparisons across countries\n - Trends over Time\n - Correlation between indicators\n - Statistcal Analysis")


# instructions
# TODO: Guide users on how to navigate the app:

# Briefly describe the different pages (e.g., Data Exploration, Visual Analysis, Country Comparisons).
# Mention any specific tools or filters, like dropdown menus.

st.markdown("## ::material/double_aroow: How to navigate the app")




# dataset
st.header(":material/double_arrow: Where to download the dataset?")
st.markdown("You can download the dataset from [here](https://hdr.undp.org/content/human-development-report-2023-24). This is the United Nations\
    Development Programme (UNDP) website.")
# create 3 columns
_,col1,_=st.columns(3)
with col1:
    st.image("UNDP-Logo-Blue-Large-Transparent.png", caption="UNDP", width=75)

# tools
st.markdown("""
## :material/double_arrow: Tools and Technologies
This app was built using:""")

st.markdown("- **[Streamlit](https://streamlit.io/):** For building the interactive web application.\n![Streamlit](https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png)")
st.markdown("- **[Plotly](https://plotly.com/):** For creating dynamic and interactive visualizations.\n![Plotly](https://images.plot.ly/logo/new-branding/plotly-logomark.png) ")
st.markdown("- **[Matplotlib](https://matplotlib.org/):** For static data visualization.\n![Matplotlib](https://matplotlib.org/_static/images/logo2.svg)")
st.markdown("- **[Dash](https://dash.plotly.com/):** For exploring layout designs and enhancing interactivity.")

