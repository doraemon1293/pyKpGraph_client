import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange,AutoDateFormatter, AutoDateLocator
)
import numpy as np
import datetime


# Fixing random state for reproducibility
np.random.seed(19680801)


# tick every 5th easter
# rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
# loc = RRuleLocator(rule)
formatter = DateFormatter('%m/%d/%y')
# date1 = datetime.date(2020, 1, 10)
# date2 = datetime.date(2020, 1, )
delta = datetime.timedelta(days=1)

dates1 = drange(datetime.date(2020, 1, 1), datetime.date(2020, 1, 7), delta)
s1=np.random.randint(low=1,high=100,size=len(dates1))  # make up some random y values

dates2 = drange(datetime.date(2020, 1, 5), datetime.date(2020, 1, 11), delta)
s2=np.random.randint(low=1,high=100,size=len(dates2))  # make up some random y values

fig, ax = plt.subplots()

# ax.xaxis.set_major_locator(loc)
ax.set_xlim(datetime.date(2019, 12, 10),datetime.date(2020, 1, 11))
# ax.xaxis.set_major_formatter(formatter)
# ax.xaxis.set_tick_params(rotation=30, labelsize=10)
# ax.set_xticks(drange(datetime.date(2020, 1, 1),datetime.date(2020, 1, 11), delta))
xtick_locator = AutoDateLocator()
xtick_formatter = AutoDateFormatter(xtick_locator)

ax = plt.axes()
ax.xaxis.set_major_locator(xtick_locator)
ax.xaxis.set_major_formatter(xtick_formatter)
ax.bar(dates1,s1)
ax.bar(dates2,s2)
plt.tight_layout()
plt.show()