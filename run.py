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


class Task:
    """
    Class representing a task. Attributes are task_name, description, due_date 
    and priority. Task name is mandatory for the user to enter, other attributes 
    are optional. Default number 10 is set on priority if the user does not 
    enter a priority number.
    """
    def __init__(self, task_name, description = None, due_date= None, priority = 10):
        self.task_name = task_name
        self.description = description
        self.due_date = due_date
        self.priority = priority

class TaskHandler:
    def __init__(self, worksheet):
        self.worksheet = worksheet
        if self.worksheet:
            self.load_tasks()

    def load_tasks(self):
        if self.worksheet:
            data = self.worksheet.get_all_values()
            header_row = data[0]
            self.tasks = []
            for row in data[1:]:
                task = Task(row[1], row[2], row[3], row[4])
                self.tasks.append(task)

    

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
            #print('Spreadsheet found')
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
        except gspread.exceptions.WorksheetNotFound:
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
        """
        Open a specific worksheet in Google Sheets. Argument is the name of 
        the worksheet.
        """
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            print(f'{worksheet_name} was opened')
            return worksheet
        except gspread.exceptions.WorksheetNotFound:
            print(f'Worksheet not found: {worksheet_name}')
            return None
        except gspread.exceptions.APIError as e:
            print(f'{e} error opening worksheet')
            sys.exit()
    
    def display_existing_worksheets(self):
        """
        Display the names of the existing worksheets. Prints a list of 
        worksheets.
        """
        try:
            worksheets = self.sheet.worksheets()
            worksheet_names = [worksheet.title for worksheet in worksheets]
            print('Your current worksheets:')
            for name in worksheet_names:
                print(name)
        except gspread.exceptions.APIError as e:
            print(f'{e} error displaying worksheets')
            sys.exit()
    
    def delete_worksheet(self, worksheet_delete):
        """
        Delete a worksheet of the users choice.
        """
        try:
            worksheet = self.sheet.worksheet(worksheet_delete)
            self.sheet.del_worksheet(worksheet)
            print(f'Worksheet {worksheet_delete} was deleted.')
        except gspread.exceptions.WorksheetNotFound:
            print(f'Worksheet not found: {worksheet_delete}')
            return None
        except gspread.exceptions.APIError as e:
            print(f'{e} error deleting worksheet')
            sys.exit()
    

    def start_worksheet_loop(self):
        """
        A loop that displays different options for the user on what to do with 
        the worksheets.
        """
        worksheet = None
        
        while True:
            print('What would you like to do? Choose one option by entering a number. You can press q whenever you want to quit or get back to the start and make a new choice')
            print('1. Create a new worksheet')
            print('2. Open a specific worksheet')
            print('3. Display a list of your current worksheets')
            print('4. Delete a whole worksheet. If you do NOT want to delete a worksheet, press q to exit the program.')
            print('q. Quit')

            worksheet_choice = input('Enter your choice: \n')

            if worksheet_choice == '1':
                worksheet_name = self.get_worksheet_name()
                self.create_worksheet(worksheet_name)
                
            elif worksheet_choice == '2':
                worksheet_name = self.get_worksheet_name()
                worksheet = self.open_worksheet(worksheet_name)
                
            elif worksheet_choice == '3':
                self.display_existing_worksheets()

            elif worksheet_choice == '4':
                while True:
                    print('Are you sure you want to delete a worksheet? Once '\
                    'you have deleted it, you can not get it back. If you do '\
                    'NOT want to delete a worksheet, press q.')
                    self.display_existing_worksheets()
                    worksheet_delete = input('Enter the name of the worksheet '\
                    'you would like to delete: \n').lower()
                    if worksheet_delete.lower() == 'q':
                        print('Exiting the program')
                        sys.exit()
                    else:
                        self.delete_worksheet(worksheet_delete)
                        break

            elif worksheet_choice.lower() == 'q':
                print('Exiting the program')
                sys.exit()
            else:
                print('Invalid choice. Please enter a valid choice')
    
    def get_worksheet_name(self):
        """
        Prompt the user to enter the name of a worksheet.
        """
        while True:
            worksheet_name = input('Enter a worksheet name: \n').lower()
            if worksheet_name.lower() == 'q':
                print('Exiting the program')
                sys.exit()
            else:
                return worksheet_name

class TodoList:
    def __init__(self, task_handler, worksheet, worksheet_name):
        self.task_handler = task_handler
        self.worksheet = worksheet
        self.worksheet_name = worksheet_name

    def display_choices_for_task(self):
        print('What would you like to do? Choose one option by entering a letter. You can press q whenever you want quit or get back start and make a new choice')
        print('a. Add task')
        print('b. Update task') # #TODO add if q under
        print('c. Sort tasks') # #TODO add if q under
        print('d. Delete task') # #TODO add if q under
        print('e. View current tasks') # #TODO add if q under
        print('q. Quit')

def main(): 
    sheet = Sheet().sheet
    worksheet_handler = WorksheetHandler(sheet)
    task_handler = None
    worksheet_handler.start_worksheet_loop()

    worksheet_name = input('Enter the name of the worksheet you would like to open: \n').lower() 
    worksheet = worksheet_handler.open_worksheet(worksheet_name)
    task_handler = TaskHandler(worksheet)

if __name__ == '__main__':
    main()