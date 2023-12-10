
import json
from service_vendor import ServiceVendor
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your actual values
base_url = "https://sb-api.efashe.com/rw/v2"
api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')

# Create an instance of ServiceVendor
airtime = ServiceVendor(base_url, api_key, api_secret)

# Generate access token
access_token = airtime.generate_access_token()

# Print the obtained access token
print(f"Access Token: {access_token}")

# Optional: You can also print the decoded payload of the access token for verification
