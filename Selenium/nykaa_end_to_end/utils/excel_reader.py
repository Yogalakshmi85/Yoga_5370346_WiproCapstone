import os
from openpyxl import load_workbook

class ExcelReader:

    def __init__(self, file_path):
        project_root = os.getcwd()
        self.file_path = os.path.join(project_root, file_path)

    def get_phone(self):
        print("Reading Excel from:", self.file_path)  

        wb = load_workbook(self.file_path)
        sheet = wb.active
        return str(sheet["A2"].value)