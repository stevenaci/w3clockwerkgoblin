from pymongo import MongoClient

client = MongoClient()

client = MongoClient("localhost", 27017)

dev_db = client["clock_werk"]

test_db = client["clock_test"]

def get_db():
    return test_db