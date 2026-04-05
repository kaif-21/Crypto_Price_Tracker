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

    st.title("Crypto Price Tracker")

    coin = st.selectbox(
        "Select Cryptocurrency",
        ["bitcoin", "ethereum", "dogecoin"]
    )

    # -------------------------------
    # CURRENT PRICE API
    # -------------------------------
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={"accept": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()

            if coin in data and "usd" in data[coin]:
                price = data[coin]["usd"]
                st.metric("Current Price (USD)", price)

                # -------------------------------
                # 7 DAY CHART API
                # -------------------------------
                chart_url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"

                params = {
                    "vs_currency": "usd",
                    "days": "7"
                }

                try:
                    chart_response = requests.get(
                        chart_url,
                        params=params,
                        timeout=10,
                        headers={"accept": "application/json"}
                    )

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
                                title=f"{coin.upper()} 7 Day Price Chart"
                            )

                            st.plotly_chart(fig, use_container_width=True)

                        else:
                            st.warning("Chart data not available right now.")

                    else:
                        st.warning(f"Chart API error: {chart_response.status_code}")

                except requests.exceptions.RequestException:
                    st.error("Network issue while loading chart data.")

                except ValueError:
                    st.error("Invalid response received from chart API.")

            else:
                st.error("Crypto data not found from API.")

        else:
            st.error(f"Price API error: {response.status_code}")

    except requests.exceptions.RequestException:
        st.error("Network issue while loading price data.")

    except ValueError:
        st.error("Invalid response received from price API.")

# -------------------------------
# PORTFOLIO DASHBOARD
# -------------------------------
elif choice == "Portfolio Dashboard":
    crypto_portfolio_dashboard.run()
