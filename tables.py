import sqlite3

# Replace with the correct path to your database file
database_path = "/home/remmittance/flaskapps/webusers.db"

# Connect to the database
connection = sqlite3.connect(database_path)

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Execute a query to fetch the table names from sqlite_master
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Display the list of table names
for table in tables:
    print(table[0])

# Close the database connection
connection.close()

