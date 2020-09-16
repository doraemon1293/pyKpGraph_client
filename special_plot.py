import matplotlib
import numpy as np
import matplotlib.ticker as mtick


def bas_function(legends, labels, k1s, k2s, format_string, data_df, ax, percent):
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
        arrs[i] = [x / sum(arrs[i]) * (100 if percent else 1) for x in arrs[i]]
        ax.bar(x, arrs[i], width, label=legends[i])
        x += width
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels)


def DL_UL_UE_Thr_Distr_Ovrall(data_df, ax, percent):
    legends = ["DL", "UL"]
    labels = ["0-1", "1-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-50", "50-100",
              "100-200", "200-500", "500-1000", ">1000"]
    k1s = ["DL", "UL"]
    k2s = range(15)
    format_string = "N_Thp_{}_Samp_Index{}"
    bas_function(legends, labels, k1s, k2s, format_string, data_df, ax, percent)


def MCS_Distr_Overall(data_df, ax, percent):
    legends = ["PDSCH", "PUSCH"]
    labels = list(range(29))
    k1s = ["PDSCH", "PUSCH"]
    k2s = list(range(29))
    format_string = "N_ChMeas_{}_MCS_{}"
    bas_function(legends, labels, k1s, k2s, format_string, data_df, ax, percent)


def TA_Dist_Overall(data_df, ax, percent):
    legends = ["TA Shares"]
    labels = ["0-78m", "78-156m", "156-312m", "312-546m", "546-1014m", "1-1.8km", "1.8-3.4km", "3.4-7.2km",
              "7.2-15.0km", "15.0-30.6km", "30.6-57.9km", "57.9-100km", ">100km"]
    k1s = [""]
    k2s = list(range(13))
    format_string = "{}N_RA_TA_UE_Index{}"
    bas_function(legends, labels, k1s, k2s, format_string, data_df, ax, percent)
