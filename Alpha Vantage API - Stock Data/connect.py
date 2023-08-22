import pandas as pd
import requests
import time
from datetime import datetime, timedelta

ALPHA_VANTAGE_API_KEY = 'YG4V57YBV7BWB0IW'
SYMBOLS = ['AAPL', 'JNJ', 'XOM']
TIME_SERIES_FUNCTION = 'TIME_SERIES_DAILY'

end_date = datetime.now()
start_date = end_date - timedelta(days=180)  # Past 6 months
all_stocks_data = pd.DataFrame()

def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function={TIME_SERIES_FUNCTION}&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()
        
        if 'Time Series (Daily)' in data:
            return pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index', dtype=float)
        else:
            print(f"Error fetching data for {symbol}: {data.get('Note', 'Unknown Error')}")
            print(data) # Print the entire response
            return None
        
    except requests.RequestException as e:
        print(f"An error occurred while fetching data for {symbol}: {str(e)}")
        return None

for symbol in SYMBOLS:
    stock_data = fetch_stock_data(symbol)
    
    if stock_data is not None:
        stock_data = stock_data[(stock_data.index >= start_date.strftime("%Y-%m-%d")) & (stock_data.index <= end_date.strftime("%Y-%m-%d"))]
        stock_data['Symbol'] = symbol # Add a column to identify the symbol
        all_stocks_data = pd.concat([all_stocks_data, stock_data]) # Concatenate data
        stock_data.to_csv(f'{symbol}_6_months.csv')

all_stocks_data.index = pd.to_datetime(all_stocks_data.index)

price_columns = ['1. open', '2. high', '3. low', '4. close']  # Make sure these match the column names in your DataFrame
all_stocks_data[price_columns] = all_stocks_data[price_columns].astype(float)

time.sleep(15) # Add a 15-second delay between requests

print(all_stocks_data.head()) # Print the first few rows to check the data
