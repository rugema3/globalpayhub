import requests
from credentials import credentials, sms_url

def send_sms(recipient_number, message, sender):
    url = sms_url

    # Read the username and password from the credentials dictionary
    username = credentials["username"]
    password = credentials["password"]

    data = {
            "recipients": recipient_number,
            "message": message,
            "sender": sender
            }
    # Make a POST request to the API with the data and authentication included
    response = requests.post(url, data=data, auth=(username, password))
    # Process the response as needed
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Request failed with status code:", response.status_code)
    
# Usage example:
#recipient_number = input("Enter the recipient number(s) (comma-separated): ")
#message = input("Enter the message: ")
#sender = input("Enter the sender: ")

#send_sms(recipient_number, message, sender)

