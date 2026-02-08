from .snaptrade_api import get_transactions_for_user
from .helpers import find_credited_invst_amount, update_invst_amounts
from .transactions import buy_usd_stock, buy_cad_stock, sell_usd_stock, sell_cad_stock, deposit, convert_cad_to_usd, fee, dividend, tax
from .google_sheets_writer import google_sheets_writer

import csv


def main():
    google_sheets_writer()


if __name__ == "__main__":
    main()