import re
import hashlib
import matplotlib.dates as mdates

def compile_formula(formula):
    if type(formula)==str:
        formula=formula.replace("\n","").replace("\r","")
        formula=formula.strip()
        p=re.compile(r"\[\'([\w.\-_\(\) /]+)\'\]")
        kpis=p.findall(formula)
        if formula.startswith("mean"):
            kpis=[]
        else:
            kpis = [kpi.replace(".", "_") for kpi in kpis]

        eval_exp=p.sub(r"df['\1']",formula)
        eval_exp=eval_exp.replace(".","_")
        eval_exp=eval_exp.replace("mean","np.mean")
        eval_exp=eval_exp.replace("sum","np.mean")
    else:
        kpis=[]
        eval_exp=str(formula)
    return kpis,eval_exp

def compile_formula_in_df(row):
    row["Kpis"],row["Formula"]=compile_formula(row["Formula"])
    return row

def get_hash_val(doc):
    m = hashlib.sha256()
    for k in sorted(doc.keys()):
        if k!="_id":
            m.update(str(k).encode())
            m.update(str(doc[k]).encode())
    return m.digest()

def merge_dict(d1,d2):
    for k in d2:
        if k not in d1:
            d1[k]=d2[k]
        else:
            if d1[k]==None and d2[k]!=None:
                d1[k]=d2[k]


def make_format(ax1, ax2,time_col):
    # current and other are axes
    def format_coord(x, y):
        # x, y are data coordinates
        # convert to display coords
        ax1_display_coord = ax1.transData.transform((x,y))
        inv = ax2.transData.inverted()
        # convert back to data coords with respect to ax
        ax2_data_coord = inv.transform(ax1_display_coord)
        y1=y
        y2=ax2_data_coord[1]
        x=mdates.num2date(x)
        if time_col=="Date":
            return 'x={}.{} y1={:.3f} y2={:.3f}'.format(x.day,x.month,y1,y2)
        elif time_col=="Time":
            return 'x={}.{} {} y1={:.3f} y2={:.3f}'.format(x.day, x.month,x.hour, y1, y2)
    return format_coord