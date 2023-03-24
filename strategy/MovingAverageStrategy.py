import yfinance as yf
import pandas as pd
import ta
import numpy as np
# Visualize the data and trading signals
import matplotlib.pyplot as plt


def runStrategy():
    ticker = 'USDINR=X'  # This is the ticker symbol for the USD currency index
    start_date = '2023-02-01'
    end_date = '2023-03-20'

    print('Start date : ', start_date)
    print('End date: ', end_date)

    # Download the historical data for the USD currency index
    data = yf.download(ticker, start=start_date, end=end_date, interval='15m')

    # Calculate the fast and slow moving averages
    data['very_fast_ma_20'] = data['Close'].rolling(window=20).mean()
    data['fast_ma_50'] = data['Close'].rolling(window=500).mean()
    data['slow_ma_200'] = data['Close'].rolling(window=200).mean()
    # Calculate RSI
    data['rsi_14'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
    data['very_fast_ma_20/close'] = data['very_fast_ma_20']/data['Close']
    data['signal_1'] = 0.0
    data.loc[(data['very_fast_ma_20'] > data['slow_ma_200']) & (data['fast_ma_50'] > data['slow_ma_200']) & (
                data['very_fast_ma_20/close'] > 0.999300) & (data['very_fast_ma_20/close'] < 1.000600), 'signal_1'] = 1

    print(data.to_string())
