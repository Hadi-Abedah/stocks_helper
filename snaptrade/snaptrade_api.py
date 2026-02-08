from dotenv import load_dotenv
import os
import json

# secrests
load_dotenv()

client_id = os.getenv("CLIENT_ID")
consumer_key = os.getenv("CONSUMER_KEY")
user_secret = os.getenv("USER_SECRET")
user_id = os.getenv("USER_ID")
usd_account_id = os.getenv("USD_ACCOUNT_ID")
cad_account_id = os.getenv("CAD_ACCOUNT_ID")

        

def get_api_status():
    """ Checks the status of the API. """

    from pprint import pprint
    from snaptrade_client import SnapTrade

    snaptrade = SnapTrade(
        client_id=client_id,
        consumer_key=consumer_key
    )

    response = snaptrade.api_status.check()
    pprint(response.body) 



def list_accounts():
    """ Checks all accounts for a user. """

    from pprint import pprint
    from snaptrade_client import SnapTrade

    snaptrade = SnapTrade(
        client_id=client_id,
        consumer_key=consumer_key
    )

    response = snaptrade.account_information.list_user_accounts(
        user_id=user_id,
        user_secret=user_secret
    )
    pprint(response.body) 

def list_account_holdings():
    """ List stock tickers in USD, CAD accounts """

    from pprint import pprint
    from snaptrade_client import SnapTrade

    snaptrade = SnapTrade(
        client_id=client_id,
        consumer_key=consumer_key
    )

    response_1 = snaptrade.account_information.get_user_holdings(
        account_id=usd_account_id,
        user_id=user_id,
        user_secret=user_secret
    )
    response_2 = snaptrade.account_information.get_user_holdings(
        account_id=cad_account_id,
        user_id=user_id,
        user_secret=user_secret
    )
    #pprint(response.body) 
    resp = response_1.body
    ticker_symbols = [position["symbol"]["symbol"]["symbol"] for position in resp.get("positions", [])]
    resp = response_2.body
    ticker_symbols = ticker_symbols + [position["symbol"]["symbol"]["symbol"] for position in resp.get("positions", [])]
    print(ticker_symbols)
    return ticker_symbols

def get_transactions_for_user(start_date='2024-04-01', end_date=None): 
    """ Get all transactions for a user in chronological order. """ 

    from pprint import pprint
    from snaptrade_client import SnapTrade
    from datetime import datetime
    
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
        
    snaptrade = SnapTrade(
        client_id=client_id,
        consumer_key=consumer_key
    )

    response = snaptrade.account_information.get_account_activities(
        account_id=cad_account_id,   # this will give me for both CAD, and USD (after June 2025)
        user_id=user_id,
        user_secret=user_secret,
        start_date=start_date,
        end_date=end_date
    )
    response_2 = snaptrade.account_information.get_account_activities(
        account_id=usd_account_id,
        user_id=user_id,
        user_secret=user_secret,
        start_date=start_date,
        end_date=end_date
    )
    response.body["data"].extend(response_2.body["data"])
    #pprint(response.body)
    resp = sorted(response.body["data"], key=lambda x: x.get("settlement_date") or x.get("trade_date"))
    #print(resp)
    
    return resp

if __name__ == "__main__":
    #get_api_status()
    #list_accounts()
    
    #list_account_holdings()
    resp = get_transactions_for_user("2025-09-03", "2025-09-03")  #just to make sure all good!
    print(json.dumps(resp, indent=4))