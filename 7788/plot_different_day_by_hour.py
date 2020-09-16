import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel("2g.xlsx", parse_dates=["DT"])
# print(df)
df["Date"] = df["DT"].dt.date
df["Date"] = pd.to_datetime(df['Date'])
df["Hour"] = df["DT"].dt.hour
tbl=pd.pivot_table(df,index=["Hour"],columns=["Date"],values=["2G PS Traffic(mb)"])
tbl.columns=tbl.columns.droplevel()
print(tbl.columns)

tbl.plot()
plt.show()
# df1 = df[df["Date"] == "2020-08-27"]
# df2 = df[df["Date"] == "2020-08-28"]
# count=1
#
#
# for title in ("2G voice volume(ERL)","2G PS Traffic(mb)"):
# # for title in ("3G voice volume(Erl)","3G PS Traffic(mb)"):
#     ax = plt.subplot(2, 1, count)
#     ax.set_title(title)
#     ax.plot(df1["Hour"], df1[title], label="08-27")
#     ax.plot(df2["Hour"], df2[title], label="08-28")
#
#     ax.set_xlabel("Hour")
#     ax.legend()
#     count+=1
#
# plt.tight_layout()
# plt.show()
