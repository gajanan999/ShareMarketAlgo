from download.DownloadDataForOneMin import downloadData
import datetime
import os

tickers = ['GOOG','DB', 'AAPL', 'MSFT', 'CRM', 'TSLA']
interval = '1m'
downloadPath = os.path.join(os.path.dirname(__file__), "downloadedData")


print(downloadPath)

for ticker in tickers:
    # Get today's date
    today = datetime.date.today()
    end_date = today.strftime("%Y-%m-%d")
    # Subtract 7 days from today's date
    seven_days_ago = today - datetime.timedelta(days=7)
    start_date = seven_days_ago.strftime("%Y-%m-%d")
    downloadData(ticker, start_date, end_date, interval, downloadPath)