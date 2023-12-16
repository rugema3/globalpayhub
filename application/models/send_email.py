import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

def send_email(api_key, sender_email, recipient_email, subject, message):
    """
    Send an email using the SendGrid API.

    Parameters:
    - api_key (str): Your SendGrid API key.
    - sender_email (str): The email address from which the email will be sent.
    - recipient_email (str): The email address to which the email will be sent.
    - subject (str): The subject of the email.
    - message (str): The HTML content of the email.

    Returns:
    None: Logs success message or error message.
    """
    # Create the SendGrid client
    sg = SendGridAPIClient(api_key)

    # Create the email content
    mail_message = Mail(
        from_email=sender_email,
        to_emails=recipient_email,
        subject=subject,
        html_content=message
    )

    try:
        # Send the email
        response = sg.send(mail_message)
        logging.info(f'Success! Status code: {response.status_code}')
    except Exception as e:
        logging.error(f'Error: {str(e)}')

if __name__ == '__main__':
    # Example usage
    api_key = os.getenv('email_api')
    sender_email = 'info@remmittance.com'
    recipient_email = 'rugema61@gmail.com'
    subject = 'Testing'
    message = '<p>Now reset password can be done with no issues. I am very happy</p>'

    send_email(api_key, sender_email, recipient_email, subject, message)
