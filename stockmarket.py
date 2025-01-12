import streamlit as st
import pandas as pd
import yfinance as yf

st.title('Stock market app - JAN')
st.write('this is hopt of getting hike !!')

# import datetime
import datetime
col1, col2 = st.columns(2)

with col1:
    st.header("Start date")
    startdate = st.date_input('Please enter Starting Date', datetime.date(2019,1,1))

with col2:
    st.header("End date")
    enddate =  st.date_input('Please enter Ending Date', datetime.date(2024,12,31))


#ticker_symbol = 'AAPL'

ticker_symbol = st.text_input('Enter the Stock market ticker symbol', 'AAPL')

ticker_data =  yf.Ticker(ticker_symbol)
ticker_df = ticker_data.history(period = '1d', start = startdate, end = enddate)

st.header("Data")
st.dataframe(ticker_df)

col1, col2 = st.columns(2)
with col1:
    st.write('## Daily closing price')
    st.line_chart(ticker_df['Close'])
with col2:
    st.write("## Volume movement over time.")
    st.line_chart(ticker_df['Volume'])