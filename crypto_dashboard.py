import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def run():

    st.title(" Crypto Market Dashboard")

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data)

    st.dataframe(df[["name","current_price","market_cap"]])

    top10 = df.head(10)

    fig = px.bar(
        top10,
        x="name",
        y="market_cap",
        color="name",
        title="Top 10 Crypto by Market Cap"
    )

    st.plotly_chart(fig)
