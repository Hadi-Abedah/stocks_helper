


from .helpers import was_transaction_processed, mark_transaction_as_processed


HARD_CODED = {
    # COUR bought on 2024-07-22
    "80f857d7-666f-492f-8e2b-7e78cf786f84": [
        ["2024-07-22", "TFSA (USD)", "72.28", "", "Converted 101.45 CAD to USD at exchange rate 1.403551"],
        ["2024-07-22", "Currency Conversion Expense", "1.52", "", "Currency conversion fee"],
        ["2024-07-22", "TFSA (CAD)", "", "102.97", "Converted 101.45 CAD to USD at exchange rate 1.403551 (incl. 1.5% fee)"],
        ["2024-07-22", "Investment (USD)", "72.28", "", "Bought 10 shares of COUR at $7.228 USD"],
        ["2024-07-22", "TFSA (USD)", "", "72.28", "Bought 10 shares of COUR at $7.228 USD"],
    ],
    # CRWD bought on 2024-07-23
    "f1436e70-f50f-4206-9f2b-abad1772486c": [
        ["2024-07-23", "TFSA (USD)", "529.08", "", "Converted 742.56 CAD to USD at exchange rate 1.403490"],
        ["2024-07-23", "Currency Conversion Expense", "11.14", "", "Currency conversion fee"],
        ["2024-07-23", "TFSA (CAD)", "", "753.70", "Converted 742.56 CAD to USD at exchange rate 1.403490 (incl. 1.5% fee)"],
        ["2024-07-23", "Investment (USD)", "529.08", "", "Bought 2 shares of CRWD at $264.542 USD"],
        ["2024-07-23", "TFSA (USD)", "", "529.08", "Bought 2 shares of CRWD at $264.542 USD"],
    ],
    # MSFT bought on 2024-07-26
    "8113876e-7c03-452f-bda5-b69af9c44a80": [
        ["2024-07-26", "TFSA (USD)", "424.40", "", "Converted 598.51 CAD to USD at exchange rate 1.4101"],
        ["2024-07-26", "Currency Conversion Expense", "8.98", "", "Currency conversion fee"],
        ["2024-07-26", "TFSA (CAD)", "", "607.49", "Converted 598.51 CAD to USD at exchange rate 1.4101 (incl. 1.5% fee)"],
        ["2024-07-26", "Investment (USD)", "424.40", "", "Bought 1 share of MSFT at $424.40 USD"],
        ["2024-07-26", "TFSA (USD)", "", "424.40", "Bought 1 share of MSFT at $424.40 USD"],
    ],
    # COUR bought on 2024-07-25
    "8e998a0d-93f1-4f4f-904a-bf3745527ba2": [
        ["2024-07-25", "TFSA (USD)", "456.69", "", "Converted 643.22 CAD to USD at exchange rate 1.408413"],
        ["2024-07-25", "Currency Conversion Expense", "9.65", "", "Currency conversion fee"],
        ["2024-07-25", "TFSA (CAD)", "", "652.87", "Converted 643.22 CAD to USD at exchange rate 1.408413 (incl. 1.5% fee)"],
        ["2024-07-25", "Investment (USD)", "456.69", "", "Bought 62 shares of COUR at $7.3661 USD"],
        ["2024-07-25", "TFSA (USD)", "", "456.69", "Bought 62 shares of COUR at $7.3661 USD"],
    ],
    # SYM bought on 2024-08-23
    "810bf567-b9a4-4320-9546-e259b4362059": [
        ["2024-08-23", "TFSA (USD)", "1158.00", "", "Converted 1,595.47 CAD to USD at exchange rate 1.377630"],
        ["2024-08-23", "Currency Conversion Expense", "23.93", "", "Currency conversion fee"],
        ["2024-08-23", "TFSA (CAD)", "", "1619.40", "Converted 1,595.47 CAD to USD at exchange rate 1.377630 (incl. 1.5% fee)"],
        ["2024-08-23", "Investment (USD)", "1158.00", "", "Bought 50 shares of SYM at $23.1625 USD"],
        ["2024-08-23", "TFSA (USD)", "", "1158.00", "Bought 50 shares of SYM at $23.1625 USD"],
    ],
    # ONC.TO sold on 2025-09-03 # manually credit the onc.to sicnce ticker has changed from onc.to to oncy
    "01227015-03e9-45fa-aa5d-3aae11a2bdd4": [
        ["2025-09-03", "TFSA (CAD)", "798.17", "", "Sold 500.0000 of ONC.TO at $1.17 USD"],
        ["2025-09-03", "Investment (CAD)", "", "300.00", "Sold 500.0000 of ONC.TO at $1.17 USD"],
        ["2025-09-03", "Realized Gain/Loss (CAD)", "", "498.17", "Sold 500.0000 of ONC.TO at $1.17 USD"],
    ],
}


