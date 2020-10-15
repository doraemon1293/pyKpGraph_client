import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import matplotlib.dates as mdates

def make_format(current, other):
    # current and other are axes
    def format_coord(x, y):
        # x, y are data coordinates
        # convert to display coords
        display_coord = current.transData.transform((x,y))
        inv = other.transData.inverted()
        # convert back to data coords with respect to ax
        ax_coord = inv.transform(display_coord)
        y2=ax_coord[1]
        y1=y
        x=mdates.num2date(x)
        return ('x={}-{}-{}, y1={:.3f}, y2={:.3f}'.format(x.month,x.day,x.hour,y1,y2))
    return format_coord

np.random.seed(6)
numdata = 10
t = np.linspace(0.05, 0.11, numdata)
y1 = np.cumsum(np.random.random(numdata) - 0.5) * 40000
y2 = np.cumsum(np.random.random(numdata) - 0.5) * 0.002

fig = plt.figure()

ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

ax2.format_coord = make_format(ax2, ax1)
x=pd.date_range(start=datetime.datetime.today(),periods=10,freq="H")
ax1.plot(x, y1, 'r-', label='y1')
ax2.plot(x, y2, 'g-', label='y2')

plt.show()