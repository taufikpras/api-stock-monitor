from pandas import DataFrame
from pymongo.mongo_client import MongoClient
from pymongo import DESCENDING
import yfinance as yf
from datetime import datetime
from bson import ObjectId
from models.database import price_db

def updateData(code, timeframe, db=price_db):
    latest_date: str = "2014-01-01"
    update_data: DataFrame

    collection_name = code+"-"+timeframe

    try:
        list_of_collections = db.list_collection_names()
        
        db_collection = db[collection_name]
        if(collection_name in list_of_collections):
            date_: datetime
            latest_data = db_collection.find().sort('Date',DESCENDING).limit(1)[0]
            _id = str(latest_data['_id'])
            date_ = latest_data['Date']
            latest_date = date_.strftime('%Y-%m-%d')
            db_collection.find_one_and_delete({"_id": ObjectId(_id)})

        update_data = yf.download(code+".JK", start=latest_date, interval=timeframe, progress=False)
        
        update_data.reset_index(inplace=True)

        update_data_dict = update_data.to_dict('records')

        db_collection.insert_many(update_data_dict)

        return True
    except Exception as e:
        print(e)
        return False

def readData(code, timeframe, db=price_db):
    collection_name = code+"-"+timeframe
    
    try:
        list_of_collections = db.list_collection_names()
        
        db_collection = db[collection_name]

        if(collection_name not in list_of_collections):
            updateData(code,timeframe,db)

        data_from_db = db_collection.find()
        items_df = DataFrame(data_from_db)
        items_df = items_df.drop(columns=["_id"] ,axis=1).set_index("Date")
        items_df["string_date"] = items_df.index.strftime('%Y-%m-%d')

        return items_df
    except Exception as e:
        print(e)
        return False

def readLatestPrice(code, timeframe = "1d"):
    df = readData(code, timeframe)

    return df.tail(1).to_dict('records')[0]
    