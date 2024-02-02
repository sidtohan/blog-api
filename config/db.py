# Dotenv
from dotenv import dotenv_values

# Pymongo
from pymongo import MongoClient
config = dotenv_values(".env")
MONGO_URI = config["MONGODB_URI"]

conn = MongoClient(MONGO_URI)

try:
    conn.admin.command("Ping")
    print("Pinged database successfully")
except Exception as e:
    print(e)
