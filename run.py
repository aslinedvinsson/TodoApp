import sys # sys module to run the function sys.exit()
import re # hänvisa källa
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Section of code taken from the Love Sandwich project
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('todo--app')
# End of section code from the Love Sandwich project

test = SHEET.worksheet('test')
data = test.get_all_values()
print(data)