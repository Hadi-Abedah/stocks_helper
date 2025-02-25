import asyncio
import yfinance as yf

async def fetch_data(ticker):
    loop = asyncio.get_event_loop()
    # Run the blocking function in a separate thread
    data = await loop.run_in_executor(None, yf.Ticker(ticker).history)
    print(f"Data for {ticker}:")
    print(data)

async def fetch_all_data(tickers):
    # Gather tasks for all tickers
    tasks = [fetch_data(ticker) for ticker in tickers]
    # Run all tasks concurrently
    await asyncio.gather(*tasks)

# List of tickers
tickers = ["AAPL", "GOOGL", "MSFT"]

# Run the event loop
asyncio.run(fetch_all_data(tickers))
