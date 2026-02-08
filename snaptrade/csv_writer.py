import csv
import os
from snaptrade.transaction_parser import parse_transactions


def csv_writer(filepath: str | None = None):
    """
    Parse *unprocessed* SnapTrade transactions and append their corresponding
    double-entry accounting rows to a CSV ledger.

    This function assumes `parse_transactions()` already performs transaction-level
    deduplication via processed transaction IDs (i.e., it only yields outputs for
    transactions that have not been consumed before). Therefore, this writer does
    not attempt to de-duplicate at the CSV row level.

    Behavior:
    - Flattens the outputs of `parse_transactions()` into a single list of rows.
    - Skips outputs that are `None` (e.g., unknown/unsupported transaction shapes).
    - Writes a header if the file does not exist or is empty.
    - Appends the new rows to the CSV file.

    Row format:
    Each written row must be a 5-element list/tuple:
        [Date, Account, Debit, Credit, Description]

    Args:
        filepath: Optional path to the CSV file. If None, defaults to
                  'transactions.csv' in the same directory as this script.

    Returns:
        list[list[str]]: The list of rows appended to the CSV during this call.

    Raises:
        OSError: If the CSV file cannot be opened or written.
    """
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "transactions.csv")

    # Parse new transactions and keep only well-formed rows.
    new_rows = [
        row
        for output in parse_transactions()
        if output
        for row in output
        if isinstance(row, (list, tuple)) and len(row) == 5
    ]

    write_header = (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0)

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["Date", "Account", "Debit", "Credit", "Description"])
            print("Header written, file created for first time (or was empty).")

        if new_rows:
            writer.writerows(new_rows)
            print(f"{len(new_rows)} new rows written to {filepath}")
        else:
            print("No new rows to write")

    return new_rows


if __name__ == "__main__":
    csv_writer()
