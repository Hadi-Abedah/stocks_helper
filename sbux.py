import yfinance as yf
import pandas as pd


ticker = "SBUX"
data = yf.download(ticker, start="2024-08-08", end="2024-08-20")


# Calculate the daily percentage change
percentage_change = data['Close'].pct_change() * 100

# Display the first few rows of the data with the percentage change
pd.set_option('display.max_rows', None)

print(percentage_change)
print(data["Close"])