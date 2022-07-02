import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd 
class GoogleAPI:
    __scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    def __init__(self):
        credentials = ServiceAccountCredentials. \
            from_json_keyfile_name("app/googleapi/credentials.json", 
                                   self.__scopes)
        self.__file = gspread.authorize(credentials) 

    def update(self):
        sheet = self.__file.open("data")
        all_cells = sheet.values_get(range='A1:inf')['values']
        for cell in all_cells[1:]:
            cell[0] = int(cell[0])
            cell[1] = int(cell[1])
            cell[2] = float(cell[2])
        return pd.DataFrame(all_cells[1:], columns=all_cells[0])