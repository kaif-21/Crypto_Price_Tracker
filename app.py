import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import crypto_portfolio_dashboard

# -------------------------------
# PAGE SETTINGS
# -------------------------------
st.set_page_config(
    page_title="Crypto Price Tracker",
    page_icon="📈",
    layout="wide"
)

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Navigation")
menu = ["Crypto Tracker", "Portfolio Dashboard"]
choice = st.sidebar.selectbox("Go to", menu)

# -------------------------------
# CACHE FUNCTIONS
# -------------------------------

# ✅ Get ONLY price (NOT response object)
@st.cache_data(ttl=60)
def get_crypto_price(coin):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"

        params = {
            "ids": coin,
            "vs_currencies": "usd"
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if coin in data:
                return data[coin]["usd"]

        return None

    except Exception as e:
        print("ERROR:", e)
        return None


# ✅ Chart API (returns response)
@st.cache_data(ttl=120)
def get_chart_data(coin):
    try:
        chart_url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

        params = {
            "vs_currency": "usd",
            "days": "7"
        }

        response = requests.get(chart_url, params=params, timeout=15)

        return response

    except Exception as e:
        print("Chart Error:", e)
        return None


# -------------------------------
# CRYPTO TRACKER PAGE
# -------------------------------
if choice == "Crypto Tracker":

    st.title("Crypto Price Tracker")
    st.write("Track live crypto prices and view the last 7 days price chart.")

    coin = st.selectbox(
        "Select Cryptocurrency",
        ["bitcoin", "ethereum", "dogecoin"]
    )

    # ---------------- PRICE ----------------
    price = get_crypto_price(coin)

    if price is not None:

        st.metric("Current Price (USD)", f"${price:,.2f}")

        st.subheader(f"{coin.upper()} - 7 Day Price Chart")

        # ---------------- CHART ----------------
        chart_response = get_chart_data(coin)

        if chart_response and chart_response.status_code == 200:

            chart_data = chart_response.json()

            if "prices" in chart_data and chart_data["prices"]:

                prices = chart_data["prices"]

                df = pd.DataFrame(prices, columns=["timestamp", "price"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

                fig = px.line(
                    df,
                    x="timestamp",
                    y="price",
                    title=f"{coin.upper()} Price Chart (Last 7 Days)"
                )

                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price (USD)"
                )

                st.plotly_chart(fig, use_container_width=True)

            else:
                st.warning("Chart data not available.")

        elif chart_response and chart_response.status_code == 429:
            st.warning("API rate limit exceeded. Try again later.")

        else:
            st.error("Failed to load chart data.")

    else:
        st.error("Failed to fetch crypto price.")


# -------------------------------
# PORTFOLIO DASHBOARD PAGE
# -------------------------------
elif choice == "Portfolio Dashboard":
    crypto_portfolio_dashboard.run()
