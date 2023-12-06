import requests
import json
from datetime import datetime

# API base URL
base_url = "https://sb-api.efashe.com/rw/v2"

# Replace with your actual API key and secret
api_key = {
    "api_key": "74b165e8-a955-4727-854d-0e241ec93adf",
    "api_secret": "be5d7e36-ff9c-4d85-b527-2e4f022ec194",
}

def get_access_token(api_key):
    url = f"{base_url}/auth/token"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "apiKey": api_key["api_key"],
        "apiSecret": api_key["api_secret"],
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def is_token_expired(expires_at):
    expiration_time = datetime.fromisoformat(expires_at)
    current_time = datetime.now()
    return current_time >= expiration_time

def perform_authenticated_request(url, method="GET", data=None):
    global api_key

    if is_token_expired(api_key["accessTokenExpiresAt"]):
        # If access token is expired, refresh it
        refresh_response = get_access_token(api_key)
        api_key = refresh_response["data"]

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key['accessToken']}",
    }

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    return response.json()

# Function to perform vend validation
def vend_validate(api_key, vertical_id, customer_account_number):
    url = f"{base_url}/vend/validate"
    data = {
        "verticalId": vertical_id,
        "customerAccountNumber": customer_account_number,
    }

    return perform_authenticated_request(url, method="POST", data=data)

# Function to perform vend execution
def vend_execute(api_key, trx_id, customer_account_number, amount, vertical_id, delivery_method, deliver_to, callback):
    url = f"{base_url}/vend/execute"
    data = {
        "trxId": trx_id,
        "customerAccountNumber": customer_account_number,
        "amount": amount,
        "verticalId": vertical_id,
        "deliveryMethodId": delivery_method,
        "deliverTo": deliver_to,
        "callBack": callback,
    }

    return perform_authenticated_request(url, method="POST", data=data)

if __name__ == "__main__":
    # Replace with your actual values
    vertical_id = "airtime"
    customer_account_number = "0781049931"

    # Perform vend validation
    validate_response = vend_validate(api_key, vertical_id, customer_account_number)
    print("Validation Response:")
    print(json.dumps(validate_response, indent=2))

    # Extract the dynamic trxId from the validation response
    trx_id = validate_response.get("data", {}).get("trxId", "")
    delivery_method = validate_response.get("data", {}).get("deliveryMethods", [{}])[0].get("id", "")
    deliver_to = validate_response.get("data", {}).get("deliverTo", "")
    callback = validate_response.get("data", {}).get("callback", "")
    amount = 100

    # Perform vend execution with the dynamic trxId
    execute_response = vend_execute(api_key, trx_id, customer_account_number, amount, vertical_id, delivery_method, deliver_to, callback)
    print("Execution Response:")
    print(json.dumps(execute_response, indent=2))

