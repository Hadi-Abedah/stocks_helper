
import unittest
from .snaptrade_api import get_api_status
import json
import os
from datetime import datetime
from .helpers import update_invst_amounts, find_credited_invst_amount
from .transactions import deposit, buy_usd_stock, sell_usd_stock  
from dotenv import load_dotenv

# secrests
load_dotenv()

client_id = os.getenv("CLIENT_ID")
consumer_key = os.getenv("CONSUMER_KEY")
user_secret = os.getenv("USER_SECRET")
user_id = os.getenv("USER_ID")
usd_account_id = os.getenv("USD_ACCOUNT_ID")
cad_account_id = os.getenv("CAD_ACCOUNT_ID")

class TestHealth(unittest.TestCase):
    """Test that my api is working correctly"""
    def test_api_status(self):
        """ Checks the status of the API. """
        from pprint import pprint
        from snaptrade_client import SnapTrade

        snaptrade = SnapTrade(
            client_id=client_id,
            consumer_key=consumer_key
        )

        response = snaptrade.api_status.check()
        pprint(response.body)
        self.assertEqual(response.body['online'], True)




# Define a temporary test file to prevent modifying the actual stocks.json
TEST_FILE = "stocks.json"

class TestStockTransactions(unittest.TestCase):
    
    def setUp(self):
        """ Create a temporary test JSON file before running tests. """
        test_data = {"BA": {"160": 10}, "AAPL": {"150": 5, "140": 10}}
        with open(TEST_FILE, "w") as f:
            json.dump(test_data, f)

    def test_deposit(self):
        """Test if deposit transaction rows are generated correctly."""
        expected_row1 = "2025-01-02, Cash(CAD), 1000.00, , Deposit of $1000.00 CAD"
        expected_row2 = "2025-01-02, Capital(Owner's Equity), , 1000.00, Deposit of $1000.00 CAD"
        
        row1, row2 = deposit()
        
        self.assertEqual(row1, expected_row1)
        self.assertEqual(row2, expected_row2)

    def test_buy_usd_stock(self):
        """Test if buy USD stock transaction rows are generated correctly."""
        expected_row1 = "2025-03-13, Cash(USD), , 507.38, Bought 13.0000 of SMCI at $39.03 USD"
        expected_row2 = "2025-03-13, Investment(SMCI), 507.38, , Bought 13.0000 of SMCI at $39.03 USD"
        
        row1, row2 = buy_usd_stock()
        
        self.assertEqual(row1, expected_row1)
        self.assertEqual(row2, expected_row2)

    def test_sell_usd_stock(self):
        """Test if sell USD stock transaction rows are generated correctly."""
        expected_row1 = "2025-03-05, Cash(USD), 1609.00, , Sold 10.0000 of BA at $160.90 USD"
        expected_row2 = "2025-03-05, Investment(BA), , 1600.00, Sold 10.0000 of BA at $160.90 USD"
        expected_row3 = "2025-03-05, 'Realized Gain on Sale', 9.00, , Sold 10.0000 of BA at $160.90 USD"

        row1, row2, row3 = sell_usd_stock()
        
        self.assertEqual(row1, expected_row1)
        self.assertEqual(row2, expected_row2)
        self.assertEqual(row3, expected_row3)

    def test_update_invst_amounts(self):
        """Test if JSON file updates correctly after buying stocks."""
        update_invst_amounts(5, "MSFT", 300, file_path=TEST_FILE)  # Buying 5 shares of MSFT at $300

        with open(TEST_FILE, "r") as f:
            stocks = json.load(f)

        self.assertIn("MSFT", stocks)
        self.assertIn("300", stocks["MSFT"])
        self.assertEqual(stocks["MSFT"]["300"], 5)

    def test_find_credited_invst_amount(self):
        """Test if JSON file correctly finds credited investment amount after selling."""
        credited_amount = find_credited_invst_amount(7, "AAPL", file_path=TEST_FILE)

        # Expected: 5 * 150 + 2 * 140 = 750 + 280 = 1030
        self.assertEqual(credited_amount, 1030)

    @classmethod
    def tearDownClass(cls):
        """Cleanup: Remove the temporary test JSON file after running tests."""
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

if __name__ == "__main__":
    unittest.main()