import unittest
from CovidReport import CovidReport


class TestCovidReport(unittest.TestCase):
    # Testing the initialized value of class
    def test_initial_df(self):
        CoRe = CovidReport()
        self.assertEqual(CoRe.df, None)

    def test_initial_full_path(self):
        CoRe = CovidReport()
        self.assertEqual(CoRe.full_path, "")

    def test_initial_output_table(self):
        CoRe = CovidReport()
        self.assertEqual(CoRe.output_table, None)

    # ----------------------------------------------------------------------
    # Testing the performance of read_config function
    def test_config_not_found(self):
        CoRe = CovidReport()
        self.assertRaises(Exception, CoRe.read_config("conf.ini", "ISO_DATE.xlsx"))

    def test_full_Excel_path(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        self.assertEqual(CoRe.full_path, "/Users/ahesam.gh/opt/anaconda3/envs/Exiger_Project/ISO_DATE.xlsx")

    def test_keyword_not_found(self):
        CoRe = CovidReport()
        self.assertRaises(Exception, CoRe.read_config("config.ini", "IS_DATE.xlsx"))

    # ----------------------------------------------------------------------
    # Testing performance of read_excel function:
    def test_df_creation(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertIsNotNone(CoRe.df)

    def test_correctness_of_df_1(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(CoRe.df.iloc[1]["iso"], "GBR")

    def test_correctness_of_df_2(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(CoRe.df.iloc[10]["iso"], "GTM")

    def test_correctness_of_df_3(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(str((CoRe.df.iloc[2]["date"]).date()), "2020-10-28")

    # ----------------------------------------------------------------------
    # Test performance of api_request function:
    def test_total_deaths(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(CoRe.api_request("2020-10-28", "AFG")[1], 1529)

    def test_total_confirmed(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(CoRe.api_request("2020-10-28", "AFG")[0], 41145)

    def test_total_recovered(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(CoRe.api_request("2020-10-28", "AFG")[2], 34237)

    def test_wrong_iso(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(CoRe.api_request("2020-10-28", "ABG")[2], 0)

    def test_wrong_date(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        self.assertEqual(CoRe.api_request("2020-09-28", "AFG")[2], 0)

    # ----------------------------------------------------------------------
    # Test performance of output_producer function:
    def test_table_size_1(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        CoRe.output_producer()
        self.assertEqual(CoRe.output_table.shape[0], 12)

    def test_table_size_2(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        CoRe.output_producer()
        self.assertEqual(CoRe.output_table.shape[1], 5)

    def test_table_elements_1(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        CoRe.output_producer()
        self.assertEqual((CoRe.output_table.loc[CoRe.output_table.iso == "GBR", "num_deaths"]).values[0], 45765)

    def test_table_elements_2(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        CoRe.output_producer()
        self.assertEqual((CoRe.output_table.loc[CoRe.output_table.iso == "ESH", "num_confirmed"]).values[0], 10)

    def test_table_elements_3(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        CoRe.output_producer()
        self.assertEqual((CoRe.output_table.loc[CoRe.output_table.iso == "UKR", "num_deaths"]).values[0], 6938)

    def test_table_elements_4(self):
        CoRe = CovidReport()
        CoRe.read_config("config.ini", "ISO_DATE.xlsx")
        CoRe.read_excel()
        CoRe.output_producer()
        self.assertEqual((CoRe.output_table.loc[CoRe.output_table.iso == "IND", "num_recovered"]).values[0], 7315989)


if __name__ == '__main__':
    unittest.main()
