#!/usr/bin/env python3
from flask import Flask, render_template, request, flash, redirect, url_for, session
from service_vendor import ServiceVendor
from paypal_handler import PayPalHandler
from credentials import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET
import secrets
import os
from dotenv import load_dotenv
from registration import RegistrationManager
from db_handler import Database

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


# Initialize the database connection
db = Database()

# Create an instance of RegistrationManager with app and db
registration_manager = RegistrationManager(app)

# Home route
@app.route('/')
def home():
    """
    Render the home page.

    Returns:
    - render_template: Renders the 'index2.html' template for the home page.
    """
    return render_template('index2.html')

@app.route('/about')
def about():
    """The route for about us page."""
    return render_template('about.html')


@app.route('/services')
def services():
    """The route for services page."""
    return render_template('services.html')

@app.route('/contact')
def contact():
    """The route for contact page."""
    api_key = os.environ.get('google_api')
    return render_template('contact.html', api_key=api_key)

@app.route('/terms')
def terms():
    """The route for terms and conditions page."""
    return render_template('terms_and_conditions.html')


# Initiate transaction route
@app.route('/vend_airtime', methods=['GET', 'POST'])
def vend_airtime():
    """
    Handle the initiation of an airtime transaction.

    If the request method is POST, retrieves user input from the form, performs vend validation,
    extracts necessary information for PayPal payment, and saves transaction information in the session.
    Then, creates a PayPal payment and redirects the user to PayPal for payment.

    For GET requests, renders the 'initiate_transaction.html' template.

    Returns:
    - redirect: Redirects to PayPal for payment if the request method is POST.
    - render_template: Renders the 'initiate_transaction.html' template for GET requests.
    """

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

    # Render the vend-airtime.html template for GET requests
    return render_template('vend_airtime.html')


# Vend Electricity route
@app.route('/vend_electricity', methods=['GET', 'POST'])
def vend_electricity():
    """
    Handle the initiation of an electricity transaction.

    If the request method is POST, retrieves user input from the form, performs vend validation,
    extracts necessary information for PayPal payment, and saves transaction information in the session.
    Then, creates a PayPal payment and redirects the user to PayPal for payment.

    For GET requests, renders the 'vend_electricity.html' template.

    Returns:
    - redirect: Redirects to PayPal for payment if the request method is POST.
    - render_template: Renders the 'vend_electricity.html' template for GET requests.
    """

    if request.method == 'POST':
        # Get the user's input from the form
        customer_account_number = request.form['customer_account_number']
        usd_amount = float(request.form['usd_amount'])
        vertical_id = 'electricity'

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

    # Render the vend_electricity.html template for GET requests
    return render_template('vend_electricity.html')

#pay_tv route
@app.route('/pay_tv_subscription', methods=['GET', 'POST'])
def pay_tv():
    """
    Handle the initiation of a TV transaction.

    If the request method is POST, retrieves user input from the form, performs vend validation,
    extracts necessary information for PayPal payment, and saves transaction information in the session.
    Then, creates a PayPal payment and redirects the user to PayPal for payment.

    For GET requests, renders the 'vend_electricity.html' template.

    Returns:
    - redirect: Redirects to PayPal for payment if the request method is POST.
    - render_template: Renders the 'vend_electricity.html' template for GET requests.
    """

    if request.method == 'POST':
        # Get the user's input from the form
        customer_account_number = request.form['customer_account_number']
        usd_amount = float(request.form['usd_amount'])
        vertical_id = 'paytv'

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

    # Render the vend_tv.html template for GET requests
    return render_template('vend_tv.html')


# Execute payment route
@app.route('/execute_payment', methods=['GET', 'POST'])
def execute_payment():
    """
    Handle the execution of a payment and vend operation.

    Retrieves necessary information from the session, including transaction details,
    executes the PayPal payment, and performs vend execution based on the transaction information.

    Returns:
    - render_template: Success or error template based on the execution result.
    """
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

        # Additional logic can be added here if needed for both 'airtime' and 'electricity'

        return render_template('success.html', execute_response=execute_response)
    else:
        # Handle payment execution failure
        return render_template('error.html', error_message=error_message)

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
            flash('Registration successful.', 'success')
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
    app.run(host='0.0.0.0', debug=True)
