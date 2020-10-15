import pymongo
import datetime
import hashlib
import numpy as np
import util
import pandas as pd

pd.options.display.max_columns = None
pd.options.display.max_rows = None
MONGO_CLIENT_URL = "mongodb://localhost:27017/"
EP_DB_NAME = "EP"
LTE_EP_COL_NAME = "LTE_EP"


def get_bandwidth_layer(row):
    myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
    mydb = myclient[EP_DB_NAME]
    mycol = mydb[LTE_EP_COL_NAME]
    d = mycol.find_one({"_id": row["Cell Name"]})
    if d:
        row["bandwidth"] = d["bandwidth"]
        row["layer"] = d["layer"]
    else:
        row["bandwidth"] = np.nan
        row["layer"] = np.nan
    myclient.close()
    return row


class Data_collector():
    def __init__(self, MONGO_CLIENT_URL, tech, data_level, time_level, start_time, end_time, project, key_values,
                 additional_kpi, conditional_kpi, agg_function, query_config, layer, cluster):
        self.MONGO_CLIENT_URL = MONGO_CLIENT_URL
        self.tech = tech
        self.data_level = data_level
        self.time_level = time_level
        self.start_time = start_time
        self.end_time = end_time
        self.project = project
        self.additional_kpi = additional_kpi
        self.conditional_kpi = conditional_kpi
        self.agg_function = agg_function
        self.key_values = key_values
        self.query_config = query_config
        self.layer = layer
        self.cluster = cluster

    def query_data(self):
        self.set_parameters()
        for index, row in self.additional_kpi.iterrows():
            if self.tech in row["tech"] and self.data_level in row["data_level"] and self.time_level in row[
                "time_level"]:
                self.project |= set(row["Kpis"])

        # add conditional kpi
        for index, row in self.conditional_kpi.iterrows():
            if self.tech in row["tech"] and self.data_level in row["data_level"] and self.time_level in row[
                "time_level"]:
                self.project |= set(row["Kpis"])

        self.query_reults = self.query_database()
        self.ori_dfs = self.trans_results_to_data_frame()
        self.final_df = self.aggregation()
        return self.final_df

    def set_parameters(self):
        # set time_col / time_range /date_format
        df = self.query_config
        df = df.set_index(["tech", "data_level", "time_level"])
        row = df.loc[self.tech, self.data_level, self.time_level]
        self.key_col = row["key_col"]
        self.db_name = row["db_name"]
        self.collection_prefix = row["collection_prefix"].split(",")
        self.time_col = row["time_col"]
        self.date_format = row["date_format"]
        self.time_range = pd.date_range(start=self.start_time, end=self.end_time, freq=row["freq"])
        if self.time_level == "Hourly":
            self.gp = 3600
        if self.time_level == "Daily":
            self.gp = 3600 * 24

    def query_database(self):
        myclient = pymongo.MongoClient(self.MONGO_CLIENT_URL)
        results = []
        # results_hash_set = set()
        project = {"Cell Name": 1,
                   "TRXNo": 1,
                   "_id": 0,
                   self.key_col: 1,
                   self.time_col: 1,
                   "Slot No_": 1,
                   "Port No": 1
                   }
        for k in self.project:
            project[k] = 1
        for prefix in self.collection_prefix:
            for time_ in self.time_range:
                collection_name = prefix + time_.strftime(self.date_format)
                mycol = myclient[self.db_name][collection_name]
                for doc in mycol.find({self.key_col: {"$in": self.key_values}}, project):
                    results.append(doc)
        myclient.close()
        return results

    def trans_results_to_data_frame(self):
        if self.tech == "2G":
            res_with_cell_name = {}
            res_with_trx = {}
            for res in self.query_reults:
                if "TRXNo" in res:
                    res_with_trx.setdefault((res[self.time_col], res["Cell Name"], res["TRXNo"]), {})
                    util.merge_dict(res_with_trx[res[self.time_col], res["Cell Name"], res["TRXNo"]], res)
                elif "Cell Name" in res:
                    res_with_cell_name.setdefault((res[self.time_col], res["Cell Name"]), {})
                    util.merge_dict(res_with_cell_name[res[self.time_col], res["Cell Name"]], res)
                else:
                    print("2G res with error")
        elif self.tech == "4G":
            res_with_cell_name = {}
            res_with_eth = {}
            res_with_bbu = {}
            for res in self.query_reults:
                if "VS_FEGE_RxMaxSpeed" in res:
                    res_with_eth.setdefault((res[self.time_col], res["eNodeB Name"]), {})
                    util.merge_dict(res_with_eth[res[self.time_col], res["eNodeB Name"]], res)
                elif "VS_BBUBoard_CPULoad_Max" in res:
                    res_with_bbu.setdefault((res[self.time_col], res["eNodeB Name"]), {})
                    util.merge_dict(res_with_bbu[res[self.time_col], res["eNodeB Name"]], res)
                elif "Cell Name" in res:
                    res_with_cell_name.setdefault((res[self.time_col], res["Cell Name"]), {})
                    util.merge_dict(res_with_cell_name[res[self.time_col], res["Cell Name"]], res)
                else:
                    print("4G res with error")
        elif self.tech == "5G":
            res_with_cell_name = {}
            for res in self.query_reults:
                if "Cell Name" in res:
                    res_with_cell_name.setdefault((res[self.time_col], res["Cell Name"]), {})
                    util.merge_dict(res_with_cell_name[res[self.time_col], res["Cell Name"]], res)
                else:
                    print("5G res with error")

        if self.tech == "2G":
            cell_df = pd.DataFrame(res_with_cell_name.values())
            cell_df = self.fill_na_for_missing_row_ans_sort(cell_df, ["Cell Name"])
            trx_df = pd.DataFrame(res_with_trx.values())
            trx_df = self.fill_na_for_missing_row_ans_sort(trx_df, ["Cell Name", "TRXNo"])
            return {"cell_df": cell_df, "trx_df": trx_df}
        elif self.tech == "4G":
            cell_df = pd.DataFrame(res_with_cell_name.values())
            cell_df = self.fill_na_for_missing_row_ans_sort(cell_df, ["Cell Name"])
            eth_df = pd.DataFrame(res_with_eth.values())
            eth_df = self.fill_na_for_missing_row_ans_sort(eth_df, ["eNodeB Name", "Port No"])
            bbu_df = pd.DataFrame(res_with_bbu.values())
            bbu_df = self.fill_na_for_missing_row_ans_sort(bbu_df, ["eNodeB Name", "Slot No_"])
            return {"cell_df": cell_df, "eth_df": eth_df, "bbu_df": bbu_df}
        elif self.tech == "5G":
            cell_df = pd.DataFrame(res_with_cell_name.values())
            cell_df = self.fill_na_for_missing_row_ans_sort(cell_df, ["Cell Name"])
            return {"cell_df": cell_df}

    def aggregation(self):
        if self.data_level == "Cluster":
            for df in self.ori_dfs.values():
                df["Cluster"] = self.cluster

        df = self.ori_dfs["cell_df"]
        if df.empty:
            return df

        # add cell number
        df["cell_number"] = len(df["Cell Name"].unique())

        # add bandwidth
        if self.tech == "4G":
            df = df.apply(get_bandwidth_layer, axis=1)

        # add additional kpi
        for index, row in self.additional_kpi.iterrows():
            if self.tech in row["tech"] and self.data_level in row["data_level"] and self.time_level in row[
                "time_level"]:
                df[row["kpi_name"]] = eval(row["Formula"])
                # if row["kpi_name"]=="DL_Spec_Eff_den":
                #     print(df["DL_Spec_Eff_den"],df['L_Thrp_Time_Cell_DL(s)'],df['L_ChMeas_PRB_DL_Used_Avg'],
                #     df['bandwidth'])

        # add gp
        df["GP"] = self.gp

        # add conditional kpi
        for index, row in self.conditional_kpi.iterrows():
            if self.tech in row["tech"] and self.data_level in row["data_level"] and self.time_level in row[
                "time_level"]:
                df.loc[df[row["condition_kpi"]] == row["condition_value"], row["kpi_name"]] = eval(row["Formula"])
        if self.data_level=="Cluster":
            self.key_col = "Cluster"
        # aggregate
        if self.data_level == "Cell":
            if self.tech == "2G":
                trx_df = self.ori_dfs["trx_df"]
                df1 = self.agg_df(trx_df)
                return self.merge_df(df, df1)
            else:
                return df
        else:
            if self.data_level == "Site" or self.data_level=="Cluster":
                if self.tech == "2G":
                    df = self.agg_df(df)
                    trx_df = self.ori_dfs["trx_df"]
                    trx_df = self.agg_df(trx_df)
                    return self.merge_df(df, trx_df)

                elif self.tech == "4G":
                    if self.data_level=="Site" and self.layer != "All Site":
                        df = df[df["layer"] == self.layer]
                    df = self.agg_df(df)
                    eth_df = self.ori_dfs["eth_df"]
                    eth_df = self.agg_df(eth_df)
                    bbu_df = self.ori_dfs["bbu_df"]
                    bbu_df = self.agg_df(bbu_df)
                    df = self.merge_df(df, eth_df)
                    df = self.merge_df(df, bbu_df)
                    return df
                elif self.tech == "5G":
                    df = self.agg_df(df)
                    return df

    def fill_na_for_missing_row_ans_sort(self, df, key_cols):
        if df.empty:
            return df
        else:
            df1 = df[key_cols].drop_duplicates()
            df1["temp_key"] = 1
            df2 = pd.DataFrame(self.time_range, columns=[self.time_col])
            df2["temp_key"] = 1
            df12 = df1.merge(df2, how="outer")
            df = df.merge(df12, how="outer")
            df = df.sort_values(by=self.time_col)
            df.drop(columns="temp_key")
            return df

    def agg_df(self, df):
        if df.empty:
            return df
        agg = {}
        for k in df.columns:
            if k not in ("Cell Name", "Site Name", "eNodeB Name", "gNodeB Name", "Date", "Time", "layer", "Cluster"):
                if k in self.agg_function:
                    agg[k] = self.agg_function[k]
                else:
                    agg[k] = lambda x: x.sum(min_count=1)
        df = df.groupby([self.time_col, self.key_col], as_index=False).agg(agg)
        df.sort_values(by=self.time_col, inplace=True)
        return df

    def merge_df(self, df, df1):
        if df.empty or df1.empty:
            return df
        merged_df = df.merge(df1, how="outer", on=[self.time_col, self.key_col])
        merged_df.sort_values(by=self.time_col, inplace=True)
        return merged_df

    # def sort_if_not_empty(self, df):
    #     if not df.empty:
    #         df.sort_values(by=self.time_col, inplace=True)


