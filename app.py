import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import crypto_portfolio_dashboard

st.sidebar.title("Navigation")

menu = ["Crypto Tracker", "Portfolio Dashboard"]
choice = st.sidebar.selectbox("Go to", menu)

# -------------------------------
# CRYPTO PRICE TRACKER
# -------------------------------
if choice == "Crypto Tracker":

    st.title(" Crypto Price Tracker")

    coin = st.selectbox(
        "Select Cryptocurrency",
        ["bitcoin", "ethereum", "dogecoin"]
    )

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"

    response = requests.get(url)
    data = response.json()

    if coin in data:

        price = data[coin]["usd"]

        st.metric("Current Price (USD)", price)

        # 7day chart
        chart_url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

        params = {
            "vs_currency": "usd",
            "days": "7"
        }

        chart_response = requests.get(chart_url, params=params)
        chart_data = chart_response.json()

        # SAFE CHECK (fix for your error)
        if "prices" not in chart_data:
            st.error("Chart data not available from API")
            st.write(chart_data)

        else:
            prices = chart_data["prices"]

            df = pd.DataFrame(prices, columns=["timestamp", "price"])

            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            fig = px.line(
                df,
                x="timestamp",
                y="price",
                title=f"{coin.upper()} 7 Day Price Chart"
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Crypto data not found from API")

# -------------------------------
# PORTFOLIO DASHBOARD
# -------------------------------
if choice == "Portfolio Dashboard":
    crypto_portfolio_dashboard.run()