import re
import hashlib
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


