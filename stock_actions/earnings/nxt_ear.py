import yfinance as yf
from datetime import datetime, date
import pytz
import json

def get_next_earnings_date(ticker):
    ''' arg: ticker or list of tickers
        returns: ticker, next_earnings_date, eps, revenue
    '''
    try:
        stock = yf.Ticker(ticker.upper())
        #print(type(stock.calendar))
        # stock is now a dict
        stock = stock.calendar
        next_earnings_date = stock["Earnings Date"][0] # it gives 2 datatimes when uncertan, I choose the nearest
        print(f"{ticker} is {next_earnings_date}")
        if next_earnings_date < date.today():
            next_earnings_date = None
        eps = stock["Earnings Average"]
        revenue = stock["Revenue Average"] / 10**6 
        if next_earnings_date:
            return ticker.upper(), next_earnings_date, eps, revenue

        else:
            return ticker.upper(), None, None, None
    except Exception as e:
        print(f"An error occurred while processing {ticker}: {e}")
        return ticker.upper(), None, None, None



if __name__ == "__main__":
    ticker_symbol = "BA"
    next_date = get_next_earnings_date(ticker_symbol)
    print(next_date)