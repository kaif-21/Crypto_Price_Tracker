import streamlit as st
import requests


def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = requests.get(url)
        data = response.json()
        return float(data["price"])
    except:
        return None


def run():
    st.header("Portfolio Tracker")

    coins = {
        "Bitcoin": "BTC",
        "Ethereum": "ETH",
        "Dogecoin": "DOGE"
    }

    coin_name = st.selectbox("Select Coin", list(coins.keys()))
    amount = st.number_input("Enter Amount", min_value=0.0)

    symbol = coins[coin_name]
    price = get_price(symbol)

    if price:
        total = price * amount

        col1, col2 = st.columns(2)
        col1.metric("Price", f"${price:.2f}")
        col2.metric("Total Value", f"${total:.2f}")

    else:
        st.error("API error. Try again.")
