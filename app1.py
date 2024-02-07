#!/usr/bin/env python3
from flask import Flask, render_template, request, flash
from flask import url_for, session, redirect
from application.models.service_vendor import ServiceVendor
from paypal_handler import PayPalHandler
from credentials import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET
import secrets
import os
from dotenv import load_dotenv
from application.models.registration import RegistrationManager
from db_handler import Database
from decimal import Decimal
from application.routes.account_recovery import password_reset_bp
from application.decorators.login_decorator import login_required
# Load environment variables from .env
load_dotenv()

# Check if the required environment variables are set
if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
    raise ValueError("PayPal credentials are not set. Please set "
                     "PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET "
                     "in the credentials.py file.")

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = secrets.token_hex(32)  # Generate a random secret key

app.register_blueprint(password_reset_bp)

base_url = os.getenv("AIRTIME_BASE_URL")
api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")

vertical_id = "airtime"

# Create instances of ServiceVendor and PayPalHandler
airtime = ServiceVendor(base_url, api_key=api_key, api_secret=api_secret)
paypal_handler = PayPalHandler(
    PAYPAL_MODE,
    PAYPAL_CLIENT_ID,
    PAYPAL_CLIENT_SECRET
)
# Initialize the database connection
db = Database()

# Create an instance of RegistrationManager with app and db
registration_manager = RegistrationManager(app)

# Define the exchange rate from USD to RWF.
exchange_rate = 1150

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
    api_key = os.environ.get('maps_api')
    return render_template('contact.html', api_key=api_key)


@app.route('/terms')
def terms():
    """The route for terms and conditions page."""
    return render_template('terms_and_conditions.html')

@app.route('/privacy')
def privacy():
    """The route for privacy policy."""
    return render_template('privacy_policy.html')

@app.route('/vend_airtime', methods=['GET', 'POST'])
def vend_airtime():
    """
    Handle the initiation of airtime transaction.

    If the request method is POST, retrieves user input from the form,
    performs vend validation, extracts necessary information for PayPal
    payment, and saves transaction information in the session.
    Then, renders a template showing the transaction details.

    For GET requests, renders the 'vend_airtime.html' template.

    Returns:
    - render_template: Renders either the transaction details template or
        the 'vend_airtime.html' template.
    """
    # Define transaction fees dictionary
    transaction_fees = {
        5: 1.79,
        6: 1.89,
        8: 1.99,
        10: 2.19,
        12: 2.29,
        15: 2.58,
        17: 2.77,
        20: 3.17,
        30: 3.49,
    }

    if request.method == 'POST':
        # Get the user's input from the form
        customer_account_number = request.form['customer_account_number']
        usd_amount = float(request.form['usd_amount'])
        local_currency = request.form['local_currency']
        print(f"The local currency is: {local_currency}")

        # Extract transaction fee based on the selected amount
        amount = int(usd_amount)
        fee = transaction_fees.get(amount, 0.0)
        total = fee + amount

        vertical_id = 'airtime'

        # Perform vend validation
        validate_response = airtime.vend_validate(
            vertical_id, customer_account_number)

        # Extract necessary information for PayPal payment
        trx_id = validate_response.get("data", {}).get("trxId", "")
        delivery_method = validate_response.get(
            "data", {}).get(
            "deliveryMethods", [
                {}])[0].get(
                "id", "")
        deliver_to = validate_response.get("data", {}).get("deliverTo", "")
        callback = validate_response.get("data", {}).get("callback", "")
        customer_name = validate_response.get("data", {}).get("customerAccountNumber", "")
        product_name = validate_response.get("data", {}).get("pdtName", "")


        # Save necessary information in session for later use in the execute
        # route
        session['transaction_info'] = {
            'trx_id': trx_id,
            'customer_account_number': customer_account_number,
            'usd_amount': usd_amount,
            'local_currency': local_currency,
            'transaction_fee': fee,
            'total': total,
            'vertical_id': vertical_id,
            'delivery_method': delivery_method,
            'deliver_to': deliver_to,
            'callback': callback,
            'customer_name' : customer_name,
            'product_name' : product_name,
        }

        # Render a template showing the transaction details
        return render_template(
            'transaction_details.html',
            transaction_info=session['transaction_info'])

    # Use the dictionary keys for electric_amounts
    airtime_amounts = list(transaction_fees.keys())
    fees = list(transaction_fees.values())

    local_currency = [amount * exchange_rate for amount in airtime_amounts]


    # Render the vend_tv.html template for GET requests
    return render_template('vend_airtime.html', airtime_amounts=airtime_amounts, local_currency=local_currency)

