import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import altair as alt
import streamlit as st

@st.cache

def getData(tic ,days):
    df = pd.DataFrame()
    for company in tic.keys():
        tkr = yf.Ticker(tic[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime("%d %B %Y")
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = "Company"
        df = pd.concat([df , hist], axis="rows")
    return df


tickers = {
    'apple' : 'AAPL',
    'Microsoft' : 'MSFT',
    'META' : 'META',
    'Netflix' : 'NFLX',
    'Google': 'GOOGL',
    'Amazon': 'AMZN'
}


st.title('米国株価可視化アプリ')
st.sidebar.write("""
# GAFA株価
こちらは株価可視化ツールです。以下のオプションから表示日数を選択できます。
""")
st.sidebar.write("""
### 表示日数選択
""")
days = st.sidebar.slider('日数', 1,50,20)

st.sidebar.write("""
### 株価の範囲指定
""")

ymin, ymax = st.sidebar.slider('範囲を指定してください', 0.0, 3500.0,(0.0,3500.0))

st.write(f"""
### 過去 **{days}日間** のGAFAの株価
""")
df = getData(tickers, days)

companies = st.multiselect(
    '会社を選択してください。',
    list(df.index),['Google','Amazon','apple','META']
)
if not companies:
    st.error('少なくとも一社選択してください。')
else:
    data = df.loc[companies]
    data.sort_index()
    st.write(data)
    data = data.T.reset_index()
    data = pd.melt(data, id_vars=['Date']).rename(
        columns={'value': 'Stock Price (USD)'}
    )

    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Stock Price (USD):Q", stack=None, scale=alt.Scale(domain=[ymin,ymax])),
            color='Company:N'
        )
    )
    st.altair_chart(chart, use_container_width=True)

