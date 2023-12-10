import requests
import json
from access_token import get_token  # Import the get_token function

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
        return get_token()  # Call the get_token function to obtain the access token

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
            # If the request returns unauthorized, refresh the access token and retry
            self.access_token = self.generate_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.get(url, headers=headers) if method == "GET" else requests.post(url, headers=headers, json=data)

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

        return self.perform_authenticated_request(url, method="POST", data=data)

    def vend_execute(self, trx_id, customer_account_number, amount, vertical_id, delivery_method, deliver_to, callback):
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

        return self.perform_authenticated_request(url, method="POST", data=data)

    def convert_to_local_currency(self, usd_amount):
        """
        Converts the given USD amount to the local currency.

        Parameters:
            usd_amount (float): The amount in USD to be converted.

        Returns:
            float: The equivalent amount in the local currency.

        Raises:
            ValueError: If the conversion for the given USD amount is not found in the amount_list.
        """
        # Replace this with your actual conversion logic using the amount_list or any other method
        amount_list = {
            0.1: 100,
            0.2: 220,
            1.00: 1100,
            5.00: 5500,
            8.00: 88000,
            10.00: 11000,
            15.00: 16500,
            20.00: 22000
        }
        local_amount = amount_list.get(usd_amount)
        if local_amount is None:
            raise ValueError(f"Amount for {usd_amount} USD not found.")

        return local_amount

if __name__ == "__main__":
    # Replace with your actual values
    base_url = "https://sb-api.efashe.com/rw/v2"

    # Create an instance of Airtime
    airtime = ServiceVendor(base_url, api_key, api_secret)

    # Replace with your actual values
    vertical_id = "airtime"
    customer_account_number = "0781049931"

    # Perform vend validation
    validate_response = airtime.vend_validate(vertical_id, customer_account_number)
    print("Validation Response:")
    print(json.dumps(validate_response, indent=2))

    # Extract the dynamic trxId from the validation response
    trx_id = validate_response.get("data", {}).get("trxId", "")
    delivery_method = validate_response.get("data", {}).get("deliveryMethods", [{}])[0].get("id", "")
    deliver_to = validate_response.get("data", {}).get("deliverTo", "")
    callback = validate_response.get("data", {}).get("callback", "")
    amount = 200

    # Perform vend execution with the dynamic trxId
    execute_response = airtime.vend_execute(trx_id, customer_account_number, amount, vertical_id, delivery_method, deliver_to, callback)
    print("Execution Response:")
    print(json.dumps(execute_response, indent=2))

