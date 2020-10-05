# trans source formula into correct format
import openpyxl
import re
wb = openpyxl.load_workbook("source_formula.xlsx")
ws = wb.active
write_wb = openpyxl.Workbook()
write_ws = write_wb.active
for row in ws.rows:
    tab = row[0].value
    chart_no = row[1].value
    chart_title = row[2].value
    s = row[7].value if row[7].value else ""
    s = s.replace("\n", "").replace("\r", "")
    print("s",s)
    arr = re.split(r",(?!\d)",s)
    print("arr",arr)

    for x in arr:
        x = x.strip()
        if x:
            print("*",x)
            if " as " in x:
                formula, kpi_name = x.split(" as ")
                formula = formula.strip()
                kpi_name = kpi_name.strip()
            elif " AS " in x:
                formula, kpi_name = x.split(" AS ")
                formula = formula.strip()
                kpi_name = kpi_name.strip()
            elif " As " in x:
                formula, kpi_name = x.split(" As ")
                formula = formula.strip()
                kpi_name = kpi_name.strip()
            else:
                formula = x
                kpi_name = None
            write_ws.append([tab, chart_no, chart_title, kpi_name, None, None, None, formula])
write_wb.save("2.xlsx")
