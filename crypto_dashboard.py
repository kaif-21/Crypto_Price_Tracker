import streamlit as st
import requests
import pandas as pd


def get_market_data():
    coins = {
        "Bitcoin": "BTCUSDT",
        "Ethereum": "ETHUSDT",
        "Dogecoin": "DOGEUSDT",
        "Solana": "SOLUSDT",
        "XRP": "XRPUSDT",
        "BNB": "BNBUSDT"
    }

    rows = []

    for name, symbol in coins.items():
        try:
            url = "https://data-api.binance.vision/api/v3/ticker/price"
            params = {"symbol": symbol}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "price" in data:
                rows.append({
                    "name": name,
                    "symbol": symbol,
                    "current_price": float(data["price"])
                })

        except Exception as e:
            print(f"ERROR loading {symbol}: {e}")

    return pd.DataFrame(rows)


def run():
    st.header(" Market Dashboard")

    df = get_market_data()

    if df.empty:
        st.error("Market data not loaded.")
    else:
        st.subheader("Live Crypto Prices")
        st.dataframe(df, use_container_width=True)

        selected_coin = st.selectbox("Select Coin", df["name"].tolist())
        selected_row = df[df["name"] == selected_coin].iloc[0]

        st.metric(
            label=f"{selected_row['name']} Price",
            value=f"${selected_row['current_price']:,.2f}"
        )
