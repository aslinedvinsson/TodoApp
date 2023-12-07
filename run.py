"""
This module contains the implementation of a todo-app. The user can create, open,
delete and view todo-lists. Inside of every todo-list the user can add, update, 
sort, delete and view tasks. 
""" 

from datetime import datetime
import re
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
    def __init__(self, task_name, description = None, due_date= None,\
    priority = 10):
        self.task_name = task_name
        self.description = description
        self.due_date = due_date
        self.priority = priority

class TaskHandler:
    """
    Class for handling tasks by using a worksheet and the class for 
    user input 
    """
    def __init__(self, worksheet, user_input_handler):
        self.worksheet = worksheet
        if self.worksheet:
            #When worksheet is provided the load_tasks method loads all tasks
            #in that worksheet
            self.load_tasks()
        self.user_input_handler = user_input_handler

    def load_tasks(self):
        """
        Method to load tasks from a worksheet into the variable 'tasks'
        """
        if self.worksheet:
            data = self.worksheet.get_all_values()
            #header_row = data[0]
            self.tasks = []
            for row in data[1:]:
                task = Task(row[1], row[2], row[3], row[4])
                self.tasks.append(task)

    def display_all_tasks(self):
        """
        Retrives all tasks from the worksheet and display a list of them to 
        the user.
        """
        self.load_tasks()
        if not self.tasks:
            print('No tasks available.')
            return []
            # Loop with enumerate function to get both the index and the task
            # with all the information about the task, starting index from 1
            # instead of 0 to be more logical to the user
        for i, task in enumerate(self.tasks, start = 1):
            print(f'Task: {task.task_name} Description: {task.description}'
            'Due Date: {task.due_date}, Priority: {task.priority}')
        return self.tasks
    
    def validate_due_date_input(self, due_date):
        """
        Validate the format of the due date the user puts in.
        Returns True if the date has a valid format, otherwise False.

        The valid date format is 'DD/MM/YY':
            - DD is a two-digit day (01-31),
            - MM is a two-digit month (01-12), 
            - YY is a two-digit year 00-99)
        """
        # Code taken from https://stackoverflow.com/questions/15491894/
        # regex-to-validate-date-formats-dd-mm-yyyy-dd-mm-yyyy-dd-mm-
        # yyyy-dd-mmm-yyyy
        valid_due_date_input = re.compile(r'^(?:(?:31(\/|-|\.)(?:0?[13578]\
        |1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]\
        |[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]\
        |[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$\
        |^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1\
        [6-9]|[2-9]\d)?\d{2})$')
        if not valid_due_date_input.match(due_date): 
            raise ValueError('Invalid date format. Please use dd/mm/yy format')

    def add_task(self, task_data, worksheet_name):
        """
        Add a task to a opened worksheet.
        The method prompts user to enter information about 
        - Task name (mandatory)
        - Task description
        - Due date
        - Priority number between 1-10
        The method uses input validation and adds default value 10 if no 
        priority number is given by the user.
        The method calls the update_worksheet_data method.
        """
        """
        if self.worksheet:
            try:
                self.worksheet.append_row([worksheet_name] + task_data)
                print(f'Task added to worksheet {worksheet_name}')
                self.load_tasks()
                data = self.worksheet.get_all_values()
                print(f'ws data {data}')
            except Exception as e:
                print(f'{e} error')
        else:
            print('Task was not added.')
            print('Going back to the main menu')
            self.worksheet_handler.start_worksheet_loop()
        """
        if self.worksheet:
            try:
                task_row = [worksheet_name] + task_data
                self.workshet.append_row(task_row)
                print(f'Task added to worksheet {worksheet_name}')
                self.load_tasks()
                print(f'Updated list of tasks: {self.tasks}')
            except Exception as e:
                print(f'{e} error')
        else:
            print('Task was not added.')
            print('Going back to the main menu')
            self.worksheet_handler.start_worksheet_loop()

    def update_task(self, task_name):
        """
        Update information for a selected task in the current worksheet.
        The method prompts user to update information for a selected task.
        The method displays the current information for the user and let 
        the user update information in the categories they want to update. 
        If the user do not want to update a specific category, the user press 
        Enter to go to the next category.
        """
        task_to_update = None
        for task in self.tasks:
            if task.task_name.lower() == task_name.lower():
                task_to_update = task
                break
        if task_to_update is None:
            print(f'Task {task_name} not found.')
            return
        self.update_worksheet_data()
        print(f'Current Task: {task_to_update.task_name}')
        new_task_name = input('Please enter a new task name (press Enter to'
        'keep current): ')
        task_to_update.task_name = new_task_name if new_task_name else \
        task_to_update.task_name
        print(f'Current Description: {task_to_update.description}')
        new_description = input('Please enter updated description (press Enter'
        ' to keep current): ')
        task_to_update.description = new_description if new_description\
        else task_to_update.description
        print(f'Current Due Date: {task_to_update.due_date}')
        new_due_date = input('Please enter updated due date (format dd/mm/yy,'
        ' press Enter to keep current): ')
        if self.validate_due_date_input(new_due_date):
            task_to_update.due_date = new_due_date if new_due_date\
            else task_to_update.due_date
        else:
            print('Invalid date format. Task due date remains unchanged.')
        print(f'Current Priority: {task_to_update.priority}')
        new_priority = input('Please, enter updated priority number (press' 
        ' Enter to keep current): ')
        if new_priority:
            try:
                new_priority = int(new_priority)
                if 1 <= new_priority <= 10:
                    task_to_update.priority = new_priority
                else:
                    print('Invalid priority number. Task priority remains'
                    'unchanged.')
            except ValueError:
                print('Invalid input. Priority should be a number. Task'
                'priority remains unchanged.')
        print(f'Task {task_to_update.task_name} updated successfully.')
        self.update_worksheet_data()
    
    def update_worksheet_data(self):
        self.worksheet.clear()
        header_row = ['todo_title', 'task_name', 'description', 'due date',\
        'priority']
        self.worksheet.append_row(header_row)
        for task in self.tasks:
            row = [self.worksheet.title, task.task_name, task.description, \
            task.due_date, task.priority]
            self.worksheet.append_row(row)

    def sort_tasks(self):
        """
        Sort tasks in the current worksheet based on the users choice.
        The method prompts the user to choose between:
        - sort by task name 
        - sort by due date
        - sort by priority
        The method then sorts the tasks and update the worksheet.
        """
        print('How would you like to sort your tasks?')
        print('1. Sort by task name (alphabetical order)')
        print('2. Sort by due date (The earliest date on the top of the'
        'todo_list)')
        print('3. Sort by priority number (1 on the top of the todo-list.)')
        choice = input('Please enter the number of the sorting method you '
        'choose: ')
        # Skip first row with categorie names
        tasks = self.worksheet.get_all_values()[1:] 
        if choice == '1':
            sorted_tasks = sorted(tasks, key = lambda x: x[1])
        elif choice == '2':
            sorted_tasks = sorted(tasks, key = lambda x: datetime.strptime\
            ( x[3], '%d/%m/%y') if x[3] else datetime.max)
        elif choice == '3':
            sorted_tasks = sorted(tasks, key = lambda x: int(x[4]))
        else:
            print('Invalid choice. Please try agian.')
            return
        # Empty existing data in the worksheet
        self.worksheet.clear()
        self.worksheet.append_row(['todo_title', 'task', 'task_description',\
        'due_date', 'priority'])
        for task in sorted_tasks:
            self.worksheet.append_row(task)
        print('The tasks are sorted')


    def delete_task(self, row_to_delete_input):
        """
        Delete the task the user selects from the current worksheet.
        The method deletes the corresponding row to the task from the worksheet.
        The user can abort the action by pressing q. 
        """
        try:
            deleted_task = None
            for i, task in enumerate(self.tasks):
                if task.task_name.lower() == row_to_delete_input.lower():
                    deleted_task = self.tasks.pop(i)
                    print(f'Task {row_to_delete_input} was deleted.')
                    break
            if deleted_task is None:
                print(f'Task {row_to_delete_input} was not found.')
            self.update_worksheet_data()
        except exception as e:
            print(f'{e} error occurred while delteing task')
  
