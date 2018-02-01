import xlrd
import json
import argparse

class ExcelToJson():

    def __init__(self, excel_file, json_file):
        self.excel = excel_file
        self.json_file = json_file
        self.convert()


    def convert(self):
        wb = xlrd.open_workbook(self.excel)
        sh = wb.sheet_by_index(0)

        for rownum in range(1, sh.nrows):
            row_values = sh.row_values(rownum)
            print(row_values)
            # print(row_values[1])


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Excel to JSON Converter")
    parser.add_argument("excel_input", type=str, help = "Member availabilities, .xlsx")
    parser.add_argument("json_starter", type=str, help = "Previous week's Member data, .json")
    args = parser.parse_args()
    scheduler = ExcelToJson(args.excel_input, args.json_starter)