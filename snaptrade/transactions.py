from .snaptrade_api import get_api_status, list_accounts, list_account_holdings, get_transactions_for_user

def deposit(transaction):
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(transaction['amount'])
    description = transaction['description']

    row1 = [str(date), "TFSA(CAD)", f"{amount:.2f}", "", f"{description} CAD"]
    row2 = [str(date), "Cash(CAD)", "", f"{amount:.2f}", f"{description} CAD"]
    return row1, row2

def buy_usd_stock(transaction):
    from .helpers import update_invst_amounts
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA(USD)", "", f"{amount:.2f}", f"{description} USD"]
    row2 = [str(date), f"Investment({symbol})", f"{amount:.2f}", "", f"{description} USD"]
    update_invst_amounts(abs(transaction['units']), symbol, transaction['price'], transaction['settlement_date'])

    return row1, row2

def sell_usd_stock(transaction):
    from .helpers import find_credited_invst_amount
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    debited_cash_amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA(USD)", f"{debited_cash_amount:.2f}", "", f"{description} USD"]
    credited_invst_amount = find_credited_invst_amount(abs(transaction['units']), symbol)
    row2 = [str(date), f"Investment({symbol})", "", f"{credited_invst_amount:.2f}", f"{description} USD"]

    realized_gain_loss = debited_cash_amount - credited_invst_amount
    if realized_gain_loss > 0:
        row3 = [str(date), "Realized Gain on Sale", "", f"{realized_gain_loss:.2f}", f"{description} USD"]
    else:
        row3 = [str(date), "Realized Loss on Sale", f"{abs(realized_gain_loss):.2f}", "", f"{description} USD"]

    return row1, row2, row3

def buy_cad_stock(transaction):
    from .helpers import update_invst_amounts
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA(CAD)", "", f"{amount:.2f}", f"{description} CAD"]
    row2 = [str(date), f"Investment({symbol})", f"{amount:.2f}", "", f"{description} CAD"]

    update_invst_amounts(abs(transaction['units']), symbol, transaction['price'], transaction['settlement_date'])

    return row1, row2

def sell_cad_stock(transaction):
    from .helpers import find_credited_invst_amount
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    debited_cash_amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA(CAD)", f"{debited_cash_amount:.2f}", "", f"{description} CAD"]
    credited_invst_amount = find_credited_invst_amount(abs(transaction['units']), symbol)
    row2 = [str(date), f"Investment({symbol})", "", f"{credited_invst_amount:.2f}", f"{description} CAD"]

    realized_gain_loss = debited_cash_amount - credited_invst_amount
    if realized_gain_loss > 0:
        row3 = [str(date), "Realized Gain on Sale", "", f"{realized_gain_loss:.2f}", f"{description} CAD"]
    else:
        row3 = [str(date), "Realized Loss on Sale", f"{abs(realized_gain_loss):.2f}", "", f"{description} CAD"]

    return row1, row2, row3

def convert_usd_to_cad(transaction):
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    description = transaction['description']

    row1 = [str(date), "TFSA(USD)", f"{amount}", "", description]
    row2 = [str(date), "TFSA(CAD)", "", "", description]
    row3 = [str(date), "Currency Conversion Expense", "", "", description]
    return row1, row2, row3

def fee(transaction):
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    description = transaction['description']

    row1 = [str(date), "TFSA(CAD)", "", f"{amount:.2f}", description]
    row2 = [str(date), "TFSA Fee Expense", f"{amount:.2f}", "", description]
    return row1, row2

def dividend(transaction):
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    currency = transaction['currency']['code']
    description = transaction['description']

    tfsa_account = "TFSA(CAD)" if currency == "CAD" else "TFSA(USD)"
    income_account = "Dividend Income(CAD)" if currency == "CAD" else "Dividend Income(USD)"

    row1 = [str(date), tfsa_account, f"{amount:.2f}", "", description]
    row2 = [str(date), income_account, "", f"{amount:.2f}", description]
    return row1, row2

def tax(transaction):
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    description = transaction['description']
    symbol_description = transaction['symbol']['description']

    row1 = [str(date), "TFSA(USD)", "", f"{amount:.2f}", description]
    row2 = [str(date), "Tax Expense", f"{amount:.2f}", "", f"{description}({symbol_description})"]
    return row1, row2
