from db_handler import Database
import bcrypt
import base64


class RegistrationManager:
    """
    A class for managing user registration.

    Attributes:
        app (Flask app): The Flask application instance.
        db (Database): An instance of the Database class for database
                        interactions.
    """

    def __init__(self, app):
        """
        Initialize the RegistrationManager with Flask app and a database
        connection.

        Args:
            app (Flask app): The Flask application instance.
        """
        self.app = app
        self.db = Database()

    def register_user(self, first_name, last_name, email, phone, password):
        """
        Register a new user and store their information in the database.

        Args:
            firstname (str): User's first name.
            lastname (str): User's last name.
            email (str): User's email address.
            phone (str): User's phone number.
            password (str): User's password (plaintext).

        Returns:
            str: A registration success message or an error message.
        """
        # Check if the user already exists
        existing_user = self.db.fetch_one(
            "SELECT * FROM users WHERE email = %s", (email,))

        if existing_user:
            return "Email already in use."

        # Create a new user with the hashed password
        query = ("INSERT INTO users ("
                 "first_name, "
                 "last_name, "
                 "email, "
                 "phone, "
                 "password) "
                 "VALUES (%s, %s, %s, %s, %s)")

        params = (first_name, last_name, email, phone, password)

        success = self.db.execute_query(query, params)

        if success:
            return "Registration successful!"
        else:
            return "Registration failed. Please try again later."

    def login_user(self, email, password):
        """
        Authenticate a user's login and return a success message or an error
        message.

        Args:
            email (str): User's email address.
            password (str): User's password (plaintext).

        Returns:
            str: A login success message or an error message.
        """
        # Retrieve the user's information from the database
        query = "SELECT * FROM users WHERE email = %s"
        print(f"Executing query: {query} with email = {email}")
        user_data = self.db.fetch_one(query, (email,))

        if user_data is not None:
            if user_data.get('password', '') == password:
                return "Login successful!"
            else:
                return "Incorrect password."
        else:
            return "Email not found."

    def close_database_connection(self):
        """
        Close the database connection when it's no longer needed.
        """
        self.db.close()
