
def compute_daily_prec(ticker):
    import yfinance as yf
    from datetime import datetime

    try:
        # Download data for the last five days to ensure we capture the previous trading day's close
        data = yf.download(ticker, period="5d", interval="1d")

        # Ensure we have at least two days of data
        if len(data) < 2:
            raise ValueError("Not enough data to compare. Ensure the stock has traded on the last two days.")

        # Get the close price for the previous day
        previous_close_price = data['Close'].iloc[-2]

        # Download data for the current day to get the most recent price
        intraday_data = yf.download(ticker, period="1d", interval="1m")

        # Ensure there's data for the current day
        if intraday_data.empty:
            raise ValueError("No intraday data available for today. Market might be closed or data is not available.")

        # Get the last available "Close" price for the current day (most recent price)
        last_close_price = intraday_data['Close'].iloc[-1]

        # Calculate the percentage change
        percentage_change = ((last_close_price - previous_close_price) / previous_close_price) * 100

        # Print the results
        #print(f"Previous close price for {ticker}: ${previous_close_price:.2f}")
        #print(f"Last available price for {ticker} on {datetime.now().date()}: ${last_close_price:.2f}")
        #print(f"Percentage change: {percentage_change:.2f}%")

        return percentage_change

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    ticker = input("Enter the company ticker: ")
    # Print the results
    compute_daily_prec(ticker)
