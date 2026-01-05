
import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab


API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Expense Management System",
    page_icon="💼",
    layout="centered"
)

st.title("💼 Expense Management System")
st.caption("Manage, update, and analyze your daily expenses with ease")

tab1 , tab2 = st.tabs(["➕ Add / Update Expenses", "📊 Analytics"])

with tab1:
    add_update_tab()
with tab2:
    analytics_tab()


