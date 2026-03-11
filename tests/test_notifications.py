import os
import sys
import unittest

# Add the parent directory and mcp-tools directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(os.path.join(parent_dir, "mcp-tools"))

from tools import list_contracts, get_contract_metadata, get_notifications, ACTIVITY_LOG_FILE

class TestNotifications(unittest.TestCase):
    def setUp(self):
        # Clear the log file if it exists
        if os.path.exists(ACTIVITY_LOG_FILE):
            os.remove(ACTIVITY_LOG_FILE)

    def test_logging(self):
        # Call some tools
        list_contracts()
        get_contract_metadata("contract_1.pdf")

        # Check notifications
        notifications = get_notifications()
        self.assertEqual(len(notifications), 2)
        self.assertIn("Listed all contracts.", notifications[0])
        self.assertIn("Extracted metadata for contract_1.pdf.", notifications[1])

if __name__ == "__main__":
    unittest.main()
