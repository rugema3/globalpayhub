# Import the AirtimeVending class and other necessary libraries
from buy_airtime import AirtimeVending

# Function to get user input for airtime vending
def get_user_input():
    customer_msisdn = input("Enter the customer's mobile number: ")
    amount = float(input("Enter the amount to top up: "))

    return customer_msisdn, amount

# Get user input
customer_msisdn, amount = get_user_input()

# Create an instance of the AirtimeVending class with the specified amount
airtime_vending = AirtimeVending(amount)

# Call vend_airtime method
response = airtime_vending.vend_execute(customer_msisdn)

# Print the result
print("Vend Airtime Result:")
print(response)
