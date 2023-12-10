#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, session
from service_vendor import ServiceVendor
from paypal_handler import PayPalHandler
from credentials import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET
import secrets
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Check if the required environment variables are set
if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
    raise ValueError("PayPal credentials are not set. Please set "
                     "PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET "
                     "in the credentials.py file.")

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = secrets.token_hex(32)  # Generate a random secret key

base_url = os.getenv("AIRTIME_BASE_URL")
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")

vertical_id = "airtime"  

# Create instances of ServiceVendor and PayPalHandler
airtime = ServiceVendor(base_url, api_key=api_key, api_secret=api_secret)
paypal_handler = PayPalHandler(PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)

# Home route
@app.route('/')
def home():
    return render_template('index2.html')

# Initiate transaction route
@app.route('/initiate_transaction', methods=['GET', 'POST'])
def initiate_transaction():
    if request.method == 'POST':
        # Get the user's input from the form (you might want to add more validation)
        customer_account_number = request.form['customer_account_number']
        usd_amount = float(request.form['usd_amount'])

        # Perform vend validation
        validate_response = airtime.vend_validate(vertical_id, customer_account_number)

        # Extract necessary information for PayPal payment
        trx_id = validate_response.get("data", {}).get("trxId", "")
        delivery_method = validate_response.get("data", {}).get("deliveryMethods", [{}])[0].get("id", "")
        deliver_to = validate_response.get("data", {}).get("deliverTo", "")
        callback = validate_response.get("data", {}).get("callback", "")

        # Save necessary information in session for later use in the execute route
        session['transaction_info'] = {
            'trx_id': trx_id,
            'customer_account_number': customer_account_number,
            'usd_amount': usd_amount,
            'vertical_id': vertical_id,
            'delivery_method': delivery_method,
            'deliver_to': deliver_to,
            'callback': callback,
        }

        # Create a PayPal payment and get the redirect URL
        paypal_redirect_url = paypal_handler.create_payment(usd_amount, customer_account_number, request)

        # Redirect the user to PayPal for payment
        return redirect(paypal_redirect_url)

    # Render the initiate_transaction.html template for GET requests
    return render_template('initiate_transaction.html')

# Execute payment route
@app.route('/execute_payment', methods=['GET', 'POST'])
def execute_payment():
    # Retrieve necessary information from session
    transaction_info = session.get('transaction_info')

    if transaction_info is None:
        return render_template('error.html', error_message='Transaction information not found in session.')

    # Extract necessary information for vend execution
    trx_id = transaction_info['trx_id']
    customer_account_number = transaction_info['customer_account_number']
    usd_amount = transaction_info['usd_amount']
    vertical_id = transaction_info['vertical_id']
    delivery_method = transaction_info['delivery_method']
    deliver_to = transaction_info['deliver_to']
    callback = transaction_info['callback']

    print(f"trx_id: {trx_id}")
    print(f"delivery_method: {delivery_method}")

    # Execute the PayPal payment
    success, error_message = paypal_handler.execute_payment(request.args.get('paymentId'), request.args.get('PayerID'))

    if success:
        # Perform vend execution with the retrieved information
        execute_response = airtime.vend_execute(trx_id, customer_account_number, usd_amount, vertical_id, delivery_method, deliver_to, callback)
        print(f"execute_response: {execute_response}")
        return render_template('success.html', execute_response=execute_response)
    else:
        # Handle payment execution failure
        return render_template('error.html', error_message=error_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
