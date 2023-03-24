
import yfinance as yf
import os


def downloadData(ticker, startDate, endDate, interval, downloadPath):
    print('Start date : ', startDate)
    print('End date: ', endDate)

    # Download the historical data for the USD currency index
    data = yf.download(ticker, start=startDate, end=endDate, interval=interval)

    print(data.to_string())

    # Use the mplfinance library to plot the candlestick chart
    #mpf.plot(data,type='candle',title=ticker)

    output_path = os.path.join(downloadPath, ticker)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file_name = ticker+"_"+ startDate + "_"+ endDate + "_" + interval+"_data.csv"
    output_file = os.path.join(output_path, output_file_name)

    data.to_csv(output_file, index=False)