from pymongo import MongoClient
MONGO_URI = "mongodb+srv://sidtohan:sidd1234@cluster0.lo4whtw.mongodb.net/?retryWrites=true&w=majority"

conn = MongoClient(MONGO_URI)

try:
    conn.admin.command("Ping")
    print("Pinged database successfully")
except Exception as e:
    print(e)
