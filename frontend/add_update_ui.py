
import streamlit as st
from datetime import datetime
import requests


API_URL = "http://localhost:8000"

def add_update_tab():

    selected_date = st.date_input(
        "Enter Date",
        datetime(2024, 8, 1),
        label_visibility="collapsed"
    )

    # 🔑 date-based key (CRITICAL FIX)
    date_key = selected_date.strftime("%Y-%m-%d")

    with st.spinner("Fetching expenses..."):
        response = requests.get(f"{API_URL}/expenses/{selected_date}")

    if response.status_code == 200:
        existing_expenses = response.json()
        if existing_expenses:
            st.success(f"Expenses loaded for {selected_date}")
        else:
            st.info("No expenses recorded for this date")
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    st.markdown("---")
    st.subheader("Expense Details")

    # 🔑 form key depends on date
    with st.form(key=f"expense_form_{date_key}"):

        # Display column headers
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.markdown("**Amount (₦)**")
        with col2:
            st.markdown("**Category**")
        with col3:
            st.markdown("**Notes**")

        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}_{date_key}",
                    label_visibility="collapsed"
                )

            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}_{date_key}",
                    label_visibility="collapsed"
                )

            with col3:
                notes_input = st.text_input(
                    label="Notes",
                    value=notes,
                    key=f"notes_{i}_{date_key}",
                    placeholder="Optional description",
                    label_visibility="collapsed"
                )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        st.markdown("---")
        submit_button = st.form_submit_button("💾 Save Expenses")

        if submit_button:
            filtered_expenses = [
                expense for expense in expenses if expense["amount"] > 0
            ]

            requests.post(f"{API_URL}/expenses/{selected_date}" ,json = filtered_expenses)

            if response.status_code ==200:
                st.success("Expenses saved successfully")
            else:
                st.error("No expenses to save")
