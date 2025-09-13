from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://localhost:27017/"

client = MongoClient(uri,server_api=ServerApi('1'))

db = client.assessment_db
collection = db["employees"]
collection.create_index("employee_id", unique=True)