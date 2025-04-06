



def google_sheets_writer():
    import gspread
    from google.oauth2.service_account import Credentials
    from .csv_writer import csv_writer
    from pathlib import Path
    import time
    import gspread.exceptions

    script_path = Path(__file__).resolve().parent
    SERVICE_ACCOUNT_FILE = script_path / "python-docs-433001-62f7d270af5b.json"
    # check for new rows (new stock transactions)
    new_rows = csv_writer()
    
    if new_rows:
           
        # Define the scope: what APIs we want access to
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        # Load the service account credentials
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Use gspread to authenticate with those credentials
        client = gspread.authorize(creds)

        # Open a specific Google Sheet by name or ID
        sheet = client.open("stock_transactions").sheet1

        # append rows
        for row in new_rows:
            MAX_ATTEMPTS = 5
            for attempt in range(MAX_ATTEMPTS):
                try:
                    sheet.append_row(row)
                    break #success
                except gspread.exceptions.APIError as e:
                    if "429" in str(e):
                        wait = 4 ** attempt
                        print(f"Rate limit hit. Retrying in {wait}s...")
                        time.sleep(wait)
                    else:
                        raise e
    else:
        print("no new rows")


if __name__ == "__main__":
    google_sheets_writer()