class Sheet:
    """
    Class to provide functionality to interact with Google sheets using the 
    gspread library
    """
    def __init__(self):
        self.sheet = self.open_spreadsheet()

    def open_spreadsheet(self):
        """
        Open the 'todo--app' spreadsheet.
        Returns a tuple with opened spreadsheet.
        """
        try:
            sheet = GSPREAD_CLIENT.open('todo--app')
            return sheet
        except gspread.exceptions.SpreadsheetNotFound as e:
            print(f'Spreadsheet not found: {e}')
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()
            return None
        except gspread.exception.APIError as e:
            print(f'{e} error opening spreadsheet')
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()
            return None

class WorksheetHandler:
    """
    Class for handling worksheets.
    """
    def __init__(self, sheet):
        self.sheet = sheet
        self.task_handler = None
        self.user_input_handler = UserInputHandler(self, None)
        self.worksheet_handler = self

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
            existing_worksheets = self.sheet.worksheets()
            for existing_worksheet in existing_worksheets:
                if existing_worksheet.title == worksheet_name:
                    print(f'Worksheet {worksheet_name} already exist. Chose '
                    'another name for the worksheet.')
                    return None
            worksheet = self.sheet.add_worksheet(title = worksheet_name, \
            rows = '20', cols= '10')
            worksheet.row_values(1)
            worksheet.insert_row(['todo_title', 'task_name', 'description', \
            'due_date', 'priority'], 1)
            print(f'Worksheet {worksheet_name} was created')
            self.task_handler = TaskHandler(worksheet, self.user_input_handler)
            return worksheet
        except gspread.exceptions.APIError as e:
            print(f'Error creating worksheet: {e}')
            print('Going back to main menu')
            self.start_worksheet_loop()
            return None

    def open_worksheet(self, worksheet_name):
        """
        Open a specific worksheet in Google Sheets. Argument is the name of 
        the worksheet.

        """
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            print(f'{worksheet_name} was opened')
            self.task_handler = TaskHandler(worksheet, self.user_input_handler)
            self.user_input_handler.task_handler = self.task_handler
            #Creating a default Task instance
            self.user_input_handler = UserInputHandler(self, self.task_handler)
            self.task_handler.load_tasks()
            todo_list = TodoList(self.user_input_handler, self.task_handler, \
            self.worksheet_handler, worksheet, worksheet_name)
            todo_list.display_choices_for_task()
            return worksheet
        except gspread.exceptions.WorksheetNotFound:
            print(f'Worksheet not found: {worksheet_name}')
            print('Going back to main menu')
            self.start_worksheet_loop()
            return None
        except gspread.exceptions.APIError as e:
            print(f'{e} error opening worksheet')
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()
            return None

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
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()
            return None
    
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
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()
            return None

    def start_worksheet_loop(self):
        """
        A loop that displays different options for the user on what to do with 
        the worksheets.
        """
        print("Welcome to your Todo App! Let's turn your tasks into "
        "accomplishments. Get started by creating your todo-list and adding"
        " tasks.\n")
        
        worksheet = None
        task_handler = None
        user_input_handler = None
        while True:
            print('What would you like to do? Choose one option by entering a '
                        'number. You can press q whenever you want to quit or'
                        ' get back to the start and make a new choice')
            print('1. Create a new worksheet')
            print('2. Open a specific worksheet')
            print('3. Display a list of your current worksheets')
            print('4. Delete a whole worksheet. If you do NOT want to delete'
            ' a worksheet, press q to exit the program.')
            print('q. Quit')
            worksheet_choice = input('Please enter your choice: \n')
            if worksheet_choice == '1':
                worksheet_name = self.get_worksheet_name()
                self.create_worksheet(worksheet_name)
                self.task_handler = TaskHandler(worksheet, \
                self.user_input_handler)   
            elif worksheet_choice == '2':
                worksheet_name = self.get_worksheet_name()
                worksheet = self.open_worksheet(worksheet_name)                   
            elif worksheet_choice == '3':
                self.display_existing_worksheets()
            elif worksheet_choice == '4':
                while True:
                    print('Are you sure you want to delete a worksheet? Once '
                    'you have deleted it, you can not get it back. If you do '
                    'NOT want to delete a worksheet, press q.')
                    self.display_existing_worksheets()
                    worksheet_delete = input('Please enter the name of the 
                    'worksheet you would like to delete: \n').lower()
                    if worksheet_delete.lower() == 'q':
                        print('Going back to main menu')
                        self.start_worksheet_loop()
                        return None
                    else:
                        self.delete_worksheet(worksheet_delete)
                        break
            elif worksheet_choice.lower() == 'q':
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
                return None
            else:
                print('Invalid choice. Please enter a valid choice')
            if worksheet and task_handler:
                user_input_handler = UserInputHandler(self, task_handler)
                task_data = user_input_handler.get_add_task_input(worksheet)
                task_handler.add_task(task_data, worksheet_name)

    def get_worksheet_name(self): #TODOadd exception
        """
        Prompt the user to enter the name of a worksheet.
        """
        while True:
            worksheet_name = input('Please enter a worksheet name: \n').lower()
            if worksheet_name.lower() == 'q':
                print('Going back to main menu')
                self.start_worksheet_loop()
                return None
            else:
                return worksheet_name

