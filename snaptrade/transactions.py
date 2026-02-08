from .snaptrade_api import get_api_status, list_accounts, list_account_holdings, get_transactions_for_user

def deposit(transaction):
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(transaction['amount'])
    description = transaction['description']

    row1 = [str(date), "TFSA (CAD)", f"{amount:.2f}", "", f"{description} CAD"]
    row2 = [str(date), "Cash (CAD)", "", f"{amount:.2f}", f"{description} CAD"]
    mark_transaction_as_processed(transaction["id"])
    return row1, row2

def buy_usd_stock(transaction):
    from .helpers import update_invst_amounts, was_transaction_processed, mark_transaction_as_processed
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA (USD)", "", f"{amount:.2f}", f"{description} USD"]
    row2 = [str(date), "Investment (USD)", f"{amount:.2f}", "", f"{description} USD"]

    update_invst_amounts(transaction['id'], abs(transaction['units']), symbol, transaction['price'], transaction['settlement_date'])
    mark_transaction_as_processed(transaction["id"])

    return row1, row2


def sell_usd_stock(transaction):
    from .helpers import find_credited_invst_amount
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    debited_cash_amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA (USD)", f"{debited_cash_amount:.2f}", "", f"{description} USD"]
    credited_invst_amount = find_credited_invst_amount(abs(transaction['units']), symbol)
    row2 = [str(date), "Investment (USD)", "", f"{credited_invst_amount:.2f}", f"{description} USD"]

    realized_gain_loss = debited_cash_amount - credited_invst_amount
    account = "Realized Gain/Loss (USD)"
    if realized_gain_loss > 0:
        row3 = [str(date), account, "", f"{realized_gain_loss:.2f}", f"{description} USD"]
    else:
        row3 = [str(date), account, f"{abs(realized_gain_loss):.2f}", "", f"{description} USD"]

    mark_transaction_as_processed(transaction["id"])
    return row1, row2, row3

def buy_cad_stock(transaction):
    from .helpers import update_invst_amounts, was_transaction_processed, mark_transaction_as_processed
    from datetime import datetime

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA (CAD)", "", f"{amount:.2f}", f"{description} CAD"]
    row2 = [str(date), "Investment (CAD)", f"{amount:.2f}", "", f"{description} CAD"]

    update_invst_amounts(transaction['id'], abs(transaction['units']), symbol, transaction['price'], transaction['settlement_date'])
    mark_transaction_as_processed(transaction["id"])

    return row1, row2


def sell_cad_stock(transaction):
    from .helpers import find_credited_invst_amount
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    debited_cash_amount = float(abs(transaction['amount']))
    symbol = transaction['symbol']['symbol']
    description = transaction['description']

    row1 = [str(date), "TFSA (CAD)", f"{debited_cash_amount:.2f}", "", f"{description} CAD"]
    credited_invst_amount = find_credited_invst_amount(abs(transaction['units']), symbol)
    row2 = [str(date), "Investment (CAD)", "", f"{credited_invst_amount:.2f}", f"{description} CAD"]

    realized_gain_loss = debited_cash_amount - credited_invst_amount
    account = "Realized Gain/Loss (CAD)"
    if realized_gain_loss > 0:
        row3 = [str(date), account, "", f"{realized_gain_loss:.2f}", f"{description} CAD"]
    else:
        row3 = [str(date), account, f"{abs(realized_gain_loss):.2f}", "", f"{description} CAD"]

    mark_transaction_as_processed(transaction["id"])
    return row1, row2, row3

def convert_cad_to_usd(transaction):
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    description = transaction['description']

    row1 = [str(date), "TFSA (USD)", f"{amount}", "", description]
    row2 = [str(date), "TFSA (CAD)", "", "", description]
    row3 = [str(date), "Currency Conversion Expense (CAD)", "", "", description]
    mark_transaction_as_processed(transaction["id"])
    return row1, row2, row3

def fee(transaction):
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    description = transaction['description']

    row1 = [str(date), "TFSA (CAD)", "", f"{amount:.2f}", description]
    row2 = [str(date), "Fee Expense (CAD)", f"{amount:.2f}", "", description]
    mark_transaction_as_processed(transaction["id"])
    return row1, row2

