"""
vend_airtime1.py

This module provides a class for performing airtime vending for a customer.

"""

import requests
import uuid
import os
from credentials import api_key, api_secret, AIRTIME_URL


class AirtimeVending:
    def __init__(self, price_list):
        """
        Initialize the AirtimeVending class.

        Args:
            price_list (dict): A dictionary mapping USD amounts to equivalent local currency amounts.
                               Example: {0.1: 100, 0.2: 220, 1.00: 1100, ...}
        """
        self.price_list = price_list

    def vend_airtime(self, customer_msisdn, amount):
        """
        Perform airtime vending for a customer.

        Args:
            customer_msisdn (str): The customer's mobile phone number.
            amount (float): The amount of airtime to be vend.

        Returns:
            str: The API response in JSON format.

        Raises:
            requests.exceptions.RequestException: If there is an error making the API request.
        """
        trxref = str(uuid.uuid4())

        querystring = {
            "pdt": "airtime",
            "ep": "vend",
            "customer_msisdn": customer_msisdn,
            "amount": amount,
            "trxref": trxref,
            "tstamp": "20230721180223",
        }

        payload = ""
        headers = {
                "api_key": api_key,
                "api_secret": api_secret
            }

        response = requests.request("GET", AIRTIME_URL, data=payload, headers=headers, params=querystring)


        return response.text

# Pricing that the customers will see and be able to buy.
price_list = {
    0.1: 100,
    0.2: 220,
    1.00: 1100,
    5.00: 5500,
    8.00: 88000,
    10.00: 11000,
    15.00: 16500,
    20.00: 22000
}

# Create an instance of the AirtimeVending class with the specified price list
airtime_vending = AirtimeVending(price_list)
