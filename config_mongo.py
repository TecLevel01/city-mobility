from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["cityMobility"]

# Collections
users_col = db["users"]
stations_col = db["stations"]
trips_col = db["trips"]

print("Connected successfully to MongoDB")
