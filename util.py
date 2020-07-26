import re
def compile_formula(formula):
    formula=formula.strip()
    p=re.compile("\[\'([\w.-_\(\) ]+)\'\]")
    kpis=p.findall(formula)
    kpis = [kpi.replace(".", "_") for kpi in kpis]
    eval_exp=p.sub(r"df['\1']",formula)
    eval_exp=eval_exp.replace(".","_")
    eval_exp=eval_exp.replace("mean","np.mean")
    eval_exp=eval_exp.replace("sum","np.mean")

    return kpis,eval_exp

