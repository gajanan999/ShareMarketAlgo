import yfinance as yf
import pandas as pd
import ta
import numpy as np
# Visualize the data and trading signals
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score


def runStrategy():
    # Define the ticker symbol and timeframe
    ticker = 'USDINR=X' # This is the ticker symbol for the USD currency index
    start_date = '2023-02-01'
    end_date = '2023-03-20'

    # Download the historical data for the USD currency index
    data = yf.download(ticker, start=start_date, end=end_date, interval='5m')



    # Calculate the fast and slow moving averages
    data['very_fast_ma'] = data['Close'].rolling(window=5).mean()
    data['fast_ma'] = data['Close'].rolling(window=13).mean()
    data['slow_ma'] = data['Close'].rolling(window=26).mean()

    # Calculate RSI
    data['rsi_14'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()

    # Calculate MACD
    macd = ta.trend.MACD(data['Close'], window_slow=26, window_fast=12, window_sign=9)
    data['macd'] = macd.macd()
    data['signal_line'] = macd.macd_signal()

    # Generate the trading signals
    data['signal'] = 0.0
    data.loc[(data['fast_ma'] > data['slow_ma']) & (data['rsi_14'] < 28) & (data['macd'] > data['signal_line']), 'signal'] = -1.0
    data.loc[((data['very_fast_ma'] < data['fast_ma']) | (data['rsi_14'] > 68) | (data['macd'] < data['signal_line']) & ((data['signal_line'] - data['macd'])> 0.001000)), 'signal'] = 1.0



    # Implement a stop loss
    stop_loss_pct = 0.10
    data['stop_loss'] = data['Close'].shift(1) * (1 - stop_loss_pct)

    # Calculate the daily returns and strategy returns
    data['returns'] = data['Close'].pct_change()
    data['strategy_returns'] = np.where(data['signal'].shift(1) == -1, np.where(data['Close'] < data['stop_loss'], -stop_loss_pct, data['returns']), data['signal'].shift(1) * data['returns'])

    print(data.to_string())
    # Calculate the daily returns and strategy returns
    #data['returns'] = data['Close'].pct_change()
    #data['strategy_returns'] = data['signal'].shift(1) * data['returns']

    # Calculate the cumulative returns
    cumulative_returns = (1.0 + data['strategy_returns']).cumprod()

    # Plot the results
    cumulative_returns.plot(figsize=(10, 6), color='g')
    plt.ylabel('Cumulative Returns')
    plt.xlabel('Date')
    plt.show()