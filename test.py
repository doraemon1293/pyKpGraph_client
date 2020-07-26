from pymongo import MongoClient
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
st = time.time()
DB_NAME = "mydatabase"
COLLECTIONS_NAMES = ["NR_CELLS_HOURLY"]
client = MongoClient()  # Remember your uri string
col = client['mydatabase']['NR_CELLS_HOURLY']
# df = pd.read_csv("1.csv",
#                  skiprows=4, skipfooter=1, parse_dates=["Time"], na_values=["NIL"])
#
# data = df.to_dict(orient='records')  # Here's our added param..
#
# for row in data:
#     col.update({"Cell Name": row["Cell Name"], "Time": row["Time"]}
#                ,{"$set":row}, upsert=True)

df = pd.DataFrame(list(col.find({"Cell Name": "99415NCn781"})))
# plt.bar(df["Time"], df["N_NsaDc_SgNB_AbnormRel"], color='green')
print(df["Time"])
print(df["N_ThpVol_DL(kbit)"])
plt.bar(df["Time"],np.random.randint(1,10,24), align="center",alpha=0.5,width=0.8/24)
plt.tight_layout()
plt.show()
