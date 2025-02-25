


def daily_percentage_change(ticker, start_period, end_period, verbose=False):
    """
    Compute the daily percentage change in the stock's closing price over a given period.
    
    Parameters:
    ticker (str): The stock ticker symbol.
    start_period (str): The start date in 'YYYY-MM-DD' format.
    end_period (str): The end date in 'YYYY-MM-DD' format.
    verbose (bool): If True, prints the percentage changes. Default is False.
    
    Returns:
    pd.Series: A Pandas Series containing the daily percentage changes.
    """
    import yfinance as yf
    import pandas as pd

    # Download the stock data
    data = yf.download(ticker, start=start_period, end=end_period)
    
    # Calculate the daily percentage change
    percentage_change = data['Close'].pct_change() * 100
    
    # Optionally print all rows if verbose is True
    if verbose:
        with pd.option_context('display.max_rows', None):
            print(percentage_change)
            print(data)
    
    return percentage_change.dropna()  # Optionally, you could choose to fillna(0) or handle NaN differently

# Example usage:
# percentage_changes = daily_percentage_change("SBUX", "2024-08-01", "2024-08-20", verbose=True)




def weekly__percentage_change(ticker, start_period, end_period, verbose=False):
    """
    Compute the weekly percentage change in the stock's closing price over a given period.
    
    Parameters:
    ticker (str): The stock ticker symbol.
    start_period (str): The start date in 'YYYY-MM-DD' format.
    end_period (str): The end date in 'YYYY-MM-DD' format.
    verbose (bool): If True, prints the percentage changes. Default is False.
    
    Returns:
    pd.Series: A Pandas Series containing the daily percentage changes.
    """
    
    import yfinance as yf
    import pandas as pd

    # Download the stock data
    data = yf.download(ticker, start=start_period, end=end_period)
    weekly_data = data['Close'].resample('W').last()
    
    # Calculate the daily percentage change
    percentage_change = weekly_data.pct_change() * 100
    
    # Optionally print all rows if verbose is True
    if verbose:
        with pd.option_context('display.max_rows', None):
            print(percentage_change)
            print(data)
    
    return percentage_change.dropna()

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol (e.g., 'AAPL'): ")
    start_period = input("Enter the start date (YYYY-MM-DD): ")
    end_period = input("Enter the end date (YYYY-MM-DD): ")
    
    # Optional: Ask whether to print the output
    verbose_input = input("Do you want to print the results? (yes/no): ")
    verbose = verbose_input.lower() in ['yes', 'y']
    # Optional: Ask whether to use weekly or daily values 
    caller = input("Do you want daily or weekly percentages?: ")
    if caller.lower() == "daily":
    # Call the function with the input values
        percentage_changes = daily_percentage_change(ticker, start_period, end_period, verbose)
    else:
        percentage_changes = weekly__percentage_change(ticker, start_period, end_period, verbose)
    