class UserInputHandler:
    """
    Class for handling user input
    """
    def __init__(self, worksheet_handler, task_handler):
        self.worksheet_handler = worksheet_handler
        self.task_handler = task_handler
    
    def get_user_choice_for_task(self): 
        return input('Please, enter your choice: \n')

    #def get_add_task_input(self, task_data, worksheet_name):
    def get_add_task_input(self, task_data):
        """
        Method to prompt the user to enter information to add a new task. The 
        user is asked to enter information on task name, description, due date 
        and priority. Only task name is mandatory for the user to enter. If the
        user at any time press q, they exit and return to the main menu. 
        """
        while True: 
            print('To add a task you have to enter a task name. All other '
            'information is optional to add. Just press Enter when you want'
            ' to go to the next category.')
            task_name = self.get_user_input('Please add the name of the '
            'task: \n')
            if task_name.lower() == 'q':
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
            elif task_name is None:
                return []
            description = self.get_user_input('Please add a description of '
            'the task: \n') 
            if description is None:
                return []
            while True:
                due_date = self.get_user_input('Please enter a due-date'
                '(format dd/mm/yy): \n')
                try:
                    if due_date == '':
                        break
                    elif due_date.lower() == 'q':
                        print('Going back to main menu')
                        self.worksheet_handler.start_worksheet_loop()
                        return []
                    self.task_handler.validate_due_date_input(due_date)
                    break
                except ValueError as e:
                    print(f'{e} error')
            priority = self.get_user_input('Please choose a priority number '
            'between 1-10, where 1 is top priority: \n')
            if priority is None:
                return []
            elif not priority:
                priority = 10
                print(f'The default value {priority} is set when you do not'
                ' add a number.')
            else:
                try:
                    # Convert input to integer
                    priority = int(priority)
                    if 1<= priority <=10:
                        return []
                    else:
                        print('Invalid priority number. Please try again.')
                except ValueError:
                    print('Invalid input. Please enter a valid number')
                    return []
        task_data = [task_name, description, due_date, priority]
        return task_data
    
    def get_user_input(self, prompt):
        """
        Method to get user input with prompt.
        """
        user_input = input(prompt)
        if user_input.lower() == 'q':
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()
        elif not user_input:
            print('Please enter a valid input or press q to go back to the'
            'main menu')
        return user_input
    
    def get_delete_task_input(self):
        """
        Method to prompt the user to enter the name of the task they want to 
        delete. The user can exit by pressing q and then return to main menu 
        without executing the deletion.
        """
        print('Are you sure you want to delete a task? Once '
        'you have deleted it, you can not get it back. If you do '
        'NOT want to delete a task, press q.')
        self.task_handler.display_all_tasks()     
        while True:
            row_to_delete_input = input('Please enter the name of the task '
            'you would like to delete: \n').lower()
            if row_to_delete_input == '':
                print('Please enter the name of the task you want to delete.'
                ' If you do NOT want to delete a task, press q.')
            elif row_to_delete_input.lower() == 'q':
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
                return None
            else:
                found_task = False
                for task in self.task_handler.tasks:
                    if task.task_name.lower() == row_to_delete_input:
                        found_task = True
                        break
                if not found_task:
                    print('Cant find task name.Please try agian')
                else:
                    self.task_handler.delete_task(row_to_delete_input)
                    break
        return row_to_delete_input
                
  
