from .snaptrade_api import get_transactions_for_user
from .helpers import find_credited_invst_amount, update_invst_amounts
from .transactions import buy_usd_stock, buy_cad_stock, sell_usd_stock, sell_cad_stock, deposit, convert_cad_to_usd, fee, dividend, tax
from .google_sheets_writer import google_sheets_writer
from .csv_writer import csv_writer
import csv
import argparse


def main(db: bool = False, csv: bool = False, google_sheets: bool = False):
    if db:
        print("Database functionality not implemented yet.")
    elif csv:
        csv_writer()
    elif google_sheets:
        google_sheets_writer()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process SnapTrade transactions.")
    parser.add_argument("--db", action="store_true", help="Enable database functionality.")
    parser.add_argument("--csv", action="store_true", help="Enable CSV functionality.")
    parser.add_argument("--google-sheets", action="store_true", help="Enable Google Sheets functionality.")

    args = parser.parse_args()
    main(db=args.db, csv=args.csv, google_sheets=args.google_sheets)