import requests

# Use the access token obtained from the previous response
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1NmM5YTEyZi1kMDhlLTQ3MzctYTQ0NS02MDgwY2JmMzhlOWMiLCJpYXQiOjE3MDExNTcxNTksIm5iZiI6MTcwMTE1NzE1OSwianRpIjoiODYyNTcyOTQtYjY1OS00ODdlLTlmZmItNjYxMDE5OTk3OTE3IiwiZXhwIjoxNzAxMjQzNTU5LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOnRydWUsInNvdXJjZSI6IkFQSSIsImFnZW50X2lkIjoiMGZiOGMyMDEtMDgxYi00M2JiLTljNWUtZWIwZTQ1Yjg5MTU0IiwibG9jYXRpb25faWQiOiIwOWU4ZTcyNC04ZTFjLTQ2YWYtOWQ0OC03NTA4NjBmNzY4M2IiLCJuYW1lIjoiQVBJX2ZkaSIsInJvbGVzIjpbImFjY291bnRfYWRtaW4iXX0.OZQY3JstpUe48h3BAOmFqKu1mHboodPdsvBnWTTXcyw"

# Example API endpoint
api_endpoint = "https://sb-api.efashe.com/rw/v2/status"

# Set up headers with the access token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

try:
    # Make a GET request to the example endpoint
    response = requests.get(api_endpoint, headers=headers)
    response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

    print(f"Success! Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

except requests.RequestException as e:
    print(f"Error: {e}")

