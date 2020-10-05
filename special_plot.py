import matplotlib
import numpy as np
import matplotlib.ticker as mtick


def base_function(legends, labels, k1s, k2s, format_string, data_df, ax, left_unit):
    df = data_df
    width = 0.8 / len(legends)
    arrs = [[] for _ in range(len(k1s))]
    x = np.arange(len(labels)) - 0.5 * 0.8 + 0.5 * width
    for i, k1 in enumerate(k1s):
        for k2 in k2s:
            kw = format_string.format(k1, str(k2))
            val = df[kw].sum()
            arrs[i].append(val)
    for i in range(len(arrs)):
        arrs[i] = [x / sum(arrs[i]) * (100 if left_unit=="%" else 1) for x in arrs[i]]
        ax.bar(x, arrs[i], width, label=legends[i])
        x += width
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylabel(left_unit)


def DL_UL_UE_Thr_Distr_Ovrall(data_df, ax, left_unit):
    legends = ["DL", "UL"]
    labels = ["0-1", "1-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-50", "50-100",
              "100-200", "200-500", "500-1000", ">1000"]
    k1s = ["DL", "UL"]
    k2s = range(15)
    format_string = "N_Thp_{}_Samp_Index{}"
    base_function(legends, labels, k1s, k2s, format_string, data_df, ax, left_unit)


def MCS_Distr_Overall(data_df, ax, left_unit):
    legends = ["PDSCH", "PUSCH"]
    labels = list(range(29))
    k1s = ["PDSCH", "PUSCH"]
    k2s = list(range(29))
    format_string = "N_ChMeas_{}_MCS_{}"
    base_function(legends, labels, k1s, k2s, format_string, data_df, ax, left_unit)

