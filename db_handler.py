import os
import mysql.connector
from dotenv import load_dotenv
from typing import List


class Database:
    """
    A class for handling database operations using MariaDB.
    """

    def __init__(self):
        """
        Initialize the database connection using configuration from .env file.
        """
        load_dotenv()  # load the environment variables
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME')

        if not (host and user and password and database):
            raise ValueError(
                "Database configuration not found in the .env file.")

        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def close(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.conn.close()

    def execute_query(self, query, params=None):
        """
        Execute a SQL query.

        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to be used with the query.

        Returns:
            bool: True if the query was executed successfully, False otherwise.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            self.conn.rollback()
            return False

    def fetch_one(self, query, params=None):
        """
        Execute a SQL query and fetch a single row.

        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to be used with the query.

        Returns:
            dict: A dictionary representing a single row from the result.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            self.conn.rollback()
            return None

    def fetch_all(self, query, params=None):
        """
        Execute a SQL query and fetch all rows.

        Args:
            query (str): The SQL query to execute.
            params (tuple): A tuple of parameters to be used with the query.

        Returns:
            list: A list of dictionaries representing rows from the result.
        """
        try:
            self.execute_query(query, params)
            result = self.cursor.fetchall()
            print(f"Executed query: {query} with parameters: {params}")
            return result
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return []


    def find_user_by_email(self, email):
        """
        Find a user in the database by their email address.

        Args:
            email (str): The email address of the user to search for.

        Returns:
            User: The User object if found, or None if not found.
        """
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        user_data = self.cursor.fetchone()

        if user_data:
            return user_data
        else:
            return None

    def update_user_password(self, user_id, new_password):
        """
        Update the user's password in the database.

        Args:
            user_id (int): The ID of the user whose password needs to be
                            updated.
            new_password (str): The new password for the user.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = "UPDATE users SET password = %s WHERE id = %s"
        params = (new_password, user_id)

        return self.execute_query(query, params)

    def get_electricity_amounts(self):
        """
        Retrieve electricity amounts from the database.

        Returns:
            List[dict]: A list of dictionaries representing electricity amounts.
        """
        query = "SELECT * FROM electricamount"
        try:
            return self.fetch_all(query)
        except Exception as e:
            print(f"Error fetching electricity amounts: {str(e)}")
            return []
