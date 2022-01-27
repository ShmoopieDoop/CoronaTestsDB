import pymongo
import os

mongo_client = pymongo.MongoClient(
    f"mongodb+srv://ShmoopieDoop:{os.environ.get('MONGO_USER_PASSWORD')}@cluster0.ylm9c.mongodb.net/testLocations?retryWrites=true&w=majority"
)
db = mongo_client["testLocations"]
colec = db["testLocations"]
