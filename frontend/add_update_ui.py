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

    # Convert date to string for API
    date_key = selected_date.strftime("%Y-%m-%d")

    # ---------------- FETCH EXPENSES ----------------
    try:
        with st.spinner("Fetching expenses..."):
            response = requests.get(
                f"{API_URL}/expenses/{date_key}",
                timeout=10
            )
    except requests.exceptions.RequestException:
        st.error("❌ Cannot connect to backend server.")
        return

    if response.status_code == 200:
        existing_expenses = response.json()
        if existing_expenses:
            st.success(f"Expenses loaded for {date_key}")
        else:
            st.info("No expenses recorded for this date")
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    st.markdown("---")
    st.subheader("Expense Details")

    # ---------------- FORM ----------------
    with st.form(key=f"expense_form_{date_key}"):

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

            with c1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    step=1.0,
                    value=float(amount),
                    key=f"amount_{i}_{date_key}",
                    label_visibility="collapsed"
                )

            with c2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}_{date_key}",
                    label_visibility="collapsed"
                )

            with c3:
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

        # ---------------- SAVE EXPENSES ----------------
        if submit_button:
            filtered_expenses = [
                e for e in expenses if e["amount"] > 0
            ]

            if not filtered_expenses:
                st.warning("No expenses to save")
                return

            try:
                post_response = requests.post(
                    f"{API_URL}/expenses/{date_key}",
                    json=filtered_expenses,
                    timeout=10
                )
            except requests.exceptions.RequestException:
                st.error("❌ Failed to save expenses (backend unreachable)")
                return

            if post_response.status_code == 200:
                st.success("✅ Expenses saved successfully")
            else:
                st.error("❌ Failed to save expenses")
