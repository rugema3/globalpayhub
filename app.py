#!/usr/bin/env python3
"""
Define airtime_vending1.py.

Description:

This module provides the main Flask application 
for airtime vending with PayPal integration.

Usage:
    python3 airtime_vending1.py

"""
from flask import Flask, render_template, request, flash, redirect, url_for, session
# from flask import Flask, render_template, request, redirect
from paypal_handler import PayPalHandler
from vend_airtime import AirtimeVending, price_list
from utils.vend_electricity import ElectricityVend  # Import ElectricityVend class
from credentials import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET
from registration import RegistrationManager
from db_handler import Database
from passlib.hash import sha256_crypt

import os

# Check if the required environment variables are set
if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
    raise ValueError("PayPal credentials are not set. Please set "
                     "PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET "
                     "in the credentials.py file.")

app = Flask(__name__, static_url_path='/static')

# Set a secret key
app.secret_key = os.urandom(24)

# Initialize the database connection
db = Database()

# Create an instance of RegistrationManager with app and db
registration_manager = RegistrationManager(app)


paypal_handler = PayPalHandler(PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
airtime_vending = AirtimeVending(price_list)
electricity_vend = ElectricityVend()

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home route for the Flask application.

    Returns:
        str: If the request method is POST, returns either a redirect to PayPal or an error message.
             If the request method is GET, returns the home page with the price list.
    """
    if request.method == 'POST':
        # Add your POST request logic here
        customer_msisdn = request.form['customer_msisdn']
        usd_amount = float(request.form['amount'])
        print("Received POST request:")
        print(f"Customer MSISDN: {customer_msisdn}")
        print(f"USD Amount: {usd_amount}")

        # Map the USD price to the equivalent local currency price using the dictionary
        local_amount = airtime_vending.price_list.get(usd_amount)
        print(f"Local Amount: {local_amount}")

        if local_amount is None:
            return "Invalid amount selected."

        # Create PayPal payment with the selected local currency amount
        redirect_url = paypal_handler.create_payment(usd_amount, customer_msisdn, request)
        print(f"Redirect URL: {redirect_url}")


        if redirect_url is not None:
            # Store the selected USD and local currency amounts to display on the page
            selected_usd_amount = usd_amount
            selected_local_amount = local_amount

            return redirect(redirect_url)

        return "Error creating PayPal payment."

    return render_template('index1.html', price_list=airtime_vending.price_list)

@app.route('/execute_payment')
def execute_payment():
    """
    Execute payment route for the Flask application.

    Returns:
        str: If the payment execution is successful, returns the result
             page with the API response.
             If there is an error in payment execution, returns an error message.
    """
    payer_id = request.args.get('PayerID')
    payment_id = request.args.get('paymentId')

    response = paypal_handler.execute_payment(payment_id, payer_id)

    if response[0]:  # Success
        usd_amount = float(request.args.get('amount'))
        local_amount = airtime_vending.price_list.get(usd_amount)
        if local_amount is None:
            return "Invalid amount selected."

        api_response = airtime_vending.vend_airtime(request.args.get('customer_msisdn'), local_amount)  # Pass local currency amount
        return render_template('result.html', api_response=api_response, selected_usd_amount=usd_amount, selected_local_amount=local_amount)
    else:
        return "Error executing payment: " + response[1]

@app.route('/electricity_vend', methods=['GET', 'POST'])
def electricity_vend_route():
    """
    Route for electricity vending in the Flask application.

    Returns:
        str: If the request method is POST, returns the API response from electricity vending.
             If the request method is GET, returns a simple HTML form to input electricity vending details.
    """
    if request.method == 'POST':
        # Add your electricity_vend_route route logic here
        meter = request.form['meter']
        amount = int(request.form['amount'])
        customer_msisdn = request.form['customer_msisdn']

        # Vend electricity using the ElectricityVend instance
        api_response = electricity_vend.vend_electricity(meter, amount, customer_msisdn)

        # Return the API response
        return api_response

    # If the request method is GET, return the HTML form for input
    return render_template('electricity_vend_form.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration requests."""
    if request.method == 'POST':
        # Get user registration data from the form
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Use the RegistrationManager to register the user
        registration_manager = RegistrationManager(app)  # Pass your Flask app and db object
        result = registration_manager.register_user(first_name, last_name, email, phone, password)

        if result == "Registration successful!":
            flash('Registration successful. You can now log in.', 'success')
            flash('Registration successful. You can now log in.', 'success')
        else:
            flash('Registration failed. Please try again.', 'danger')

        # Close the database connection
        registration_manager.close_database_connection()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login requests."""
    if request.method == 'POST':
        # Get user login data from the form
        email = request.form['email']
        password = request.form['password']

        # Print the email and password to check if they are received correctly
        print(f"Received email: {email}")
        print(f"Received password: {password}")

        # Use the RegistrationManager to authenticate the user
        registration_manager = RegistrationManager(app)
        
        # Print messages for debugging
        print("Before login attempt")

        result = registration_manager.login_user(email, password)

        # Print messages for debugging
        print(f"Login result: {result}")

        if result == "Login successful!":
            flash('Login successful. Welcome!', 'success')
            # Add your logic to redirect to the user's profile or dashboard
        else:
            flash('Login failed. Please check your email and password.', 'danger')

        # Close the database connection
        registration_manager.close_database_connection()

    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

