import pymongo
import re

MONGO_CLIENT_URL = "mongodb://localhost:27017/"
DB_NAME = "mydatabase"
myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
mydb = myclient[DB_NAME]
mycol = mydb["NR_CELL_NAMES"]
cell = "1"
query = {"_id": re.compile("^{}".format(cell), re.IGNORECASE)}
print(query)

for d in mycol.find(query, sort=[("_id", 1)], limit=5):
    print(d)
mycol = mydb["NR_CELLS_HOURLY"]
print(mycol.find_one({}, {"Time": 1}, sort=[("Time", -1)]))
print(mycol.find_one({}, {"Time": 1}, sort=[("Time", 1)]))
mycol = mydb["NR_CELLS_DAILY"]
print(mycol.find_one({}, {"Date": 1}, sort=[("Date", -1)]))
print(mycol.find_one({}, {"Date": 1}, sort=[("Date", 1)]))
