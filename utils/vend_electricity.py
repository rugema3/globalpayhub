import json
import requests
import uuid
from credentials import api_key, api_secret
from sendsms1 import send_sms

class ElectricityVend:
    def __init__(self):
        self.url_base = "https://converged-api-01.fdibiz.com/prod/trx/v1/"
        self.headers = {
            "api_key": api_key,
            "api_secret": api_secret,
        }

    def vend_electricity(self, meter, amount, customer_msisdn):
        meter = input("Please enter the meter number: ")
        amount = int(input("Please enter the amount: "))  # Convert amount to an integer
        customer_msisdn = input("Please enter the customer's mobile phone number: ")

        # Generate a unique transaction reference (trxref)
        trxref = str(uuid.uuid4())

        querystring = {
            "pdt": "electricity",
            "ep": "vend",
            "meterno": meter,
            "amount": amount,
            "customer_msisdn": customer_msisdn,
            "tstamp": "20230721180223",
            "trxref": trxref,  # Include the trxref parameter with the generated unique value
        }

        try:
            response = requests.get(self.url_base, headers=self.headers, params=querystring)
            print("Request URL:", response.url)
            print("Request Parameters:", querystring)

            # Check if the request was successful (200 OK status code)
            if response.status_code == 200:
                # Process the API response data
                api_data = response.json()
                print("API accessed successfully")
                print("API Response:", api_data)

                """
                Extract the token, customer's mobile phone number, 
                and units from the API response.
                """
                token = api_data['data']['token']
                customer_phone = api_data['data']['customer_name']
                units = api_data['data']['units']

                # Send an SMS to the customer with the electricity token and units
                sms_message = f"You purchased electricity worth {amount} RWF, " \
               "{units} KWH, your electricity token is: {token}. " \
               "Thank you for shopping with Remmittance.com"
                send_sms(customer_msisdn, sms_message, "REMMITTANCE")  

            else:
                print(f"API request failed with status code: {response.status_code}")
                print("API Response:", response.text)

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")

# Example usage:
#if __name__ == "__main__":
 #   vend_instance = ElectricityVend()
  #  vend_instance.vend_electricity()

