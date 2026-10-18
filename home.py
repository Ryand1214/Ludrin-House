import streamlit as st

st.title("Project Hub")
st.write(
    "A collection of my personal projects, hosted on Databricks Apps. "
    "Pick a project from the sidebar to open it."
)

st.subheader("Projects")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("### Ludrin House")
        st.write(
            "Business plan for a two-floor TCG card shop, play hall, PC room and kitchen in NYC. "
            "The financial model updates revenue, profit, break-even and equity payback live, "
            "and the floor plan shows how both floors are laid out."
        )
        st.page_link("pages/1_Ludrin_House_Model.py", label="Open the business model", icon="📊")
        st.page_link("pages/2_Ludrin_House_Floor_Plan.py", label="Open the floor plan", icon="🏢")

with col2:
    with st.container(border=True):
        st.markdown("### More coming soon")
        st.write("New projects get added here as separate pages.")

st.caption("Built with Streamlit on Databricks Apps.")
