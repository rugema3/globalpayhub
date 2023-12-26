import requests
import json
from .access_token import get_token  # Import the get_token function


class ServiceVendor:
    """
    A class for vending airtime using the provided API.
    """

    def __init__(self, base_url, api_key, api_secret):
        """
        Initialize the Airtime instance.

        Parameters:
        - base_url (str): The base URL of the vending API.
        - api_key (str): The API key used for authentication.
        - api_secret (str): The API secret used for authentication.
        """
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = self.generate_access_token()

    def generate_access_token(self):
        """
        Generate an access token using the provided API key and API secret.

        Returns:
        - str: The obtained access token.
        """
        return get_token()  # Return token as a value.

    def perform_authenticated_request(self, url, method="GET", data=None):
        """
        Perform an authenticated request to the API.

        Parameters:
        - url (str): The URL for the request.
        - method (str): The HTTP method (GET or POST).
        - data (dict): The request payload for POST requests.

        Returns:
        - dict: The JSON response from the API.
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.status_code == 401:
            self.access_token = self.generate_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.get(
                url, headers=headers) if method == "GET" else requests.post(
                url, headers=headers, json=data)

        return response.json()

    def vend_validate(self, vertical_id, customer_account_number):
        """
        Perform vend validation.

        Parameters:
        - vertical_id (str): The service/product vertical unique identifier.
        - customer_account_number (str): The account number for the customer.

        Returns:
        - dict: The JSON response from the vend validation.
        """
        url = f"{self.base_url}/vend/validate"
        data = {
            "verticalId": vertical_id,
            "customerAccountNumber": customer_account_number,
        }

        return self.perform_authenticated_request(
            url, method="POST", data=data)

    def vend_execute(
            self,
            trx_id,
            customer_account_number,
            amount,
            vertical_id,
            delivery_method,
            deliver_to,
            callback):
        """
        Perform vend execution.

        Parameters:
        - trx_id (str): The transaction ID from the vend validation response.
        - customer_account_number (str): The account number for the customer.
        - amount (float): The transaction amount.
        - vertical_id (str): The service/product vertical unique identifier.
        - delivery_method (str): The delivery method for the transaction.
        - deliver_to (str): The delivery destination for the transaction.
        - callback (str): The callback URL for asynchronous processing.

        Returns:
        - dict: The JSON response from the vend execution.
        """
        url = f"{self.base_url}/vend/execute"
        data = {
            "trxId": trx_id,
            "customerAccountNumber": customer_account_number,
            "amount": amount,
            "verticalId": vertical_id,
            "deliveryMethodId": delivery_method,
            "deliverTo": deliver_to,
            "callBack": callback,
        }

        return self.perform_authenticated_request(
            url, method="POST", data=data)

    def calculate_transaction_fee(self, usd_amount, fee_percentage=3.49, fixed_fee=0.49):
        """
        Calculate the transaction fee based on the PayPal fee structure.

        Args:
            usd_amount (float): The original USD amount.
            fee_percentage (float): The PayPal fee percentage.
            fixed_fee (float): The fixed PayPal fee.

        Returns:
            float: The calculated transaction fee.
        """
        fee_percentage /= 100.0
        transaction_fee = fee_percentage * usd_amount + fixed_fee
        return transaction_fee


    def calculate_profit_margin(self, usd_amount, minimum_profit=1.0, maximum_profit=3.0):
        """
        Calculate the profit margin based on the desired range.

        Args:
            usd_amount (float): The original USD amount.
            minimum_profit (float): The minimum profit amount.
            maximum_profit (float): The maximum profit amount.

        Returns:
            float: The calculated profit margin.
        """
        profit_margin = min(maximum_profit, max(minimum_profit, usd_amount * 0.1))  # 10% profit margin
        return profit_margin

    def calculate_local_currency_amount(self, usd_amount, exchange_rate=1200.0):
        """
        Convert the original USD amount to local currency based on the exchange rate.

        Args:
            usd_amount (float): The original USD amount.
            exchange_rate (float): The exchange rate.

        Returns:
            float: The local currency amount.
        """
        local_currency_amount = usd_amount * exchange_rate
        return local_currency_amount

    def handle_electricity_transaction(self, customer_account_number, usd_amount):
        """
        Handle an electricity transaction, including fee and profit calculations.

        Args:
            customer_account_number (str): The customer's account number.
            usd_amount (float): The original USD amount.

        Returns:
            dict: The result of the electricity transaction.
        """
        # Perform vend validation and other necessary steps
        validate_response = self.vend_validate("electricity", customer_account_number)
        # Extract necessary information for PayPal payment
        trx_id = validate_response.get("data", {}).get("trxId", "")
        delivery_method = validate_response.get("data", {}).get("deliveryMethods", [{}])[0].get("id", "")
        deliver_to = validate_response.get("data", {}).get("deliverTo", "")
        callback = validate_response.get("data", {}).get("callback", "")

        # Calculate transaction fee and profit margin
        transaction_fee = self.calculate_transaction_fee(usd_amount)
        profit_margin = self.calculate_profit_margin(usd_amount)

        # Calculate total amount (USD + transaction fee + profit)
        total_amount_usd = usd_amount + transaction_fee + profit_margin

        # Calculate local currency amount before fees and profit
        local_currency_amount_before_fees = self.calculate_local_currency_amount(usd_amount)

        # Perform vend execution with the retrieved information
        execute_response = self.vend_execute(
            trx_id, customer_account_number, total_amount_usd,
            "electricity", delivery_method, deliver_to, callback)

        return {
            "transaction_fee": transaction_fee,
            "profit_margin": profit_margin,
            "local_currency_amount_before_fees": local_currency_amount_before_fees,
            "execute_response": execute_response
        }



if __name__ == "__main__":
    # Replace with your actual values
    base_url = "https://sb-api.efashe.com/rw/v2"

    # Create an instance of Airtime
    airtime = ServiceVendor(base_url, api_key, api_secret)

    # Replace with your actual values
    vertical_id = "airtime"
    customer_account_number = "0781049931"

    # Perform vend validation
    validate_response = airtime.vend_validate(
        vertical_id, customer_account_number)
    print("Validation Response:")
    print(json.dumps(validate_response, indent=2))

    # Extract the dynamic trxId from the validation response
    trx_id = validate_response.get("data", {}).get("trxId", "")
    delivery_method = validate_response.get(
        "data", {}).get(
        "deliveryMethods", [
            {}])[0].get(
                "id", "")
    deliver_to = validate_response.get("data", {}).get("deliverTo", "")
    callback = validate_response.get("data", {}).get("callback", "")
    amount = 200

    # Perform vend execution with the dynamic trxId
    execute_response = airtime.vend_execute(
        trx_id,
        customer_account_number,
        amount,
        vertical_id,
        delivery_method,
        deliver_to,
        callback)
    print("Execution Response:")
    print(json.dumps(execute_response, indent=2))
