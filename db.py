import pymongo
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

auth_string = f"mongodb+srv://ShmoopieDoop:{os.environ.get('MONGO_USER_PASSWORD')}@cluster0.ylm9c.mongodb.net/testLocations?retryWrites=true&w=majority"
print(auth_string)
mongo_client = pymongo.MongoClient(auth_string)
db = mongo_client["testLocations"]
colec = db["testLocations"]
