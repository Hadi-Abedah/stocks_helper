import yfinance as yf
from datetime import datetime
import pytz

def get_next_earnings_date(ticker):
    ''' arg: ticker or list of tickers
        returns: string describing next exprected earning date with some expectation about revernue and earning'''
    try:
        stock = yf.Ticker(ticker.upper())
        #print(type(stock.calendar))
        # stock is now a dict
        stock = stock.calendar
        next_earnings_date = stock["Earnings Date"][0] # it gives 2 datatimes when uncertan, I choose the nearest
        next_earning_date = next_earnings_date.strftime('%Y-%m-%d')
        eps = stock["Earnings Average"]
        revenue = stock["Revenue Average"] / 10**6 
        if next_earning_date:
            return f"""The next expected financial statement date for {ticker.upper()} is: {next_earning_date}.
                The average EPS is: {eps}, with an average Revenue of {revenue} million dollars

            """
        else:
            return f"No upcoming earnings dates found for {ticker.upper()}."
    except Exception as e:
        print(f"An error occurred while processing {ticker}: {e}")
        return f"No upcoming earnings dates found for {ticker.upper()}."



if __name__ == "__main__":
    ticker_symbol = "JKS"
    next_date = get_next_earnings_date(ticker_symbol)
    print(next_date)