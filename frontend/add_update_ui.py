import streamlit as st
from datetime import datetime
import requests

API_URL = "https://expense-management-g8gz.onrender.com"

def add_update_tab():

    selected_date = st.date_input(
        "Enter Date",
        datetime(2024, 8, 1),
        label_visibility="collapsed"
    )

    # ✅ convert date to string ONCE
    date_str = selected_date.strftime("%Y-%m-%d")

    st.write("Using API:", API_URL)
    st.write("Selected date:", date_str)

    try:
        with st.spinner("Fetching expenses..."):
            response = requests.get(
                f"{API_URL}/expenses/{date_str}",
                timeout=10
            )
    except requests.exceptions.RequestException as e:
        st.error("❌ Cannot connect to backend API")
        st.stop()

    if response.status_code == 200:
        existing_expenses = response.json()
        if existing_expenses:
            st.success(f"Expenses loaded for {date_str}")
        else:
            st.info("No expenses recorded for this date")
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    st.markdown("---")
    st.subheader("Expense Details")

    with st.form(key=f"expense_form_{date_str}"):

        col1, col2, col3 = st.columns([1, 1, 2])
        col1.markdown("**Amount (₦)**")
        col2.markdown("**Category**")
        col3.markdown("**Notes**")

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

            c1, c2, c3 = st.columns([1, 1, 2])

            amount_input = c1.number_input(
                "Amount",
                min_value=0.0,
                step=1.0,
                value=amount,
                key=f"amount_{i}_{date_str}",
                label_visibility="collapsed"
            )

            category_input = c2.selectbox(
                "Category",
                categories,
                index=categories.index(category),
                key=f"category_{i}_{date_str}",
                label_visibility="collapsed"
            )

            notes_input = c3.text_input(
                "Notes",
                value=notes,
                key=f"notes_{i}_{date_str}",
                label_visibility="collapsed"
            )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submitted = st.form_submit_button("💾 Save Expenses")

        if submitted:
            filtered = [e for e in expenses if e["amount"] > 0]

            try:
                r = requests.post(
                    f"{API_URL}/expenses/{date_str}",
                    json=filtered,
                    timeout=10
                )
                if r.status_code == 200:
                    st.success("Expenses saved successfully")
                else:
                    st.error("Failed to save expenses")
            except requests.exceptions.RequestException:
                st.error("❌ Backend unreachable")