def dividend(transaction):
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    currency = transaction['currency']['code']
    description = transaction['description']

    tfsa_account = "TFSA (CAD)" if currency == "CAD" else "TFSA (USD)"
    income_account = "Dividend Income (CAD)" if currency == "CAD" else "Dividend Income (USD)"

    row1 = [str(date), tfsa_account, f"{amount:.2f}", "", description]
    row2 = [str(date), income_account, "", f"{amount:.2f}", description]
    mark_transaction_as_processed(transaction["id"])
    return row1, row2

def tax(transaction):
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    amount = float(abs(transaction['amount']))
    description = transaction['description']
    symbol_description = transaction['symbol']['description']

    row1 = [str(date), "TFSA (USD)", "", f"{amount:.2f}", description]
    row2 = [str(date), "Tax Expense (USD)", f"{amount:.2f}", "", f"{description}({symbol_description})"]
    mark_transaction_as_processed(transaction["id"])
    return row1, row2




def buy_usd_put_option(transaction):
    """
    Handle a BUY for one or more PUT contracts settled in USD.
    Produces two journal rows identical to buy_usd_stock(), except that the
    description becomes:
        "Bought <N> PUT option for <UNDERLYING> at <STRIKE>"
    """
    from datetime import datetime
    from .helpers import (
        update_invst_amounts,
        mark_transaction_as_processed,
    )

    date        = datetime.fromisoformat(transaction["settlement_date"].rstrip("Z")).date()
    amount      = float(abs(transaction["amount"]))          # premium paid (same as stock logic)
    contracts   = int(abs(transaction["units"])) *100             # each contract is 100 share 
    underlying  = transaction["symbol"]["symbol"]             # e.g. "UAMY"
    strike      = transaction["option_symbol"]["strike_price"]
    option_tkr  = transaction["symbol"]["symbol"]      

    # --- narrative --------------------------------------------------------
    description = f"Bought {contracts} PUT option for {underlying} at {strike}"

    # --- journal rows -----------------------------------------------------
    row1 = [str(date), "TFSA (USD)", "",           f"{amount:.2f}", f"{description} USD"]
    row2 = [str(date), "Investment (USD)", f"{amount:.2f}", "",         f"{description} USD"]

    update_invst_amounts(transaction["id"], contracts, option_tkr, transaction["price"], transaction["settlement_date"], is_option=True)
    mark_transaction_as_processed(transaction["id"])
    return row1, row2



def buy_usd_call_option(transaction):
    """
    Buy one or more CALL contracts settled in USD.
    """
    from datetime import datetime
    from .helpers import update_invst_amounts, mark_transaction_as_processed

    date       = datetime.fromisoformat(transaction["settlement_date"].rstrip("Z")).date()
    amount     = float(abs(transaction["amount"]))
    contracts  = int(abs(transaction["units"])) * 100          # 1 contract = 100 shares
    symbol     = transaction["symbol"]["symbol"]               # underlying ticker
    strike     = transaction["option_symbol"]["strike_price"]

    descr = f"Bought {contracts} CALL option{'s' if contracts!=100 else ''} for {symbol} at {strike}"

    row1 = [str(date), "TFSA (USD)", "", f"{amount:.2f}", f"{descr} USD"]
    row2 = [str(date), "Investment (USD)", f"{amount:.2f}", "", f"{descr} USD"]

    update_invst_amounts(contracts, symbol, transaction["price"],
                         transaction["settlement_date"], is_option=True)
    mark_transaction_as_processed(transaction["id"])
    return row1, row2


def buy_cad_put_option(transaction):
    """
    Buy PUT contracts settled in CAD.
    """
    from datetime import datetime
    from .helpers import update_invst_amounts, mark_transaction_as_processed

    date       = datetime.fromisoformat(transaction["settlement_date"].rstrip("Z")).date()
    amount     = float(abs(transaction["amount"]))
    contracts  = int(abs(transaction["units"])) * 100
    symbol     = transaction["symbol"]["symbol"]
    strike     = transaction["option_symbol"]["strike_price"]

    descr = f"Bought {contracts} PUT option{'s' if contracts!=100 else ''} for {symbol} at {strike}"

    row1 = [str(date), "TFSA (CAD)", "", f"{amount:.2f}", f"{descr} CAD"]
    row2 = [str(date), "Investment (CAD)", f"{amount:.2f}", "", f"{descr} CAD"]

    update_invst_amounts(contracts, symbol, transaction["price"],
                         transaction["settlement_date"], is_option=True)
    mark_transaction_as_processed(transaction["id"])
    return row1, row2


