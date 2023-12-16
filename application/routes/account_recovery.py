from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from application.models.send_email import send_email
from application.models.random_password import random_password
from db_handler import Database

password_reset_bp = Blueprint('forgot_password', __name__)

# Initialize the database connection
db = Database()

@password_reset_bp.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    """
    Handle the forgot password functionality.

    For GET requests, render the forgot password form.
    For POST requests, check if the provided email exists in the database.
    If the email exists, generate a temporary password, update the user's password,
    and send an email with the temporary password. Redirect to the login page.

    Returns:
        render_template or redirect: Depending on the request type and the success of the operation.
    """
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the email exists in the database
        user_data = db.find_user_by_email(email)
        print(user_data)

        if user_data:
            # Generate a temporary password
            temporary_password = random_password()

            # Update the user's password in the database with the temporary password
            if db.update_user_password(user_data['id'], temporary_password):
                # Send an email with the temporary password using the existing send_email function
                sender_email = 'info@remmittance.com'  # Update with your sender email
                subject = 'Temporary Password for Password Reset'
                message = f'<p>Your temporary password is: <b>{temporary_password}</b></p>'

                # Get the SendGrid API key from the environment
                api_key = os.getenv('email_api')

                # Send the email using the existing send_email function
                send_email(api_key, sender_email, email, subject, message)

                flash("Temporary password sent to your email. Please check your inbox.")
                return redirect(url_for('login'))

            flash("Error updating password. Please try again.")
        else:
            flash("Email not found. Please try again.")
    
    # For GET requests or unsuccessful POST requests, render the forgot password form
    return render_template('forgot_password.html')
