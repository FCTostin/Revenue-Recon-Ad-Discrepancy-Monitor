import streamlit as st
from ui.uploader import render_uploader_page
from ui.dashboard import render_dashboard_page

# --- CONFIG ---
st.set_page_config(
    page_title="Revenue Recon | AdOps Tool",
    page_icon="💸",
    layout="wide"
)

# --- SIDEBAR NAV ---
st.sidebar.title("Revenue Recon 💸")
page = st.sidebar.radio("Navigation", ["Dashboard", "Upload Data"])

st.sidebar.info("System Status: Online \nDB Connection: SQLite")

# --- ROUTING ---
if page == "Dashboard":
    render_dashboard_page()
elif page == "Upload Data":
    render_uploader_page()

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("v1.0.0 | Enterprise Edition")
