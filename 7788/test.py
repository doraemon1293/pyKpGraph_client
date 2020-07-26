from query_data import query_data
import pandas as pd
import pyqtgraph as pg
import datetime
from pyqtgraph.Qt import QtGui, QtCore

MONGO_CLIENT_URL = "mongodb://localhost:27017/"
DB_NAME = "mydatabase"
COLLECTIONS_NAME = "NR_CELLS_HOURLY"

query = {"Cell Name": "95021NCn781", "Time": {"$lte": datetime.datetime(2020, 4, 26, 22, 0),
                                              "$gte": datetime.datetime(2020, 4, 26, 1, )
                                              }
         }
projection = {"Cell Name": 1, "Time": 1, "N_ThpVol_DL_Cell(kbit)": 1}
arr = query_data(MONGO_CLIENT_URL, DB_NAME, COLLECTIONS_NAME, query, projection)
print(arr)

df = pd.DataFrame(arr)

win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
p1 = win.addPlot(title="Basic array plotting", x=df["Time"],y=df["N_ThpVol_DL_Cell(kbit)"])

# pg.plot(df["Time"],df["N_ThpVol_DL_Cell(kbit)"])

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()