def parse_transactions():
    """ parse each transaction and outputs csv rows(list of lists), each row is an account affected by that transaction"""
    import os
    from .snaptrade_api import get_transactions_for_user
    from .transactions import deposit, buy_usd_stock, sell_usd_stock, buy_cad_stock, sell_cad_stock, convert_cad_to_usd, fee, dividend, tax, buy_usd_put_option, buy_usd_call_option, option_expire #, sell_cad_call_option, sell_cad_put_option 
    from .helpers import was_transaction_processed, mark_transaction_as_processed, find_credited_invst_amount, update_invst_amounts
    outputs = []
    transactions = get_transactions_for_user()
    for transaction in transactions:
        if was_transaction_processed(transaction['id']):
            continue
        tid = transaction.get('id')
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
            output = convert_cad_to_usd(transaction)
        elif transaction['description'] == 'FEE':
            output = fee(transaction)
        elif transaction['type'] == 'DIVIDEND':
            output = dividend(transaction)
        elif transaction['type'] == 'TAX':
            output = tax(transaction)
        # Catch all other weird transactions to be debugged later
        else:
            import json
            tx_type = transaction.get('type')
            tid = transaction.get('id')
            date = transaction.get('settlement_date')
            wrong_file_path = os.path.join(os.path.dirname(__file__), "weird_transactions.txt")
            entry = {"id": tid, "type": tx_type, "date": date, "transaction": transaction}
            with open(wrong_file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str, indent=4) + "\n")
            # avoid emitting invalid rows
            output = []
            # optionally mark the TX as processed so it won't spam the log repeatedly
            try:
                from .helpers import mark_transaction_as_processed
                if tid:
                    mark_transaction_as_processed(tid)
            except Exception:
                pass
            output = ["",""]
        # re-assign the output variable for certain hardcoded transactions
        if tid in HARD_CODED:
            # these are flagged as processed already above in the helper functions that will execute any way
            outputs.append(HARD_CODED[tid])
            continue

        
        outputs.append(output)    
    return outputs

from .helpers import was_transaction_processed, mark_transaction_as_processed

# keep your HARD_CODED dict as-is


def parse_transactions_db():
    """
    Generator version of parse_transactions() meant for database insertion:
    yields (tx_id, rows) for each transaction, where rows is a list of 5-element rows:
        [Date, Account, Debit, Credit, Description]

    Keeps your current paradigm:
    - classify tx -> call handler -> output rows
    - then override rows if tid in HARD_CODED (row-layer override)
    Returns:
      Generator[tuple[str, list[list[str]]]]: Yields (tx_id, rows) for each transaction,
    """
    import os
    import json
    from .snaptrade_api import get_transactions_for_user
    from .transactions import (
        deposit, buy_usd_stock, sell_usd_stock, buy_cad_stock, sell_cad_stock,
        convert_cad_to_usd, fee, dividend, tax,
        buy_usd_put_option, buy_usd_call_option, option_expire,
    )
    from .helpers import was_transaction_processed  # (you already import at top; keeping local is fine)

    transactions = get_transactions_for_user()

    for transaction in transactions:
        tid = transaction.get("id")
        if not tid:
            continue

        if was_transaction_processed(tid):
            continue

        # Default output
        output = []

        # --- your existing classification chain ---
        if transaction.get("option_symbol"):
            usd = (transaction["currency"]["code"] == "USD")  # still unused but ok

            if transaction["type"] == "BUY":
                if transaction["option_symbol"]["option_type"] == "PUT":
                    output = buy_usd_put_option(transaction)
                else:
                    output = buy_usd_call_option(transaction)

            elif transaction["type"] == "OPTIONEXPIRATION":
                output = option_expire(transaction)

            else:
                raise ValueError(f"Unknown option transaction type {transaction['type']}")

        elif transaction["type"] == "CONTRIBUTION":
            output = deposit(transaction)

        elif transaction["currency"]["code"] == "USD" and transaction["type"] == "BUY":
            output = buy_usd_stock(transaction)

        elif transaction["currency"]["code"] == "USD" and transaction["type"] == "SELL":
            output = sell_usd_stock(transaction)

        elif transaction["currency"]["code"] == "CAD" and transaction["type"] == "BUY":
            output = buy_cad_stock(transaction)

        elif transaction["currency"]["code"] == "CAD" and transaction["type"] == "SELL":
            output = sell_cad_stock(transaction)

        elif transaction["type"] == "FUNDS_CONVERSION":
            output = convert_cad_to_usd(transaction)

        elif transaction.get("description") == "FEE":
            output = fee(transaction)

        elif transaction["type"] == "DIVIDEND":
            output = dividend(transaction)

        elif transaction["type"] == "TAX":
            output = tax(transaction)

        else:
            # weird logging 
            wrong_file_path = os.path.join(os.path.dirname(__file__), "weird_transactions.txt")
            entry = {
                "id": tid,
                "type": transaction.get("type"),
                "date": transaction.get("settlement_date"),
                "transaction": transaction,
            }
            with open(wrong_file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, default=str, indent=4) + "\n")

            # If you want to avoid repeated weirds, you can mark processed here.
            # But keep your existing behavior:
            try:
                if tid:
                    mark_transaction_as_processed(tid)
            except Exception:
                pass

            output = []  

        # --- row-layer override for hardcoded TIDs ---
        if tid in HARD_CODED:
            output = HARD_CODED[tid]

        # Ensure rows are well-formed (optional but strongly recommended)
        rows = [
            row for row in (output or [])
            if isinstance(row, (list, tuple)) and len(row) == 5
        ]

        yield tid, rows
          

if __name__ == "__main__":
    print("Date,Account,Debit,Credit,Description")    
    for output in parse_transactions():
        for row in output:
            print(row)
