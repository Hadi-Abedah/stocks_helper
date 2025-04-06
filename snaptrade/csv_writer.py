
import csv
import os
from snaptrade.transaction_parser import parse_transactions

def csv_writer(filepath=None):
    '''Write only new transaction rows to CSV and return them for further use.'''

    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), 'transactions.csv')
        
    # Step 1: Parse new transactions
    parsed_rows = [row for output in parse_transactions() for row in output]

    # Step 2: Load existing rows if file exists
    existing_rows = set()
    if os.path.exists(filepath):
        with open(filepath, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                existing_rows.add(tuple(row))

    # Step 3: Filter new rows
    new_rows = [row for row in parsed_rows if tuple(row) not in existing_rows]

    # Step 4: Write header and new rows
    write_header = not os.path.exists(filepath)
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Date", "Account", "Debit", "Credit", "Description"])
            print("Header written, file created for first time")
        if new_rows:
            writer.writerows(new_rows)
            print(f"{len(new_rows)} new rows written to {filepath}")
        else:
            print("No new rows to write")
    

    return new_rows


if __name__ == '__main__':
    csv_writer()