def buy_cad_call_option(transaction):
    """
    Buy CALL contracts settled in CAD.
    """
    from datetime import datetime
    from .helpers import update_invst_amounts, mark_transaction_as_processed

    date       = datetime.fromisoformat(transaction["settlement_date"].rstrip("Z")).date()
    amount     = float(abs(transaction["amount"]))
    contracts  = int(abs(transaction["units"])) * 100
    symbol     = transaction["symbol"]["symbol"]
    strike     = transaction["option_symbol"]["strike_price"]

    descr = f"Bought {contracts} CALL option{'s' if contracts!=100 else ''} for {symbol} at {strike}"

    row1 = [str(date), "TFSA (CAD)", "", f"{amount:.2f}", f"{descr} CAD"]
    row2 = [str(date), "Investment (CAD)", f"{amount:.2f}", "", f"{descr} CAD"]

    update_invst_amounts(contracts, symbol, transaction["price"],
                         transaction["settlement_date"], is_option=True)
    mark_transaction_as_processed(transaction["id"])
    return row1, row2


def option_expire(transaction):

    from .helpers import find_credited_invst_amount_options
    from datetime import datetime
    from .helpers import mark_transaction_as_processed

    date = datetime.fromisoformat(transaction['settlement_date'].rstrip('Z')).date()
    symbol = transaction['symbol']['symbol']
    currency = transaction["currency"]["code"]
    description = f"{transaction['description']}_{symbol}"
    premium_paid = find_credited_invst_amount_options(symbol)

    # Record the expired option premium as a debit in the realized gain/loss account
    account = f"Realized Gain/Loss ({currency})"
    row1 = [str(date), account, f"{premium_paid:.2f}", "", f"{description}"]
    row2 = [str(date), f"Investment ({currency})", "", f"{premium_paid:.2f}", f"{description}"]

    mark_transaction_as_processed(transaction["id"])
    return row1, row2








# -------------------------------------------------------------------
# SELL helpers  (mirror the stock‑sale pattern)
## -------------------------------------------------------------------
#
#def _sell_option_common(transaction, acct_currency, call_or_put):
#    """
#    Internal helper – returns the three journal rows.
#    `acct_currency` => 'USD' or 'CAD'
#    `call_or_put`   => 'CALL' or 'PUT'
#    """
#    from datetime import datetime
#    from .helpers import find_credited_invst_amount, mark_transaction_as_processed
#
#    mark_transaction_as_processed(transaction["id"])
#
#    date        = datetime.fromisoformat(transaction["settlement_date"].rstrip("Z")).date()
#    cash_inflow = float(abs(transaction["amount"]))
#    contracts   = int(abs(transaction["units"])) * 100
#    symbol      = transaction["symbol"]["symbol"]
#    strike      = transaction["option_symbol"]["strike_price"]
#
#    descr = f"Sold {contracts} {call_or_put} option{'s' if contracts!=100 else ''} for {symbol} at {strike}"
#
#    row1 = [str(date), f"TFSA({acct_currency})", f"{cash_inflow:.2f}", "", f"{descr} {acct_currency}"]
#    cost_basis = find_credited_invst_amount(contracts, symbol)
#    row2 = [str(date), f"Investment({symbol})", "", f"{cost_basis:.2f}", f"{descr} {acct_currency}"]
#
#    gain = cash_inflow - cost_basis
#    if gain >= 0:
#        row3 = [str(date), "Realized Gain on Sale", "", f"{gain:.2f}", f"{descr} {acct_currency}"]
#    else:
#        row3 = [str(date), "Realized Loss on Sale", f"{abs(gain):.2f}", "", f"{descr} {acct_currency}"]
#
#    return row1, row2, row3
#
#
#def sell_usd_put_option(transaction):
#    return _sell_option_common(transaction, "USD", "PUT")
#
#
#def sell_usd_call_option(transaction):
#    return _sell_option_common(transaction, "USD", "CALL")
#
#
#def sell_cad_put_option(transaction):
#    return _sell_option_common(transaction, "CAD", "PUT")
#
#
#def sell_cad_call_option(transaction):
#    return _sell_option_common(transaction, "CAD", "CALL")
#