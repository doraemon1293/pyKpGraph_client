import re
import openpyxl
import matplotlib.pyplot as plt
import pandas as pd
# df=pd.DataFrame([[1,2,3],
#                  [10,20,1],
#                  [5,3,1]],columns=["A","B","C"])
# print(df[["A","B"]])
#
# print(df.sort_values(by="A"))



# wb = openpyxl.load_workbook("template.xlsx")
# p = re.compile(r"\['([^()]+)(\([^()]+\))'\]")
#
# # for ws_name in ("HUAWEI5G_Hourly_tab", "HUAWEI5G_Daily_tab", "HUAWEI4G_Daily_tab", "HUAWEI4G_Hourly_tab"):
# for ws_name in ("todoHUAWEI2G_Hourly_tab",):
#     ws = wb[ws_name]
#     row0 = next(ws.rows)
#     for i in range(len(row0)):
#         if row0[i].value == "Formula":
#             break
#     cols = ws.columns
#     for _ in range(i + 1):
#         col = next(cols)
#     for cell in col:
#         s = cell.value
#         if type(s)==str:
#             s1,number = p.subn(r"['\1']", s)
#             if number>0:
#                 cell.value = s1
# wb.save("1.xlsx")
# # s="sum(['L.Thrp.bits.UL(bit)'])/sum(['L.Thrp.Time.UL(ms)'])/1000"
# # p=re.compile(r"\['([^()]+)(\([^()]+\))'\]")
# # for m in p.finditer(s):
# #     print(s[m.span()[0]:m.span()[1]])
# #     print(m.pos)
# #     print(m.endpos)
# # s1=p.subn(r"['\1']",s)
# # print(s1)
import pandas as pd
import datetime
import matplotlib.dates as mdates

t=737718.1
x=mdates.num2date(t)
print(x.day,x.hour)


print("x:{}".format(1))