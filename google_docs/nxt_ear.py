import yfinance as yf
from datetime import datetime
import pytz

def get_next_earnings_date(ticker):

    stock = yf.Ticker(ticker.upper())
    earnings_dates = stock.earnings_dates
    print(earnings_dates.head())

    # Convert the current time to match the timezone of the earnings dates
    current_time = datetime.now(pytz.timezone("America/New_York"))

    # Filter the earnings dates to only those in the future and sort them in ascending order
    future_earnings = earnings_dates[earnings_dates.index > current_time].sort_index()
    
    if not future_earnings.empty:
        next_earnings_date = future_earnings.index[0]
        next_earning_date = next_earnings_date.strftime('%Y-%m-%d')
        return f"The next expected financial statement date for {ticker.upper()} is: {next_earning_date}"
    else:
        return f"No upcoming earnings dates found for {ticker.upper()}."

if __name__ == "__main__":
    ticker_symbol = input("Enter the ticker symbol: ").upper()
    next_date = get_next_earnings_date(ticker_symbol)
    print(f"The next expected financial statement date for {ticker_symbol} is: {next_date}")