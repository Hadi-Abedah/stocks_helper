import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snaptrade.settings")
django.setup()

from myapp.models import journal
from .transaction_parser import parse_transactions_db


def write_to_db():
    """
    Parse *unprocessed* SnapTrade transactions and append their corresponding
    double-entry accounting rows to the database ledger.

    This function assumes `parse_transactions_db()` already performs
    transaction-level deduplication via processed transaction IDs.

    `parse_transactions_db()` is a generator that yields:

        Generator[tuple[str, list[list[str]]]]

    Meaning:
        For each transaction, it yields:
            (tx_id, rows)

        where:
            tx_id: str
            rows: list of 5-element lists:
                  [Date, Account, Debit, Credit, Description]

    Behavior:
    - Iterates transaction-by-transaction.
    - Skips empty row sets.
    - Inserts each valid journal row into the database.

    Returns:
        list[tuple[str, list[list[str]]]]:
            List of successfully written (tx_id, rows) pairs.
    """

    written = []

    for tx_id, rows in parse_transactions_db():
        if not rows:
            continue

        for row in rows:
            if not isinstance(row, (list, tuple)) or len(row) != 5:
                continue

            journal.objects.create(
                date=row[0],
                account=row[1],
                debit=row[2],
                credit=row[3],
                description=row[4],
                txn_id=tx_id,
            )

        written.append((tx_id, rows))

    return written
