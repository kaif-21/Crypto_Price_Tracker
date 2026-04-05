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
@st.cache_data(ttl=60)
def get_crypto_price(coin):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin,
        "vs_currencies": "usd"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15,
        headers={"accept": "application/json"}
    )

    return response


@st.cache_data(ttl=120)
def get_chart_data(coin):
    chart_url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "7"
    }

    response = requests.get(
        chart_url,
        params=params,
        timeout=15,
        headers={"accept": "application/json"}
    )

    return response


# -------------------------------
# CRYPTO TRACKER
# -------------------------------
if choice == "Crypto Tracker":
    st.title("Crypto Price Tracker")
    st.write("Track live crypto prices and view the last 7 days price chart.")

    coin = st.selectbox(
        "Select Cryptocurrency",
        ["bitcoin", "ethereum", "dogecoin"]
    )

    try:
        response = get_crypto_price(coin)

        if response.status_code == 200:
            data = response.json()

            if coin in data and "usd" in data[coin]:
                price = data[coin]["usd"]
                st.metric("Current Price (USD)", f"${price:,}")

                st.subheader(f"{coin.upper()} - 7 Day Price Chart")

                try:
                    chart_response = get_chart_data(coin)

                    if chart_response.status_code == 200:
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
                            st.warning("Chart data is not available right now.")

                    elif chart_response.status_code == 429:
                        st.warning("Chart temporarily unavailable because API rate limit exceeded. Please try again later.")

                    else:
                        st.error(f"Chart API error: {chart_response.status_code}")

                except requests.exceptions.RequestException:
                    st.error("Network issue while loading chart data.")
                except ValueError:
                    st.error("Invalid response received from chart API.")

            else:
                st.error("Crypto price data not found.")

        elif response.status_code == 429:
            st.warning("CoinGecko API rate limit exceeded. Please try again later.")

        else:
            st.error(f"Price API error: {response.status_code}")

    except requests.exceptions.RequestException:
        st.error("Network issue while loading crypto price.")
    except ValueError:
        st.error("Invalid response received from price API.")

# -------------------------------
# PORTFOLIO DASHBOARD
# -------------------------------
elif choice == "Portfolio Dashboard":
    crypto_portfolio_dashboard.run()
