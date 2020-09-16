import pandas as pd
import pymongo
import datetime
import hashlib
import util

pd.options.display.max_columns = None
pd.options.display.max_rows = None


def calc_bandwidth(row):
    return 20


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
                        # # remove duplicate
                        # h = get_hash_val(doc)
                        # if h in results_hash_set:
                        #     print("{} in {} is removed".format(doc["_id"], collection_name))
                        #     print("removed doc is".format(doc))
                        #     mycol.remove_one({"_id": doc["_id"]})
                        # else:
                        #     results_hash_set.add(h)
                        #     doc={[(for k in self.project]}
                        # if self.tech == "4G" and self.time_level == "Daily":
                        #     # todo add bandwidth for 4G/daily
                        #     if "Cell Name" in doc:
                        #         doc["bandwidth"] = 20
                        #         if doc["bandwidth"] == 20:
                        #             doc["UL_Thr_target"] = 0.5
                        #             doc["DL_Thr_target"] = 8
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

        # add bandwidth
        if self.tech == "4G" and self.time_level == "Daily":
            df["bandwidth"] = df.apply(lambda row: calc_bandwidth(row), axis=1)

        # add additional kpi
        for index, row in self.additional_kpi.iterrows():
            if self.tech in row["tech"] and self.data_level in row["data_level"] and self.time_level in row[
                "time_level"]:
                df[row["kpi_name"]] = eval(row["Formula"])

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
    # if "Hourly" in tab1_name:
    #     time_col = "Time"
    #     GP = 3600
    #     st = self.start_date_time_edit.dateTime().toPyDateTime()
    #     end = self.end_date_time_edit.dateTime().toPyDateTime()
    #     if tab1_name.startswith("HUAWEI5G"):
    #         collection_name = "NR_CELLS_HOURLY"
    # if "Daily" in tab1_name:
    #     time_col = "Date"
    #     GP = 3600 * 24
    #     st = self.start_date_edit.dateTime().toPyDateTime()
    #     end = self.end_date_edit.dateTime().toPyDateTime()
    #     if tab1_name.startswith("HUAWEI5G"):
    #         collection_name = "NR_CELLS_DAILY"
    #
    # if query_level == "cell":
    #     column_name = "Cell Name"
    #     column_value = self.cell_line_edit.text().strip()
    #
    # if query_level == "site":
    #     if tab1_name.startswith("HUAWEI5G"):
    #         column_name = "gNodeB Name"  # todo need to consider 2/3/4G
    #         column_value = self.site_line_edit.text().strip()  # todo need to consider 2/3/4G
    # # todo cluster
    #
    # myclient = pymongo.MongoClient(MONGO_CLIENT_URL)
    # col = myclient[db_name][collection_name]
    #
    # project[time_col] = 1
    # project[column_name] = 1
    # query = {column_name: column_value,
    #          time_col: {"$gte": st, "$lte": end}}
    # res = list(col.find(query, project))
    # if res:
    #     df = pd.DataFrame(res)
    #     df["GP"] = GP
    #     if query_level == "site":
    #         for kpi in set(agg):
    #             if kpi not in df.columns:
    #                 del agg[kpi]
    #                 print("missing {} in databse for {}".format(kpi, column_value))
    #         df = df.groupby([time_col, column_name], as_index=False).agg(agg)
    #
    #     for tab2_name in self.charts_config.get(tab1_name, {}):
    #         sc = tab1.findChild(mpl_cls.ScrollaleChartsArea, tab2_name)
    #         configs = self.charts_config[tab1_name][tab2_name]
    #         sc.plot(configs, df, GP, column_value, time_col, self.special_legend_title)
    #     self.statusbar.showMessage("{} {} query finished".format(column_value, tab1_name, 60000))
    # else:
    #     self.statusbar.showMessage("{} doesn't have data".format(column_value))
    #     # todo cluster
    # myclient.close()
