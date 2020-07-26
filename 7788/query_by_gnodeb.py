import pandas as pd
import datetime
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.mydatabase
collection = db["NR_CELLS_HOURLY"]
for doc in collection.find({"Cell Name": "95021NCn781", "Time": datetime.datetime(2020, 4, 26, 0, 0)}):
    print(doc)