# Vend Electricity route
@app.route('/vend_electricity', methods=['GET', 'POST'])
def vend_electricity():
    """
    Handle the initiation of an electricity transaction.

    If the request method is POST, retrieves user input from the form,
    performs vend validation, extracts necessary information for PayPal
    payment, and saves transaction information in the session.
    Then, creates a PayPal payment and redirects the user to PayPal for payment.

    For GET requests, renders the 'vend_electricity.html' template.

    Returns:
    - redirect: Redirects to PayPal for payment if the request method is POST.
    - render_template: Renders the 'vend_electricity.html' template for GET requests.
    """

    # Define transaction fees dictionary
    transaction_fees = {
        5: 1.79,
        6: 1.89,
        8: 1.99,
        10: 2.19,
        12: 2.29,
        15: 2.58,
        17: 2.77,
        20: 3.17,
        30: 3.49,
    }

    if request.method == 'POST':
        # Get the user's input from the form
        customer_account_number = request.form['customer_account_number']
        usd_amount = request.form['usd_amount']
        local_currency = request.form['local_currency']
        print(f"The local currency is: {local_currency}")

        # Extract transaction fee based on the selected amount
        amount = int(usd_amount)
        fee = transaction_fees.get(amount, 0.0)
        total = fee + amount

        vertical_id = 'electricity'

        # Perform vend validation
        validate_response = airtime.vend_validate(
            vertical_id, customer_account_number)

        # Extract necessary information for PayPal payment
        trx_id = validate_response.get("data", {}).get("trxId", "")
        delivery_method = validate_response.get(
            "data", {}).get(
            "deliveryMethods", [
                {}])[0].get(
                "id", "")
        deliver_to = validate_response.get("data", {}).get("deliverTo", "")
        callback = validate_response.get("data", {}).get("callback", "")
        customer_name = validate_response.get("data", {}).get("customerAccountNumber", "")
        product_name = validate_response.get("data", {}).get("pdtName", "")

        # Save necessary information in session for later use in the execute route
        session['transaction_info'] = {
            'trx_id': trx_id,
            'customer_account_number': customer_account_number,
            'usd_amount': usd_amount,
            'local_currency': local_currency,
            'transaction_fee': fee,  
            'total': total,
            'vertical_id': vertical_id,
            'delivery_method': delivery_method,
            'deliver_to': deliver_to,
            'callback': callback,
            'customer_name' : customer_name,
            'product_name' : product_name,
        }

        # Render a template showing the transaction details
        return render_template(
            'transaction_details.html',
            transaction_info=session['transaction_info'])

    # Use the dictionary keys for electric_amounts
    electric_amounts = list(transaction_fees.keys())
    fees = list(transaction_fees.values())

    local_currency = [amount * exchange_rate for amount in electric_amounts]

    # Render the vend_electricity.html template for GET requests
    return render_template('vend_electricity.html', electric_amounts=electric_amounts, local_currency=local_currency)

