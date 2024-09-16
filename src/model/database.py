from pymongo.mongo_client import MongoClient
import os

MONGO_HOST = "mongo-stock"
MONGO_USER = "root"
MONGO_PASS = "1234qweR"
MONGO_PORT = "27017"
if(os.environ.get("MONGO_HOST") != None):
    MONGO_HOST = str(os.environ.get("MONGO_HOST"))
if(os.environ.get("MONGO_USER") != None):
    MONGO_USER = str(os.environ.get("MONGO_USER"))
if(os.environ.get("MONGO_PASS") != None):
    MONGO_PASS = str(os.environ.get("MONGO_PASS"))
if(os.environ.get("MONGO_PORT") != None):
    MONGO_PORT = str(os.environ.get("MONGO_PORT"))


MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"

client = MongoClient(MONGO_URL)

db = client.stock
price_db = client.stock_prices_db
