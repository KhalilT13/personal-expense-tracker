import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import create_table, add_transaction, get_all_transactions, delete_transaction


create_table()

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1, h2, h3 {
        color: #111827;
        font-weight: 700;
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    }

    [data-testid="stMetricLabel"] {
        color: #6B7280;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #111827;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }

    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
    }

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #111827;
        background-color: #111827;
        color: white;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }

    .stButton > button:hover {
        background-color: #374151;
        color: white;
        border: 1px solid #374151;
    }

    .stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #111827;
        background-color: #FFFFFF;
        color: #111827;
        font-weight: 600;
    }

    .stDownloadButton > button:hover {
        background-color: #F3F4F6;
        color: #111827;
        border: 1px solid #111827;
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 💰 Personal Expense Tracker
A clean dashboard for tracking income, expenses, and spending patterns.
""")
st.divider()


transactions = get_all_transactions()

columns = ["ID", "Type", "Category", "Amount", "Date", "Note"]
df = pd.DataFrame(transactions, columns=columns)


with st.sidebar.expander("➕ Add New Transaction", expanded=False):
    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    category = st.selectbox(
        "Category",
        ["Salary", "Food", "Rent", "Transportation", "Car", "University", "Entertainment", "Health", "Other"]
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=10.0
    )

    transaction_date = st.date_input(
        "Date",
        value=date.today()
    )

    note = st.text_area("Note")

    if st.button("Add Transaction"):
        if amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            add_transaction(transaction_type, category, amount, str(transaction_date), note)
            st.success("Transaction added successfully!")
            st.rerun()


if not df.empty:
    with st.sidebar.expander("🗑️ Delete Transaction", expanded=False):
        transaction_options = {}

        for _, row in df.iterrows():
            label = f'{row["ID"]} | {row["Type"]} | {row["Category"]} | {row["Amount"]} ₪ | {row["Date"]}'
            transaction_options[label] = row["ID"]

        selected_transaction = st.selectbox(
            "Choose transaction to delete",
            list(transaction_options.keys())
        )

        if st.button("Delete Selected Transaction"):
            delete_transaction(transaction_options[selected_transaction])
            st.success("Transaction deleted successfully!")
            st.rerun()


if df.empty:
    st.info("No transactions yet. Add your first transaction from the sidebar.")

else:
    df["Date"] = pd.to_datetime(df["Date"])

    with st.sidebar.expander("🔎 Filter Transactions", expanded=False):
        type_filter = st.selectbox(
            "Transaction Type",
            ["All", "Income", "Expense"]
        )

        category_filter = st.selectbox(
            "Category",
            ["All"] + sorted(df["Category"].unique().tolist())
        )

        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()

        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    filtered_df = df.copy()

    if type_filter != "All":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]

    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category_filter]

    if len(date_range) == 2:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])

        filtered_df = filtered_df[
            (filtered_df["Date"] >= start_date) &
            (filtered_df["Date"] <= end_date)
        ]

    total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
    total_expenses = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
    balance = total_income - total_expenses

    display_df = filtered_df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Total Income", f"{total_income:.2f} ₪")
    col2.metric("🧾 Total Expenses", f"{total_expenses:.2f} ₪")
    col3.metric("💰 Balance", f"{balance:.2f} ₪")

    st.divider()

    dashboard_tab, transactions_tab, charts_tab = st.tabs(
        ["📊 Dashboard", "📋 Transactions", "📈 Charts"]
    )

    with dashboard_tab:
        st.subheader("Summary")

        total_transactions = len(filtered_df)
        expense_df = filtered_df[filtered_df["Type"] == "Expense"]

        if not expense_df.empty:
            top_spending_category = expense_df.groupby("Category")["Amount"].sum().idxmax()
            average_expense = expense_df["Amount"].mean()
        else:
            top_spending_category = "No expenses"
            average_expense = 0

        s1, s2, s3 = st.columns(3)

        s1.metric("Number of Transactions", total_transactions)
        s2.metric("Top Spending Category", top_spending_category)
        s3.metric("Average Expense", f"{average_expense:.2f} ₪")

        st.markdown("### Recent Transactions")

        if display_df.empty:
            st.warning("No transactions match the selected filters.")
        else:
            st.dataframe(
                display_df.head(5),
                use_container_width=True,
                hide_index=True
            )

    with transactions_tab:
        st.subheader("Transactions")

        if display_df.empty:
            st.warning("No transactions match the selected filters.")
        else:
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            csv = display_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Transactions as CSV",
                data=csv,
                file_name="transactions.csv",
                mime="text/csv"
            )

    with charts_tab:
        st.subheader("Expenses by Category")

        expense_df = filtered_df[filtered_df["Type"] == "Expense"]

        if expense_df.empty:
            st.warning("No expense data available for the selected filters.")
        else:
            category_summary = expense_df.groupby("Category", as_index=False)["Amount"].sum()

            fig = px.bar(
                category_summary,
                x="Category",
                y="Amount",
                title="Expenses by Category",
                text="Amount"
            )

            fig.update_traces(
                texttemplate="%{text:.2f}",
                textposition="outside"
            )

            fig.update_layout(
                xaxis_tickangle=0,
                font=dict(color="black"),
                title_font=dict(color="black"),
                xaxis=dict(
                    tickfont=dict(color="black"),
                    title_font=dict(color="black")
                ),
                yaxis=dict(
                    tickfont=dict(color="black"),
                    title_font=dict(color="black")
                )
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown(
        "Built with **Python**, **Streamlit**, **SQLite**, **Pandas**, and **Plotly**."
    )