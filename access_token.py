"""This module deals with the generation of the access token."""
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

base_url = os.getenv("AIRTIME_BASE_URL")
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")


def get_token():
    """Generate access token.

    Description:
                This function generates the access token which is needed
                during the authentication of the transaction.

                I chose this approach so that every time a transaction is
                initiated, a new token will be generated and used for this
                particular transaction. this will insure that the each
                transaction is unique it its own way and no security threats.

                We need the api_key and secret to generate the token.
                These values are in the environment variable.
    """
    url = f'{base_url}/auth'
    headers = {'Content-Type': 'application/json'}
    data = {
        "api_key": api_key,
        "api_secret": api_secret
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        json_response = response.json()

        # Extract the access token from the response
        access_token = json_response.get('data', {}).get('accessToken')

        # Print the access token
        # print(f"Access Token: {access_token}")
        return access_token
    else:
        print(f"Failed to obtain access token. Status code: "
              f"{response.status_code}, Response: {response.text}")


if __name__ == '__main__':

    # I wanna test the function to see that it works before I import
    # But also making it doesn't execute when imported.
    # Call the function to test
    response = get_token()
    print(response)
