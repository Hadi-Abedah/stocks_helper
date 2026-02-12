
def compute_daily_prec(tickers=None):
    """
    Fetches historical closing price data and computes the daily percentage change for each ticker.
    
    Parameters:
        tickers (list): List of ticker symbols. Defaults to a predefined list if None.
        
    Returns:
        list: A list of tuples, mapping each ticker to its percentage change from the previous day.
    """
    import yfinance as yf
    
    if tickers is None:
        tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"]
    
    daily_changes = []
    print(f"Downloading data for {len(tickers)} tickers")
    data = yf.download(
    tickers,
    period="5d",
    threads=True,
    progress=True,
    auto_adjust=True   # explicitly silence that warning
    )
    if data.empty:
        print("No data found for the provided tickers.")
        return None
    
    # Process each ticker
    for ticker in tickers:
        
        close_prices = data['Close'][ticker]
        if len(close_prices) < 2:
            print(f"Not enough data to compute change for {ticker}")
            continue
        today_price = close_prices.iloc[-1]
        yesterday_price = close_prices.iloc[-2]
        perc_change = ((today_price - yesterday_price) / yesterday_price) * 100
        #print(f"Percentage change for {ticker}: {perc_change:.2f}%")
        daily_changes.append((ticker, perc_change))
    sorted_daily_changes = sorted(daily_changes, key=lambda x: x[1], reverse=True)
    #print(sorted_daily_changes)
    return sorted_daily_changes

if __name__ == "__main__":
    response = compute_daily_prec()
    print(response)