@app.route('/pay_tv_subscription', methods=['GET', 'POST'])
def pay_tv():
    """
    Handle the initiation of a TV transaction.

    If the request method is POST, retrieves user input from the form,
    performs vend validation, extracts necessary information for PayPal
    payment, and saves transaction information in the session.
    Then, renders a template showing the transaction details.

    For GET requests, renders the 'vend_tv.html' template.

    Returns:
    - render_template: Renders either the transaction details template or
        the 'vend_tv.html' template.
    """
    # Define transaction fees dictionary
    transaction_fees = {
        5: 1.79,
        6: 1.89,
        8: 1.99,
        10: 2.19,
        12: 2.29,
        15: 2.58,
        17: 2.77,
        20: 3.17,
        30: 3.49,
    }

    if request.method == 'POST':
        # Get the user's input from the form
        customer_account_number = request.form['customer_account_number']
        usd_amount = float(request.form['usd_amount'])
        local_currency = request.form['local_currency']
        print(f"The local currency is: {local_currency}")

        # Extract transaction fee based on the selected amount
        amount = int(usd_amount)
        fee = transaction_fees.get(amount, 0.0)
        total = fee + amount

        vertical_id = 'paytv'

        # Perform vend validation
        validate_response = airtime.vend_validate(
            vertical_id, customer_account_number)

        # Extract necessary information for PayPal payment
        trx_id = validate_response.get("data", {}).get("trxId", "")
        delivery_method = validate_response.get(
            "data", {}).get(
            "deliveryMethods", [
                {}])[0].get(
                "id", "")
        deliver_to = validate_response.get("data", {}).get("deliverTo", "")
        callback = validate_response.get("data", {}).get("callback", "")
        customer_name = validate_response.get("data", {}).get("customerAccountNumber", "")
        product_name = validate_response.get("data", {}).get("pdtName", "")


        # Save necessary information in session for later use in the execute
        # route
        session['transaction_info'] = {
            'trx_id': trx_id,
            'customer_account_number': customer_account_number,
            'usd_amount': usd_amount,
            'local_currency': local_currency,
            'transaction_fee': fee,
            'total': total,
            'vertical_id': vertical_id,
            'delivery_method': delivery_method,
            'deliver_to': deliver_to,
            'callback': callback,
            'customer_name' : customer_name,
            'product_name' : product_name,
        }

        # Render a template showing the transaction details
        return render_template(
            'transaction_details.html',
            transaction_info=session['transaction_info'])

    # Use the dictionary keys for electric_amounts
    tv_amounts = list(transaction_fees.keys())
    fees = list(transaction_fees.values())

    local_currency = [amount * exchange_rate for amount in tv_amounts]


    # Render the vend_tv.html template for GET requests
    return render_template('vend_tv.html', tv_amounts=tv_amounts, local_currency=local_currency)

@app.route('/vend_tax', methods=['GET', 'POST'])
def vend_tax():
    """
    Handle the initiation of tax transaction.

    If the request method is POST, retrieves user input from the form,
    performs vend validation, extracts necessary information for PayPal
    payment, and saves transaction information in the session.
    Then, creates a PayPal payment and redirects the user to PayPal 4 payment

    For GET requests, renders the 'vend_tax.html' template.

    Returns:
    - redirect: Redirects to PayPal for payment if the request method is POST.
    - render_template: Renders the 'vend_tax.html' template 4 GET requests
    - render_template: Renders an error template if an exception occurs during
                        transaction initiation.
    """

    if request.method == 'POST':
        try:
            # Get the user's input from the form
            customer_account_number = request.form['customer_account_number']

            vertical_id = 'tax'

            # Perform vend validation
            validate_response = airtime.vend_validate(
                vertical_id, customer_account_number)
            print(f'response: {validate_response}')

            # Extract necessary information for PayPal payment
            trx_id = validate_response.get("data", {}).get("trxId", "")
            delivery_method = validate_response.get(
                "data", {}).get(
                "deliveryMethods", [
                    {}])[0].get(
                "id", "")
            deliver_to = validate_response.get("data", {}).get("deliverTo", "")
            callback = validate_response.get("data", {}).get("callback", "")
            extra_info = validate_response.get("data", {}).get("extraInfo", {})
            vend_max_amount = validate_response.get("data", {}).get("vendMax", "")
            usd_amount = round(vend_max_amount / exchange_rate, 2)

            # Calculate the transaction fee. 4% of the taxes to be paid
            transaction_fee = round(usd_amount * 0.04, 2)
            print(f'extra_info: {extra_info}')
            tax_payer = validate_response.get("data", {}).get("customerAccountNumber", "")
            total = usd_amount + transaction_fee
            local_currency = vend_max_amount
            
            # Extract information from extra_info
            tax_center = extra_info.get("tax_center", "")
            dec_date = extra_info.get("dec_date", "")
            is_full_pay = extra_info.get("is_full_pay", "")
            tax_type = extra_info.get("tax_type", "")
            tin = extra_info.get("tin", "")

            # Save necessary information in session for later use in the
            # execute route
            session['transaction_info'] = {
                'trx_id': trx_id,
                'customer_account_number': customer_account_number,
                'usd_amount': usd_amount,
                'vertical_id': vertical_id,
                'delivery_method': delivery_method,
                'deliver_to': deliver_to,
                'callback': callback,
                'extra_info': extra_info,
                'transaction_fee': transaction_fee,
                'vend_max_amount': vend_max_amount,
                'tin': tin,
                'tax_type': tax_type,
                'dec_date': dec_date,
                'tax_center':tax_center,
                'tax_payer': tax_payer,
                'total': total,
                'local_currency': local_currency
            }
            

            # Render a template showing the transaction details
            return render_template(
            'transactions.html',
            transaction_info=session['transaction_info'])
            print(f'Transaction_info: {transaction_info}')

        except Exception as e:
            # Print the error for debugging
            print(f"An error occurred in vend_tax route: {str(e)}")
    
    # Render the vend-airtime.html template for GET requests
    return render_template('vend_tax.html')


