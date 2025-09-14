





def parse_transactions():
    """ parse each transaction and outputs csv rows(list of lists), each row is an account affected by that transaction"""
    
    from .snaptrade_api import get_transactions_for_user
    from .transactions import deposit, buy_usd_stock, sell_usd_stock, buy_cad_stock, sell_cad_stock, convert_usd_to_cad, fee, dividend, tax, buy_usd_put_option, buy_usd_call_option, option_expire #, sell_cad_call_option, sell_cad_put_option 
    from .helpers import was_transaction_processed
    outputs = []
    transactions = get_transactions_for_user()
    for transaction in transactions:
        if was_transaction_processed(transaction['id']):
            continue
        # Check if it is an option contract first
        if transaction.get("option_symbol"):
            # currency split if you someday trade CAD‑settled options
            usd = (transaction["currency"]["code"] == "USD")

            # BUY or SELL?                         # until now I only bought put option and it expired, so the code is not complete!
            if transaction["type"] == "BUY":
                if transaction["option_symbol"]["option_type"] == "PUT":
                    output = buy_usd_put_option(transaction)  #if usd else buy_cad_put_option(transaction)
                else:  # CALL
                    output = buy_usd_call_option(transaction) #if usd else buy_cad_call_option(transaction)

            #elif transaction["type"] == "SELL":
            #    if transaction["option_symbol"]["option_type"] == "PUT":
            #        output = sell_usd_put_option(transaction) if usd else sell_cad_put_option(transaction)
            #    else:  # CALL
            #        output = sell_usd_call_option(transaction) if usd else sell_cad_call_option(transaction)
            #
            elif transaction["type"] == "OPTIONEXPIRATION":
               output = option_expire(transaction)

            else:
                raise ValueError(f"Unknown option transaction type {transaction['type']}")
        elif transaction['type'] == 'CONTRIBUTION':
            output = deposit(transaction)
        elif transaction['currency']['code'] == 'USD' and transaction['type'] == 'BUY':
            output = buy_usd_stock(transaction)
        elif transaction['currency']['code'] == 'USD' and transaction['type'] == 'SELL':
            output = sell_usd_stock(transaction)
        elif transaction['currency']['code'] == 'CAD' and transaction['type'] == 'BUY':
            output = buy_cad_stock(transaction)
        elif transaction['currency']['code'] == 'CAD' and transaction['type'] == 'SELL':
            output = sell_cad_stock(transaction)
        elif transaction['type'] == 'FUNDS_CONVERSION':
            output = convert_usd_to_cad(transaction)
        elif transaction['description'] == 'FEE':
            output = fee(transaction)
        elif transaction['type'] == 'DIVIDEND':
            output = dividend(transaction)
        elif transaction['type'] == 'TAX':
            output = tax(transaction)
        else:
            tx_type = transaction.get('type')  # None if missing
            date = transaction.get('settlement_date')
            with open("./weird_transactions.txt", "a", encoding="utf-8") as f:
                f.write(f"Invalid transaction type: {tx_type!r}, Date: {date}\n")
            output = ["",""]
            #raise ValueError(f"Invalid transaction type: {tx_type!r}, Date: {date}")

        
        # I will hard code some transcations that were USD stcks, but bought uing CAD in the period 2024-07-22 to 2024-08-23
        
        
        if (output[0], output[1]) == (
            ["2024-07-22", "TFSA(CAD)", "", "101.45", "Bought 10.0000 of COUR at $10.14 CAD"],
            ["2024-07-22", "Investment(COUR)", "101.45", "", "Bought 10.0000 of COUR at $10.14 CAD"]
        ):
            rows = [
                ["2024-07-22", "TFSA(USD)", "72.28 USD", "", "Converted 101.45 CAD to USD at exchange rate 1.403551"],
                ["2024-07-22", "TFSA(CAD)", "", "101.45 CAD", "Converted 101.45 CAD to USD at exchange rate 1.403551"],
                ["2024-07-22", "Currency Conversion Expense", "1.52 CAD", "", "Currency conversion fee"],
                ["2024-07-22", "TFSA(CAD)", "", "1.52 CAD", "Currency conversion fee"],
                ["2024-07-22", "Investments (COUR)", "72.28 USD", "", "Purchased 10 shares of COUR at $7.228 USD per share"],
                ["2024-07-22", "TFSA(USD)", "", "72.28 USD", "Purchased 10 shares of COUR at $7.228 USD per share"],
            ]
            
            output = rows
            
        
        if (output[0], output[1]) == (
            ["2024-07-23", "TFSA(CAD)", "", "742.56", "Bought 2.0000 of CRWD at $371.28 CAD"],
            ["2024-07-23", "Investment(CRWD)", "742.56", "", "Bought 2.0000 of CRWD at $371.28 CAD"]
        ):
            rows = [
                ["2024-07-23", "TFSA(USD)", "529.08 USD", "", "Converted 742.56 CAD to USD at exchange rate 1.403490"],
                ["2024-07-23", "TFSA(CAD)", "", "742.56 CAD", "Converted 742.56 CAD to USD at exchange rate 1.403490"],
                ["2024-07-23", "Currency Conversion Expense", "11.14 CAD", "", "Currency conversion fee"],
                ["2024-07-23", "TFSA(CAD)", "", "11.14 CAD", "Currency conversion fee"],
                ["2024-07-23", "Investments (CRWD)", "529.08 USD", "", "Purchased  2 shares of CRWD at $264.542 USD per share"],
                ["2024-07-23", "TFSA(USD)", "", "529.08 USD", "Purchased shares of CRWD"],
            ]

            output = rows
        
        if (output[0], output[1]) == (
            ["2024-07-26", "TFSA(CAD)", "", "598.51", "Bought 1.0000 of MSFT at $598.51 CAD"],
            ["2024-07-26", "Investment(MSFT)", "598.51", "", "Bought 1.0000 of MSFT at $598.51 CAD"]
        ):
            rows = [
                ["2024-07-26", "TFSA(USD)", "424.40 USD", "", "Converted 598.51 CAD to USD at exchange rate 1.4101"],
                ["2024-07-26", "TFSA(CAD)", "", "598.51 CAD", "Converted 598.51 CAD to USD at exchange rate 1.4101"],
                ["2024-07-26", "Currency Conversion Expense", "8.97 CAD", "", "Currency conversion fee"],
                ["2024-07-26", "TFSA(CAD)", "", "8.97 CAD", "Currency conversion fee"],
                ["2024-07-26", "Investments (MSFT)", "424.40 USD", "", "Purchased 1 share of MSFT at $424.40 USD per share"],
                ["2024-07-26", "TFSA(USD)", "", "424.40 USD", "Purchased 1 share of MSFT at $424.40 USD per share"],
            ]
            
            output = rows
        
        if (output[0], output[1]) == (
            ["2024-07-25", "TFSA(CAD)", "", "643.22", "Bought 62.0000 of COUR at $10.37 CAD"],
            ["2024-07-25", "Investment(COUR)", "643.22", "", "Bought 62.0000 of COUR at $10.37 CAD"]
        ):
            rows = [
                ["2024-07-25", "TFSA(USD)", "456.69 USD", "", "Converted 643.22 CAD to USD at exchange rate 1.408413"],
                ["2024-07-25", "TFSA(CAD)", "", "643.22 CAD", "Converted 643.22 CAD to USD at exchange rate 1.408413"],
                ["2024-07-25", "Currency Conversion Expense", "9.65 CAD", "", "Currency conversion fee"],
                ["2024-07-25", "TFSA(CAD)", "", "9.65 CAD", "Currency conversion fee"],
                ["2024-07-25", "Investments (COUR)", "456.69 USD", "", "Purchased 62 shares of COUR at $7.3661 USD per share"],
                ["2024-07-25", "TFSA(USD)", "", "456.69 USD", "Purchased 62 shares of COUR at $7.3661 USD per share"],
            ]
            
            output = rows

        if (output[0], output[1]) == (
            ["2024-08-23", "TFSA(CAD)", "", "1595.47", "Bought 50.0000 of SYM at $31.91 CAD"],
            ["2024-08-23", "Investment(SYM)", "1595.47", "", "Bought 50.0000 of SYM at $31.91 CAD"]
        ):
            rows = [
                ["2024-08-23", "Cash(CAD) (Owner's Equity)", "", "2000 CAD", "Fourth deposit"],
                ["2024-08-23", "TFSA(USD)", "1158.00 USD", "", "Converted 1,595.47 CAD to USD at exchange rate 1.377630"],
                ["2024-08-23", "TFSA(CAD)", "", "1595.47 CAD", "Converted 1,595.47 CAD to USD at exchange rate 1.377630"],
                ["2024-08-23", "Currency Conversion Expense", "24.00 CAD", "", "Currency conversion fee"],
                ["2024-08-23", "TFSA(CAD)", "", "24.00 CAD", "Currency conversion fee"],
                ["2024-08-23", "Investments (SYM)", "1158.00 USD", "", "Purchased 50 shares of SYM at $23.1625 USD per share"],
                ["2024-08-23", "TFSA(USD)", "", "1158.00 USD", "Purchased 50 shares of SYM at $23.1625 USD per share"],
            ]
            
            output = rows
        outputs.append(output)    
    return outputs
            

if __name__ == "__main__":
    print("Date,Account,Debit,Credit,Description")    
    for output in parse_transactions():
        for row in output:
            print(row)
