
import requests
import yfinance as yf
import pandas as pd
from pathlib import Path
from percentage_change.daily_perc_chng import compute_daily_prec

API_URL = "https://api.callmebot.com/telegram/group.php"
API_KEY = "LTEwMDIzODAyODEzNTU"

def send_alert(companies, label):
    if not companies:
        return  # Don't send an empty message

    message = f"{label}: " + ", ".join(companies)
    formatted_message = message.replace(" ", "+")  # Replace spaces with '+' for URL encoding

    params = {
        "apikey": API_KEY,
        "text": formatted_message
    }

    try:
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")

def main():
    script_dir = Path(__file__).parent
    companies = []
    under_perform_stocks = []
    over_perform_stocks = []

    df1 = pd.read_csv(f"{script_dir}/nasdaq_screener_1724268381610.csv")
    df2 = pd.read_csv(f"{script_dir}/nasdaq_screener_1724268475973.csv")
    companies = df1["Symbol"].tolist() + df2["Symbol"].tolist()
    print(f"There are {len(companies)} companies in my list.")

    for comp in companies:
        perc_chng = compute_daily_prec(comp)
        try:
            print(f"{comp}: {perc_chng}%")
            if perc_chng <= -5:
                under_perform_stocks.append(comp)
            elif perc_chng >= 5:
                over_perform_stocks.append(comp)
        except (ValueError, TypeError) as e:
            print(e)

    # Alert via API
    print("under_perform_stocks:", under_perform_stocks, label="under_perform_stocks")
    print("over_perform_stocks:", over_perform_stocks, label="over_perform_stocks")
    send_alert(under_perform_stocks)
    send_alert(over_perform_stocks)

if __name__ == "__main__":
    main()