class TodoList:
    """
    Class representing a todo list.
    """
    def __init__(self, user_input_handler, task_handler, worksheet_handler, \ 
    worksheet, worksheet_name):
        self.user_input_handler = user_input_handler
        self.task_handler = task_handler
        self.worksheet_handler = worksheet_handler
        self.worksheet = worksheet
        self.worksheet_name = worksheet_name

    def display_choices_for_task(self):
        """
        Method to display a number of choices to manage a task. 
        The user is prompt to make a choice by enter the letter of the 
        action they want to perform. 
        The choices are:
        - add task
        - update task
        - sort task
        - delete task
        - quit
        Depending on the users choice other methods are called.
        """
        print('What would you like to do? Choose one option by entering a '
        'letter. You can press q whenever you want quit or get back start and '
        'make a new choice')
        print('a. Add task')
        print('b. Update task') 
        print('c. Sort tasks') 
        print('d. Delete task') 
        print('e. View current tasks')
        print('q. Quit')

        user_choice = self.user_input_handler.get_user_choice_for_task()
        self.handle_user_choice(user_choice)

    def handle_user_choice(self, choice):
        """
        Method to handle the user's choice for action in the todo list.
        """
        while True:
            if choice == 'a':
                task_data = self.user_input_handler.get_add_task_input\
                (self)
                self.task_handler.add_task(task_data, self.worksheet_name)   
                break
            elif choice == 'b':
                self.task_handler.display_all_tasks()
                task_name_to_update = input('Please enter the name of the task'
                ' you would like to update: ')
                if task_name_to_update == 'q':
                    print('Going back to main menu')
                    self.worksheet_handler.start_worksheet_loop()
                self.task_handler.update_task(task_name_to_update)
                break
            elif choice == 'c':
                self.task_handler.sort_tasks()
                break
            elif choice == 'd':
                task_to_delete = self.user_input_handler.get_delete_task_input()
                if task_to_delete == 'q':
                    print('Going back to main menu')
                    self.worksheet_handler.start_worksheet_loop()
                self.task_handler.delete_task(task_to_delete)   
                break    
            elif choice == 'e':
                self.task_handler.display_all_tasks()
                break
            elif choice == 'q':
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
                break
            else: 
                print('Invalid choice. Please enter a valid choice') 
                choice = self.user_input_handler.get_user_choice_for_task()

def main(): 
    """
    The main function of the program. It initialixes objects, handles 
    user input and manages workflow of the program
    """
    sheet = Sheet().sheet
    worksheet_handler = WorksheetHandler(sheet)
    worksheet_handler.start_worksheet_loop()

if __name__ == '__main__':
    main()
