import json

import json
import os

def find_credited_invst_amount(sold_shares, ticker, file_path=None):
    """ Read from json to determine how much to credit the investment account after a stock sell. """

    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "stocks.json")
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")

    with open(file_path, "r") as f:
        stocks = json.load(f)

    total_amount = 0
    for price, available_shares in stocks.get(ticker, {}).items():
        if sold_shares > available_shares:
            total_amount += float(price.split('_')[0]) * available_shares
            sold_shares -= available_shares
            stocks[ticker][price] = 0  
        else:
            total_amount += sold_shares * float(price.split('_')[0])
            stocks[ticker][price] -= sold_shares
            break

    # Write the updated stocks back to the file
    with open(file_path, "w") as f:
        json.dump(stocks, f, indent=4)

    return total_amount


def update_invst_amounts(bought_shares, ticker, price, date, file_path=None):
    """ Write to a json file to track stock purchases for later selling. """

    from datetime import datetime
    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "stocks.json")
        
    date = datetime.fromisoformat(date).strftime("%Y-%m-%d")
    unique_key = f"{price}_{date}"  # so When I purchase in future with the same price, FIFO is preserved!
    # I will hard code some transactions that were USD stocks, but bought using CAD in the period 2024-07-22 to 2024-08-23
    if ticker == 'SYM' and unique_key == '31.9094_2024-08-23':
        unique_key = '23.1625_2024-08-23'
    if ticker == 'COUR' and unique_key == '10.145_2024-07-22':
        unique_key = '7.228_2024-07-22'
    if ticker == 'COUR' and unique_key == '10.3745_2024-07-25':
        unique_key = '7.3661_2024-07-25'
    if ticker == 'CRWD' and unique_key == '371.28_2024-07-23':
        unique_key = '264.542_2024-07-23'
    if ticker == 'MSFT' and unique_key == '598.51_2024-07-26':
        unique_key = '424.405_2024-07-26'
    

    try:
        with open(file_path, "r") as f:
            stocks = json.load(f)
        if ticker in stocks:
            # if I buy twice the same stock in same price in single day. It just adds the number!
            if unique_key in stocks[ticker]:
                stocks[ticker][unique_key] += bought_shares
            else:
                stocks[ticker][unique_key] = bought_shares
        else:
            stocks[ticker] = {unique_key: bought_shares}

    except (FileNotFoundError, json.JSONDecodeError):
        stocks = {ticker: {unique_key: bought_shares}}

    with open(file_path, "w") as f:
        json.dump(stocks, f, indent=4)


def find_all_transcription_types(start_date="2024-07-01", end_date="2025-03-19"):
    from .snaptrade_api import get_transactions_for_user
    import json
    transactions = get_transactions_for_user(start_date=start_date, end_date=end_date)
    transactions_dict = {} 
    lst_of_transactions = []
    for transaction in transactions:
        if transaction['type'] == 'TAX':
            
            lst_of_transactions.append(transaction)
            transactions_dict[transaction['type']] = transaction['description']
    return transactions_dict, lst_of_transactions 


#resp = find_all_transcription_types()
#print(resp)



