import unittest
from unittest.mock import patch
from app import AirtimeVending

class TestAirtimeVending(unittest.TestCase):
    def setUp(self):
        # Sample price list for testing
        self.price_list = {
            0.1: 100,
            0.2: 220,
            1.00: 1100,
            5.00: 5500,
            8.00: 88000,
            10.00: 11000,
            15.00: 16500,
            20.00: 22000
        }
        self.airtime_vending = AirtimeVending(self.price_list)

    def test_successful_airtime_vending(self):
        # Simulate a successful API response
        with patch('requests.request') as mock_request:
            mock_request.return_value.text = '{"status": "success", "data": {"trxid": "12345"}}'
            response = self.airtime_vending.vend_airtime("1234567890", 10.00)
        self.assertIn("status", response)
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)
        self.assertIn("trxid", response["data"])

    def test_unsuccessful_airtime_vending_api_error(self):
        # Simulate an API error response
        with patch('requests.request') as mock_request:
            mock_request.return_value.text = '{"status": "error", "message": "API error"}'
            with self.assertRaises(requests.exceptions.RequestException):
                self.airtime_vending.vend_airtime("1234567890", 5.00)

    def test_invalid_customer_msisdn(self):
        # Test with an invalid customer MSISDN (empty string)
        with self.assertRaises(ValueError):
            self.airtime_vending.vend_airtime("", 10.00)

    def test_invalid_airtime_amount(self):
        # Test with an invalid airtime amount (negative amount)
        with self.assertRaises(ValueError):
            self.airtime_vending.vend_airtime("1234567890", -5.00)

    def test_large_airtime_amount(self):
        # Test with a large airtime amount
        with patch('requests.request') as mock_request:
            mock_request.return_value.text = '{"status": "success", "data": {"trxid": "12345"}}'
            response = self.airtime_vending.vend_airtime("1234567890", 10000.00)
        self.assertIn("status", response)
        self.assertEqual(response["status"], "success")
        self.assertIn("data", response)
        self.assertIn("trxid", response["data"])

if __name__ == "__main__":
    unittest.main()

