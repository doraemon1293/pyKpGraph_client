import pandas as pd
import pymongo
import datetime
import hashlib
import util

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
    row["bandwidth"] = d["bandwidth"]
    row["layer"] = d["layer"]
    myclient.close()
    return row


class Data_collector():
    def __init__(self, MONGO_CLIENT_URL, tech, data_level, time_level, start_time, end_time, project, key_values,
                 additional_kpi, conditional_kpi, agg_function, query_config):
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
        self.key_values = [int(x) if x.isdigit() else x for x in key_values]
        self.query_config = query_config

    def query_data(self):
        # todo 2g cluster
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
        self.final_df = self.trans_results_to_data_frame()
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
                   "_id": 0,
                   self.key_col: 1,
                   self.time_col: 1,
                   }
        for k in self.project:
            project[k] = 1
        for prefix in self.collection_prefix:
            for time_ in self.time_range:
                collection_name = prefix + time_.strftime(self.date_format)
                mycol = myclient[self.db_name][collection_name]
                for key_value in self.key_values:
                    # print(self.db_name, collection_name, self.key_col, repr(key_value), project)
                    for doc in mycol.find({self.key_col: key_value}, project):
                        results.append(doc)
        myclient.close()
        return results

    def trans_results_to_data_frame(self):
        res_with_cell_name = {}
        res_without_cell_name = {}
        for res in self.query_reults:
            if "Cell Name" in res:
                res_with_cell_name.setdefault((res[self.time_col], res["Cell Name"]), {})
                util.merge_dict(res_with_cell_name[res[self.time_col], res["Cell Name"]], res)
            else:
                res_without_cell_name.setdefault((res[self.time_col], res[self.key_col]), {})
                util.merge_dict(res_without_cell_name[res[self.time_col], res[self.key_col]], res)
        df = pd.DataFrame(res_with_cell_name.values())
        df1 = pd.DataFrame(res_without_cell_name.values())
        if df.empty:
            return df
        df["cell_number"]=len(df["Cell Name"].unique())

        # add bandwidth
        if self.tech == "4G" and self.time_level == "Daily":
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

        # aggregate
        if self.data_level == "Cell":
            return df
        elif self.data_level == "Site":
            agg_function = {}
            for k in df.columns:
                if k not in ("Cell Name", self.time_col, self.key_col):
                    if k in self.agg_function:
                        agg_function[k] = self.agg_function[k]
                    else:
                        agg_function[k] = lambda x: x.sum(min_count=1)
            df = df.groupby([self.time_col, self.key_col], as_index=False).agg(agg_function)
            if df1.empty:
                return df
            else:
                merged_df = df.merge(df1, how="outer", on=[self.time_col, self.key_col])
                return merged_df
            # todo cluster


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
