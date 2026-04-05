import streamlit as st
import portfolio_tracker
import crypto_dashboard


def run():
    st.title("Crypto Portfolio Dashboard")

    menu = ["Portfolio Tracker", "Market Dashboard"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Portfolio Tracker":
        portfolio_tracker.run()

    elif choice == "Market Dashboard":
        crypto_dashboard.run()

