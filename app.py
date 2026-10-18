import streamlit as st

st.set_page_config(page_title="Project Hub", page_icon="🗂️", layout="wide")

pg = st.navigation(
    {
        "": [st.Page("home.py", title="Home", icon="🏠", default=True)],
        "Ludrin House": [
            st.Page("pages/1_Ludrin_House_Model.py", title="Business Model", icon="📊"),
            st.Page("pages/2_Ludrin_House_Floor_Plan.py", title="Floor Plan", icon="🏢"),
        ],
    }
)
pg.run()
