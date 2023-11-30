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


class Sheet:
    def __init__(self):
        self.sheet = self.open_spreadsheet()

    def open_spreadsheet(self):
        """
        Open the 'todo--app' spreadsheet.
        Returns a tuple with opened spreadsheet.
        """
        try:
            sheet = GSPREAD_CLIENT.open('todo--app')
            print('Spreadsheet found')
            return sheet
        except gspread.exceptions.SpreadsheetNotFound as e:
            print(f'Spreadsheet not found: {e}')
            sys.exit()

class WorksheetHandler:
    def __init__(self, sheet):
        self.sheet = sheet

    def get_worksheet(self, worksheet_name):
        """
        Retrieve a worksheet form Google Sheets.
        Argument is the name of the workshet.
        Returns the worksheet requested or None.
        """

        try:
            worksheets = self.sheet.worksheets()
            
            for worksheet in worksheets:
                if worksheet.title == worksheet_name:
                    print(f'{worksheet_name} was got')
                    return worksheet

            print(f'Worksheet not found: {worksheet_name}')
            return None

        except gspread.exceptions.APIError as e:
            print(f'Error getting worksheet: {e}')
            return None

    def create_worksheet(self, worksheet_name):
        """
        Create a new worksheet in the spreadsheet.
        Returns the new worksheet.
        """
        try:
            worksheet = self.sheet.add_worksheet(title = worksheet_name, rows = '20', cols= '10')
            worksheet.row_values(1)
            worksheet.insert_row(['todo_title', 'task_name', 'description', 'due_date', 'priority', 'color'], 1)
            print(f'Worksheet {worksheet_name} was created')
            return worksheet
        except gspread.exceptions.APIError as e:
            print(f'Error creating worksheet: {e}')
            sys.exit()

    def open_worksheet(self, worksheet_name):
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            print(f'{worksheet_name} was opened')
            return worksheet
        except gspread.exceptions.APIError as e:
            print(f'{e} error opening worksheet')
            sys.exit()