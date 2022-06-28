import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd 
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
file = gspread.authorize(credentials) 
sheet = file.open("data")
all_cells = sheet.values_get(range='A1:inf')['values']
df = pd.DataFrame(all_cells[1:], columns=all_cells[0])
print(df)