@app.route('/complete_transaction', methods=['POST'])
#@login_required
def complete_transaction():
    """
    Handle the completion of a transaction.

    Retrieves transaction information from the session, including user and
    payment details, performs any additional logic if needed, creates a
    PayPal payment, and redirects the user to PayPal for payment.

    Returns:
    - redirect: Redirects to PayPal for payment after completing necessary
                steps.
    - render_template: Renders an error template if transaction information is
                        not found in session.
    """
    transaction_info = session.get('transaction_info')

    if transaction_info is None:
        return render_template(
            'error.html',
            error_message='Transaction information not found in session.')

    # Retrieve additional information as needed for PayPal payment
    usd_amount = float(transaction_info['usd_amount']) + transaction_info['transaction_fee']

    #transaction_info['transaction_fee']
    print(usd_amount)
    print(type(usd_amount))
    print(transaction_info['transaction_fee'])
    print(type((transaction_info['transaction_fee'])))
    customer_account_number = transaction_info['customer_account_number']

    # Create a PayPal payment and get the redirect URL
    paypal_redirect_url = paypal_handler.create_payment(
        usd_amount, customer_account_number, request)

    # Redirect the user to PayPal for payment
    return redirect(paypal_redirect_url)


# Execute payment route
@app.route('/execute_payment', methods=['GET', 'POST'])
def execute_payment():
    """
    Handle the execution of a payment and vend operation.

    Retrieves necessary information from the session, including transaction
    details, executes the PayPal payment, and performs vend execution based on
    the transaction information.

    Returns:
    - render_template: Success or error template based on the execution result.
    """
    # Retrieve necessary information from session
    transaction_info = session.get('transaction_info')
    print(transaction_info)

    if transaction_info is None:
        return render_template(
            'error.html',
            error_message='Transaction information not found in session.')

    # Extract necessary information for vend execution
    trx_id = transaction_info['trx_id']
    customer_account_number = transaction_info['customer_account_number']
    usd_amount = transaction_info['usd_amount']
    local_currency = float(transaction_info['local_currency']) 
    vertical_id = transaction_info['vertical_id']
    delivery_method = transaction_info['delivery_method']
    deliver_to = transaction_info['deliver_to']
    callback = transaction_info['callback']

    print(f"trx_id: {trx_id}")
    print(f"delivery_method: {delivery_method}")

    # Execute the PayPal payment
    success, error_message = paypal_handler.execute_payment(
        request.args.get('paymentId'), request.args.get('PayerID'))

    if success:
        # Perform vend execution with the retrieved information
        execute_response = airtime.vend_execute(
            trx_id,
            customer_account_number,
            local_currency,
            vertical_id,
            delivery_method,
            deliver_to,
            callback)
        print(f"execute_response: {execute_response}")

        return render_template(
            'success.html',
            execute_response=execute_response)
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
        registration_manager = RegistrationManager(
            app)  # Pass your Flask app and db object
        result = registration_manager.register_user(
            first_name, last_name, email, phone, password)

        if result == "Registration successful!":
            flash('Registration successful.', 'success')
        else:
            flash('Registration failed. Please try again.', 'danger')

        # Close the database connection
        registration_manager.close_database_connection()

    return render_template('register.html')


from flask import redirect, url_for, request

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login requests."""
    if request.method == 'POST':
        # Get user login data from the form
        email = request.form['email']
        password = request.form['password']

        # Use the RegistrationManager to authenticate the user
        registration_manager = RegistrationManager(app)
        result = registration_manager.login_user(email, password)

        if result == "Login successful!":
            flash('Login successful. Welcome!', 'success')

            # Redirect the user back to the original page or a default page
            next_url = request.args.get('next') or url_for('home')
            print(f"Redirecting to: {next_url}") # check the redirection url
            return redirect(next_url)

        else:
            flash('Login failed. Please check your email and password.', 'danger')

        # Close the database connection
        registration_manager.close_database_connection()

    return render_template('login.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
