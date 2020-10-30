from configparser import ConfigParser
import pandas as pd
import json
import urllib.request as urlreq


class CovidReport:
    # initialize class
    def __init__(self):
        self.full_path = ""
        self.df = None
        self.output_table = None

    # read the config file and create full path of Excel file
    # config file has to be in the same folder of CovidReport.py
    def read_config(self, config_file_name, excel_file_name):
        config_object = ConfigParser()
        try:
            config_object.read(config_file_name)
            location = config_object["Local_Address"]["ExcelFile"]
            self.full_path = location + "/" + excel_file_name
        except:
            print("**Keyword used is not correct as in the config file or config file is not found**")

    # create a DataFrame from the Excel file
    def read_excel(self):
        self.df = pd.read_excel(io=self.full_path)

    # call to URL API for each pair of date & iso
    def api_request(self, date, iso):
        try:
            url = "https://covid-api.com/api/reports/"
            rsp = urlreq.urlopen(url)
            data_dict = json.loads(rsp.read())

            num_confirmed = 0
            num_deaths = 0
            num_recovered = 0
            for d1 in data_dict["data"]:
                if (date == d1["date"]) and (iso == d1["region"]["iso"]):
                    num_confirmed = num_confirmed + d1["confirmed"]
                    num_deaths = num_deaths + d1["deaths"]
                    num_recovered = num_recovered + d1["recovered"]
            return num_confirmed, num_deaths, num_recovered
        except:
            print("**Call to URL was not successful**")

    # Create the output DataFrame with requested columns as out_put_table
    def output_producer(self):
        column_names = ["date", "iso", "num_confirmed", "num_deaths", "num_recovered"]
        self.output_table = pd.DataFrame(columns=column_names)

        for ind, row in self.df.iterrows():
            d1 = row["date"]
            i1 = row["iso"]
            ##
            (conf, deat, reco) = self.api_request(str(d1.date()), str(i1))
            if (conf == 0) and (deat == 0) and (reco == 0):
                continue
            self.output_table = self.output_table.append({"date": d1.date(), "iso": str(i1),
                                                          "num_confirmed": conf, "num_deaths": deat,
                                                          "num_recovered": reco}, ignore_index=True)

    # Function to write the output DataFrame to a local Excel file
    def excel_writer(self):
        with pd.ExcelWriter("Output.xlsx", date_format='YYYY-MM-DD') as writer:
            self.output_table.to_excel(writer, index=False)

    @classmethod
    def run(cls, config_file_name, excel_file_name):
        my_CR = CovidReport()
        my_CR.read_config(config_file_name, excel_file_name)
        my_CR.read_excel()
        my_CR.output_producer()
        my_CR.excel_writer()


if __name__ == '__main__':
    conf_name = input("Enter the Config file name:")
    excel_name = input("Enter the Excel file name:")
    CovidReport.run(conf_name, excel_name)
