# Personal Expense Tracker

A modern personal finance dashboard built with Python, Streamlit, SQLite, Pandas, and Plotly.

## Overview

Personal Expense Tracker is a simple web application that helps users track income, expenses, and spending patterns through a clean dashboard interface.

The app allows users to add transactions, filter them, view financial summaries, analyze expenses by category, delete transactions, and export data to CSV.

## Features

- Add income and expense transactions
- Store transactions locally using SQLite
- View total income, total expenses, and current balance
- Filter transactions by type, category, and date range
- Delete transactions using a dropdown menu
- View recent transactions
- Display expense summaries
- Show expenses by category using a chart
- Export filtered transactions to CSV
- Modern light dashboard UI

## Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## Project Structure

ExpenseTracker/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml

## How to Run

1. Clone the repository:

git clone https://github.com/KhalilT13/personal-expense-tracker

2. Navigate into the project folder:

cd ExpenseTracker

3. Install dependencies:

pip install -r requirements.txt

4. Run the app:

streamlit run app.py

## Database

The project uses SQLite for local storage.

The database file is created automatically when the app runs.

The local SQLite database file is ignored by Git to avoid uploading personal financial data.

## Future Improvements

- Edit existing transactions
- Add monthly spending charts
- Add budget limits
- Add recurring transactions
- Add user authentication
- Add PostgreSQL support

## Author

Khalil Talhami