import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables from .env file
load_dotenv()

# Retrieve database connection parameters from environment variables
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

# Create a connection
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor
cursor = conn.cursor(dictionary=True)

# Execute the query
query = "SELECT usd_amount FROM electricamount"
cursor.execute(query)

# Fetch and print the results as plain float values
results = cursor.fetchall()
usd_amounts = [float(row['usd_amount']) for row in results]
print(usd_amounts)

# Close the cursor and connection
cursor.close()
conn.close()

