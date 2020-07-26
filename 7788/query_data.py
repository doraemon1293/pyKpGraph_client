import pandas as pd
import pymongo
import datetime
import pyqtgraph as pg



def query_data(MONGO_CLIENT_URL, DB_NAME, COLLECTIONS_NAME, query, projection):
    my_client = pymongo.MongoClient(MONGO_CLIENT_URL)
    my_database = my_client[DB_NAME]
    my_col = my_database[COLLECTIONS_NAME]

    docs = list(my_col.find(query, projection))
    my_client.close()
    return docs



