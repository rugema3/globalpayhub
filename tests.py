import os

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

print(f"DB_USER: {db_user}")
print(f"DB_PASSWORD: {db_password}")
print(f"DB_HOST: {db_host}")
print(f"DB_NAME: {db_name}")
