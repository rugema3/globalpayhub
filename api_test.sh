#!/bin/bash

# Set your Bearer Token
BEARER_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1NmM5YTEyZi1kMDhlLTQ3MzctYTQ0NS02MDgwY2JmMzhlOWMiLCJpYXQiOjE3MDE3NjUxNjUsIm5iZiI6MTcwMTc2NTE2NSwianRpIjoiYmFhNGUzNDQtZWJmNi00Mzg2LTgzNGEtMDAyMjdkM2QyMDc0IiwiZXhwIjoxNzAxODUxNTY1LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOnRydWUsInNvdXJjZSI6IkFQSSIsImFnZW50X2lkIjoiMGZiOGMyMDEtMDgxYi00M2JiLTljNWUtZWIwZTQ1Yjg5MTU0IiwibG9jYXRpb25faWQiOiIwOWU4ZTcyNC04ZTFjLTQ2YWYtOWQ0OC03NTA4NjBmNzY4M2IiLCJuYW1lIjoiQVBJX2ZkaSIsInJvbGVzIjpbImFjY291bnRfYWRtaW4iXX0.T_BPiwb9Lmz0GgZT0YG1FU8hxv-GWpvjP7yOACPuZS4"

# API Endpoint
API_ENDPOINT="https://sb-api.efashe.com/rw/v2/vend/validate"

# Request data
REQUEST_DATA='{"verticalId": "airtime", "customerAccountNumber": "0781049931"}'

# Print debug information
#echo "Bearer Token: $BEARER_TOKEN"
#echo "API Endpoint: $API_ENDPOINT"
#echo "Request Data: $REQUEST_DATA"

# Make the Curl request
curl -X POST "$API_ENDPOINT" \
     -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $BEARER_TOKEN" \
     -d "$REQUEST_DATA"

