# Dotenv
from os import getenv
from dotenv import load_dotenv

# Pymongo
from pymongo import MongoClient

load_dotenv()
MONGO_URI = getenv("MONGODB_URI")

conn = MongoClient(MONGO_URI)

try:
    conn.admin.command("Ping")
    print("Pinged database successfully")
except Exception as e:
    print(e)