if __name__ == "__main__":
    additional_kpi = pd.read_excel("template.xlsx", sheet_name="additional_kpi")
    additional_kpi = additional_kpi.apply(util.compile_formula_in_df, axis=1)

    conditional_kpi = pd.read_excel("template.xlsx", sheet_name="conditional_kpi")
    conditional_kpi = conditional_kpi.apply(util.compile_formula_in_df, axis=1)

    query_config = pd.read_excel("template.xlsx", sheet_name="query_config")
    agg_function = pd.read_excel("template.xlsx", sheet_name="agg_function")
    d = {}
    for _, row in agg_function.iterrows():
        kpi_name, agg = row["kpi_name"], row["agg"]
        kpi_name = kpi_name.replace(".", "_")
        d[kpi_name] = agg
    agg_function = d
    db_operator = Data_collector(MONGO_CLIENT_URL="mongodb://localhost:27017/",
                                 tech="4G", data_level="Site", time_level="Daily",
                                 agg_function=agg_function,
                                 additional_kpi=additional_kpi,
                                 conditional_kpi=conditional_kpi,
                                 start_time=datetime.datetime(2020, 7, 23),
                                 end_time=datetime.datetime(2020, 7, 24),
                                 project={"L_Thrp_Time_Cell_DL(s)",
                                          "L_Thrp_Time_Cell_UL(s)",
                                          "L_ChMeas_PRB_DL_Used_Avg",
                                          "L_ChMeas_PRB_UL_Used_Avg",
                                          "L_ChMeas_PUSCH_MCS_29", "L_IRATHO_E2G_ExecAttOut",
                                          "L_Voice_UL_EVSSWB_Increase_Times", "VS_FEGE_TxMeanSpeed(bit/s)"},
                                 key_values=[75117],
                                 query_config=query_config,
                                 )
    db_operator.query_data()
    print(db_operator.final_df)
