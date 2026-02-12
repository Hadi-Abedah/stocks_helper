import requests
import yfinance as yf
import pandas as pd
from pathlib import Path
from collections import defaultdict
from stock_actions.percentage_change.daily_perc_chng import compute_daily_prec

API_URL = "https://api.callmebot.com/telegram/group.php"
API_KEY = "LTEwMDIzODAyODEzNTU"  # free trial!

def send_alert(sector_dict, label):
    if not sector_dict:
        return

    message_parts = [f"{label}:"]
    for sector, ticker_tuples in sector_dict.items():
        if ticker_tuples:
            # Sort by percentage change descending
            ticker_tuples.sort(key=lambda x: x[1], reverse=True)
            tickers_str = ", ".join(f"{sym} ({chng:.2f}%)" for sym, chng in ticker_tuples)
            message_parts.append(f"{sector}: {tickers_str}")
    
    message = "\n \n".join(message_parts)

    params = {
        "apikey": API_KEY,
        "text": message[:2500]  # truncate
    }

    try:
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")


def chunked(iterable, n):
    """Yield successive n-sized chunks from iterable."""
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]

def main():
    script_dir = Path(__file__).parent
    all_dfs = [
        pd.read_csv(f"{script_dir}/nasdaq_screener_1747363955212.csv"),
        pd.read_csv(f"{script_dir}/nasdaq_screener_1747364000664.csv")
    ]

    combined_df = pd.concat(all_dfs, ignore_index=True)
    print(f"There are {len(combined_df)} companies in my list.")

    # Grouping dictionaries
    underperform_by_sector = defaultdict(list)
    overperform_by_sector = defaultdict(list)
    symbol_sector_dict = {}
    symbols = []     
    for _, row in combined_df.iterrows():
        symbol = str(row["Symbol"]).strip()
        if symbol and symbol.lower() != 'nan':
            symbols.append(row["Symbol"])
            symbol_sector_dict[row["Symbol"]] = row["Sector"]
        
    
    try:
        all_ticker_changes = []
        for symbol_chunk in chunked(symbols[0:3000], 300):  
            ticker_changes = compute_daily_prec(symbol_chunk)
            if ticker_changes:
                all_ticker_changes.extend(ticker_changes)

        sorted_daily_changes = sorted(all_ticker_changes, key=lambda x: x[1], reverse=True)

        for symbol, perc_chng in sorted_daily_changes:
            if perc_chng <= -5:
                underperform_by_sector[symbol_sector_dict[symbol]].append((symbol, perc_chng))
            elif perc_chng >= 5:
                overperform_by_sector[symbol_sector_dict[symbol]].append((symbol, perc_chng))
    except (ValueError, TypeError) as e:
        print(f"Error - {e}")

    # Print and send alerts
    print("Underperforming by sector:", dict(underperform_by_sector))
    print("Overperforming by sector:", dict(overperform_by_sector))

    send_alert(underperform_by_sector, label="Underperformers")
    send_alert(overperform_by_sector, label="Overperformers")

if __name__ == "__main__":
    main()
