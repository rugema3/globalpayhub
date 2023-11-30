import requests
import uuid
from datetime import datetime
from credentials import access_token, AIRTIME_URL

class AirtimeVending:
    def __init__(self, price_list):
        self.price_list = price_list

    def vend_validate(self, vertical_id, customer_account_number):
        payload = {
            "verticalId": vertical_id,
            "customerAccountNumber": customer_account_number
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.post(AIRTIME_URL + "/vend/validate", json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

            return response.json()

        except requests.RequestException as e:
            return f"Error: {e}"

    def vend_execute(self, trx_id, customer_account_number, amount, vertical_id, delivery_method_id, deliver_to, callback):
        payload = {
            "trxId": trx_id,
            "customerAccountNumber": customer_account_number,
            "amount": amount,
            "verticalId": vertical_id,
            "deliveryMethodId": delivery_method_id,
            "deliverTo": deliver_to,
            "callBack": callback
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.post(AIRTIME_URL + "/vend/execute", json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

            return response.json()

        except requests.RequestException as e:
            return f"Error: {e}"

    def vend_trx_status(self, trx_id):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.get(AIRTIME_URL + f"/vend/{trx_id}/status", headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

            return response.json()

        except requests.RequestException as e:
            return f"Error: {e}"
