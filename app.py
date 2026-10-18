import streamlit as st

st.set_page_config(page_title="Project Hub", page_icon="🗂️", layout="wide")

st.title("Project Hub")
st.write(
    "A collection of my personal projects, hosted on Databricks Apps. "
    "Pick a project from the sidebar to open it."
)

st.subheader("Projects")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("### Ludrin House Business Model")
        st.write(
            "Interactive financial model for a two-floor TCG card shop, "
            "PC room, and kitchen in NYC. Adjust the assumptions and watch "
            "revenue, costs, break-even, and payback update live."
        )
        st.page_link("pages/1_Ludrin_House_Model.py", label="Open the model", icon="📊")

with col2:
    with st.container(border=True):
        st.markdown("### More coming soon")
        st.write("New projects get added here as separate pages.")

st.caption("Built with Streamlit on Databricks Apps.")
