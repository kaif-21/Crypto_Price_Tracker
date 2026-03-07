import streamlit as st
import requests

def run():

    st.title("Crypto Portfolio Tracker")

    coin = st.selectbox(
        "Select Coin",
        ["bitcoin", "ethereum", "dogecoin"]
    )

    amount = st.number_input("Enter Amount", min_value=0.0)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"

    response = requests.get(url)
    data = response.json()

    if coin in data:

        price = data[coin]["usd"]

        value = amount * price

        st.metric("Current Price", price)
        st.metric("Portfolio Value", value)

    else:

        st.error("API data not found. Try again.")