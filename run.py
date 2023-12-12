"""
This module contains the implementation of a todo-app. The user can create,
open, delete and view todo-lists. Inside of every todo-list the user can add,
update, sort, delete and view tasks.
"""
import sys # sys module to run the function sys.exit()
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
    and priority. Task name is mandatory for the user to enter, other
    attributes are optional. Default number 10 is set on priority if the user
    does not enter a priority number.
    """
    def __init__(self, task_name, description = None, due_date= None, \
    priority = 10):
        self.task_name = task_name
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.urgency = self.calculate_urgency()

    def task_summary(self):
        """
        Returns a summary of the task.
        """
        return f'Task: {self.task_name}, Description: {self.description}, \
        Due Date: {self.due_date}, Priority: {self.priority}'

    def calculate_urgency(self):
        """
        Calculates and returns the urgency of the task based on due date
        and priority by dividing the priority by the number of days left until
        due date.
        """
        if self.due_date:
            due_date = datetime.strptime(self.due_date, '%d/%m/%y')
            if self.priority is not None:
                priority = int(self.priority)
                urgency = priority / (due_date - datetime.now()).days
                return round(urgency, 2)
        return None

class TaskHandler:
    """
    Class for handling tasks by using a worksheet and the class for
    user input
    """
    def __init__(self, worksheet, worksheet_handler, user_input_handler):
        self.worksheet_handler = worksheet_handler
        self.user_input_handler = user_input_handler
        self.worksheet = worksheet
        if self.worksheet:
            #When worksheet is provided the load_tasks method loads all tasks
            #in that worksheet
            self.load_tasks()

    def load_tasks(self):
        """
        Method loads tasks from the worksheet and creates Task instances for
        each row and append to tasks list
        """
        if self.worksheet:
            data = self.worksheet.get_all_values()
            #initialize an empty list
            self.tasks = []
            #skip the first row witch is the header row
            for row in data[1:]:
                task = Task(row[1], row[2], row[3], row[4])
                self.tasks.append(task)

    def display_all_tasks(self):
        """
        Retrives all tasks from the worksheet and display a list of them to
        the user.
        """
        print()
        self.load_tasks()
        if not self.tasks:
            print('No tasks available.')
            print()
            print('Going back to the main menu')
            self.worksheet_handler.start_worksheet_loop()
           #Loop with enumerate function to get both the index and the task
           #with all the information about the task, starting index from 1
           #instead of 0 to be more logical to the user
        for task in self.tasks:
            urgency = task.calculate_urgency()
            #If there is a due date, the urganecy is calculated
            urgency_message = f'Urgency: {round(urgency, 2)}' if urgency is \
            not None else 'No due date'
            print(f'{task.task_summary()}, {urgency_message}')
        return self.tasks

    def validate_due_date_input(self, due_date):
        """
        Method to validate due date format. Returns True if the format is
        correct, otherwise returns False.
        Code from https://datatest.readthedocs.io/en/stable/how-to/date-time-
        str.html and https://www.digitalocean.com/community/tutorials/python-
        string-to-datetime-strptime
        """
        try:
            # Try to parse the date using the specified format
            datetime.strptime(due_date, '%d/%m/%y')
            # Date is in the correct format
            return True
        except ValueError:
            # Date is not in the correct format
            return False

    def add_task(self, task_data, worksheet_name = None, worksheet = None):
        """
        Add a task to a opened worksheet.
        The method calls the update_worksheet_data method.
        """
        try:
            if worksheet_name and worksheet:
                row_data = [worksheet_name] + task_data
                #List comprehension to replace any None in row_data with an
                #empty string
                row_data = [item if item is not None else '' for item \
                in row_data]
                worksheet.append_row(row_data)
                print(f'Task added to {worksheet_name}')
                self.load_tasks()
            else:
                print('Invalid worksheet information. Task was not added.')
        except gspread.exceptions.APIError as e:
            print(f'{e} error adding task')
        print()
        print('Going back to the main menu')
        self.worksheet_handler.start_worksheet_loop()

    def update_task(self, task_name):
        """
        Update information for a selected task in the current worksheet.
        The method prompts user to update information for a selected task.
        The method displays the current information for the user and let the
        user update information in the categories they want to update. If the
        user do not want to update a specific category, the user press Enter
        to go to the next category.
        """
        task_to_update = self.find_task_by_name(task_name)

        if task_to_update:
            self.update_task_name(task_to_update)
            self.update_description(task_to_update)
            self.update_due_date(task_to_update)
            self.update_priority(task_to_update)
            print(f'Task {task_to_update.task_name} updated sucessfully')
            self.update_worksheet_data()
        else:
            print(f'Task {task_name} not found.')
        if self.worksheet_handler:
            self.worksheet_handler.start_worksheet_loop()

    def find_task_by_name(self, task_name):
        """
        Method to find a task in the worksheet by its name.
        """
        return next((task for task in self.tasks if task.task_name.lower() \
        == task_name.lower()), None)

    def update_task_name(self, task):
        """
        Method to update the name of the task
        """
        new_task_name = self.user_input_handler.get_update_task_input\
        ('Please enter a new task name.', task.task_name)
        if self.user_input_handler.handle_exit_condition(new_task_name):
            return
        task.task_name = new_task_name if new_task_name else \
        task.task_name

    def update_description(self, task):
        """
        Method to update the description of the task
        """
        new_description = self.user_input_handler.get_update_task_input\
        ('Please enter updated description', task.description)
        if self.user_input_handler.handle_exit_condition(new_description):
            return
        task.description = new_description if new_description \
        else task.description

    def update_due_date(self, task):
        """
        Method to update the due date of the task
        """
        print(f'Current due date: {task.due_date}')
        new_due_date = self.user_input_handler.get_update_task_input\
        ('Please enter updated due date (format dd/mm/yy)', \
        task.due_date)
        if self.user_input_handler.handle_exit_condition(new_due_date):
            return
        if self.validate_due_date_input(new_due_date):
            task.due_date = new_due_date if new_due_date else\
                task.due_date
        else:
            print('No new due date entered or invalid date format. Task due '
            'date remains unchanged.')

    def update_priority(self, task):
        """
        Method to update the priority of the task
        """
        new_priority = self.user_input_handler.get_update_task_input\
        ('Please enter updated priority ', task.priority)
        if self.user_input_handler.handle_exit_condition(new_priority):
            return
        if new_priority:
            try:
                new_priority = int(new_priority)
                if 1 <= new_priority <= 10:
                    task.priority = new_priority
                else:
                    print('Invalid priority number. Task priority '
                    'remains unchanged.')
            except ValueError:
                print('Invalid input. Priority should be a number. '
                'Task priority remains unchanged.')

    def update_worksheet_data(self):
        """
        Method to update worksheet with task data. Clears existing data, adds
        header row and append rows for each task.
        """
        self.worksheet.clear()
        header_row = ['todo_title', 'task_name', 'description', 'due date', \
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
        Learned abourt lambda functions at https://www.freecodecamp.org/news/
        python-lambda-functions/
        """
        # Skip first row with categorie names
        tasks = self.worksheet.get_all_values()[1:]
        self.load_tasks()
        if not self.tasks:
            print('No tasks available.')
            print()
            print('Going back to the main menu')
            self.worksheet_handler.start_worksheet_loop()
            return
        print('How would you like to sort your tasks?')
        print('1. Sort by task name (alphabetical order)')
        print('2. Sort by due date (The earliest date on the top of the '
        'todo_list)')
        print('3. Sort by priority number (1 on the top of the todo-list.)')
        while True:
            choice = input('Please enter the number of the sorting method '
            'you choose: ')
            if choice in ['1', '2', '3']:
                break
            elif choice.lower() == 'q':
                        print()
                        print('Going back to main menu')
                        self.worksheet_handler.start_worksheet_loop()
                        return None
            else:
                print('Invalid choice. Please try again.')
        #Initialize an empty list to store sorted tasks
        sorted_tasks = []
        if choice == '1':
            #Sorted by the second element of each task
            sorted_tasks = sorted(tasks, key = lambda x: x[1])
        elif choice == '2':
            #Sorted by the fourth element of each task
            sorted_tasks = sorted(tasks, key = lambda x: \
            datetime.strptime( x[3], '%d/%m/%y') if x[3] else datetime.max)
        elif choice == '3':
            #Sorted by the fifth element of each task
            sorted_tasks = sorted(tasks, key = lambda x: int(x[4]))
        # Empty existing data in the worksheet
        self.worksheet.clear()
        self.worksheet.append_row(['todo_title', 'task', 'task_description', \
        'due_date', 'priority'])
        for task in sorted_tasks:
            self.worksheet.append_row(task)
        print('The tasks are sorted')
        self.worksheet_handler.start_worksheet_loop()

    def delete_task(self, row_to_delete_input):
        """
        Delete the task the user selects from the current worksheet.
        The method deletes the corresponding row to the task from the
        worksheet.The user can abort the action by pressing q.
        """
        for i, task in enumerate(self.tasks):
            if task.task_name.lower() == row_to_delete_input.lower():
                self.tasks.pop(i)
                print(f'Task {row_to_delete_input} was deleted.')
                break
        self.update_worksheet_data()
        self.worksheet_handler.start_worksheet_loop()

class Sheet:
    """
    Represent a Google sheets document.
    """
    def __init__(self):
        """
        Initialize a Sheet instance and open the 'todo--app' spreadsheet
        """
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
            ptint('Exiting the program. Press the red button to start the app'
            'again.')
            sys.exit()

    def linter_method(self):
        """
        Method to satisfy the linter.
        """
        print('Linter method')

class WorksheetHandler:
    """
    Class for handling worksheets.
    """
    def __init__(self, sheet):
        self.sheet = sheet
        self.worksheet_handler = None
        self.task_handler = None
        self.user_input_handler = UserInputHandler(self, self.task_handler, \
        None)

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
            print(f'Todo-list not found: {worksheet_name}.Going back to main '
            'menu')
            self.start_worksheet_loop()
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
                    print(f'Todo-list {worksheet_name} already exist. Chose '
                    'another name for the worksheet.')
                    return None
            worksheet = self.sheet.add_worksheet(title = worksheet_name, \
            rows = '20', cols= '10')
            worksheet.row_values(1)
            worksheet.insert_row(['todo_title', 'task_name', 'description', \
            'due_date', 'priority'], 1)
            print(f'Todo-list {worksheet_name} was created')
            self.task_handler = TaskHandler(worksheet, self.worksheet_handler,\
             self.user_input_handler)
            return worksheet
        except gspread.exceptions.APIError as e:
            print(f'Error creating worksheet: {e}')
            print()
            print('Going back to main menu')
            self.start_worksheet_loop()
            return None

    def open_worksheet(self, worksheet_name, worksheet_handler):
        """
        Open a specific worksheet in Google Sheets. Argument is the name of
        the worksheet.
        """
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            print(f'{worksheet_name} was opened')
            self.task_handler = TaskHandler(worksheet, self, \
            self.user_input_handler)
            self.user_input_handler.task_handler = self.task_handler
            #Creating a default Task instance
            self.user_input_handler = UserInputHandler(self, \
            self.task_handler, Task('', '', '', 10))
            self.task_handler.load_tasks()
            #Create a dictionary to hold references to objects
            settings = {
                'user_input_handler': self.user_input_handler,
                'task_handler': self.task_handler,
                'worksheet': worksheet,
                'worksheet_name': worksheet_name,
                'worksheet_handler': worksheet_handler
            }
            todo_list = TodoList(settings)
            todo_list.display_choices_for_task()
            return worksheet
        except gspread.exceptions.WorksheetNotFound:
            print(f'Todo-list not found: {worksheet_name}. Going back to main'
            ' menu')
            self.start_worksheet_loop()
            return None
        except gspread.exceptions.APIError as e:
            print(f'{e} error opening worksheet')
            print()
            print('Going back to main menu')
            self.start_worksheet_loop()
            return None

    def display_existing_worksheets(self):
        """
        Display the names of the existing worksheets. Prints a list of
        worksheets.
        """
        try:
            worksheets = self.sheet.worksheets()
            worksheet_names = [worksheet.title for worksheet in worksheets]
            print('Your current todo-lists:')
            for name in worksheet_names:
                print(name)
        except gspread.exceptions.APIError as e:
            print(f'{e} error displaying worksheets')
            print()
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()

    def delete_worksheet(self, worksheet_delete):
        """
        Delete a worksheet of the users choice.
        """
        try:
            worksheet = self.sheet.worksheet(worksheet_delete)
            self.sheet.del_worksheet(worksheet)
            print(f'Todo-list {worksheet_delete} was deleted.')
        except gspread.exceptions.WorksheetNotFound:
            print(f'Todo-list not found: {worksheet_delete}')
        except gspread.exceptions.APIError as e:
            print(f'{e} error deleting worksheet')
            print('Going back to main menu')
            self.worksheet_handler.start_worksheet_loop()

    def start_worksheet_loop(self):
        """
        A loop that displays different options for the user on what to do with
        the worksheets.
        """
        worksheet = None
        while True:
            title = """
 _____      _         _____
|_   _|__ _| |___ ___|  _  |___ ___
  | || . | . | . |___|     | . | . |
  |_||___|___|___|   |__|__|  _|  _|
                           |_| |_|
"""
            print(title)
            print('Welcome to your todo app! Here, you can create todo lists,'
            ' and within each list, you can efficiently manage your tasks by '
            'adding, updating, sorting, deleting, and viewing them.')
            print()
            print('What would you like to do? Choose one option by entering '
            'a number. You can press q whenever you want to quit or get back '
            'to the start and make a new choice')
            print('1. Create a new todo-list')
            print('2. Open a specific todo-list. Here you can then modify your'
            ' todo-list by handeling tasks in the todo-list')
            print('3. Display a list of your current todo-list')
            print('4. Delete a whole todo-list. If you do NOT want to delete '
            'a todo-list, press q to exit the program.')
            worksheet_choice = input('Please enter your choice: \n')
            print()
            if worksheet_choice == '1':
                worksheet_name = self.get_worksheet_name()
                self.create_worksheet(worksheet_name)
                worksheet_handler = WorksheetHandler(self.sheet)
                self.task_handler = TaskHandler(worksheet, worksheet_handler, \
                self.user_input_handler)
            elif worksheet_choice == '2':
                worksheet_name = self.get_worksheet_name()
                worksheet_handler = WorksheetHandler(self.sheet)
                worksheet = worksheet_handler.open_worksheet(worksheet_name, \
                worksheet_handler)
            elif worksheet_choice == '3':
                self.display_existing_worksheets()
            elif worksheet_choice == '4':
                print('Are you sure you want to delete a worksheet? Once '
                'you have deleted it, you can not get it back. If you do '
                'NOT want to delete a worksheet, press q.')
                self.display_existing_worksheets()
                while True:
                    worksheet_delete = input('Please enter the name of the '
                    'todo-list you would like to delete: \n').lower()
                    if worksheet_delete.lower() == 'q':
                        print()
                        print('Going back to main menu')
                        self.start_worksheet_loop()
                        return None
                    elif worksheet_delete in [worksheet.title for worksheet \
                        in self.sheet.worksheets()]:
                        self.delete_worksheet(worksheet_delete)
                        break
                    else:
                        print(f'{worksheet_delete} does not exist. Please try '
                        'another todo-list name')
            else:
                print(f'{worksheet_choice} is not a valid choice. Please enter '
                ' a valid choice.')

    def get_worksheet_name(self):
        """
        Prompt the user to enter the name of a worksheet.
        """
        while True:
            worksheet_name = input('Please enter a todo-list name: \n').lower()
            if worksheet_name.lower() == 'q':
                print()
                print('Going back to main menu')
                self.start_worksheet_loop()
                return None
            return worksheet_name

class UserInputHandler:
    """
    Class for handling user input
    """
    def __init__(self, worksheet_handler, task_handler, task):
        self.worksheet_handler = worksheet_handler
        self.task_handler = task_handler
        self.task = task

    def get_user_choice_for_task(self):
        """
        Method to prompt the user to enter their choice for a task
        """
        return input('Please, enter your choice: \n')

    def get_task_name(self):
        """
        Method to prompt the user to enter a task name. Only task name is
        mandatory for the user to enter. If the user at any time press q,
        they exit and return to the main menu.
        """
        while True:
            task_name = input('Please add the name of the task: \n')
            if task_name == '':
                print('Please add a name of the task you would like to add.')
            elif task_name.lower() == 'q':
                print()
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
            else:
                return task_name

    def get_descripton(self):
        """
        Method to prompt the user to enter a priority (1-10) for the task
        """
        while True:
            print()
            description = input('Please add a description of the task: \n')
            if description.lower() == 'q':
                print()
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
            return description

    def get_due_date(self, worksheet):
        """
        Method to prompt the user to enter a description for the task
        """
        while True:
            print()
            due_date = input('Please enter a due-date(format dd/mm/yy): \n')
            task_handler = TaskHandler(worksheet, self.worksheet_handler, self)
            if due_date.lower() == 'q':
                print()
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
            elif due_date == '':
                return due_date
            valid_due_date_input = task_handler.validate_due_date_input\
            (due_date)
            if valid_due_date_input:
                return due_date
            print('Invalid date format. Please try agian.')

    def get_priority(self):
        """
        Method to prompt the user to enter a priority (1-10) for the task
        """
        while True:
            print()
            priority = input('Please choose a priority number between 1-10, '
            'where 1 is top priority: \n')
            if priority.lower() == 'q':
                print()
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
            if not priority:
                priority = 10
                print(f'The default value {priority} is set when you do '
                'not add a number.')
                return priority
            try:
                # Convert input to integer
                priority = int(priority)
                if 1<= priority <=10:
                    return priority
            except ValueError:
                print('Invalid input. Please enter a valid number')

    def get_add_task_input(self, worksheet):
        """
        Method to prompt the user to enter information to add a new task. The
        user is asked to enter information on task name, description, due date
        and priority. Only task name is mandatory for the user to enter. If the
        user at any time press q, they exit and return to the main menu.
        """
        print()
        print('To add a task you have to enter a task name. All other '
            'information is optional to add. Just press Enter when you want to '
            'go to the next category.')
        task_name = self.get_task_name()
        if task_name is None:
            return None
        description = self.get_descripton()
        if description is None:
            return None
        due_date = self.get_due_date(worksheet)
        if due_date is None:
            return None
        priority = self.get_priority()
        if priority is None:
            return None
        task_data = [task_name, description, due_date, priority]
        return task_data

    def get_update_task_input(self, prompt, current_value):
        """
        The method get user input to update a task, press Enter to keep current
        information or press 'q' to go back to main menu
        """
        while True:
            user_input = input (f'{prompt} Current value: {current_value}. '
            'Press Enter to keep current information, or press q to go back '
            'to main menu): ')
            self.handle_exit_condition(user_input)
            return user_input

    def handle_exit_condition(self, user_input):
        """
        The method handles the exit condition if user enter 'q'
        """
        if user_input.lower() == 'q':
            print('Going back to the main menu')
            self.worksheet_handler.start_worksheet_loop()
            return True
        return False

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
                print()
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
                    print()
                else:
                    self.task_handler.delete_task(row_to_delete_input)
                    break
        return row_to_delete_input

class TodoList:
    """
    Class representing a todo list.
    """
    def __init__(self, settings):
        self.user_input_handler = settings.get('user_input_handler')
        self.task_handler = settings.get('task_handler')
        self.worksheet = settings.get('worksheet')
        self.worksheet_name = settings.get('worksheet_name')
        self.worksheet_handler = settings.get('worksheet_handler') or \
        self.default_worksheet_handler()

    def default_worksheet_handler(self):
        """
        Create and return a default worksheet handler
        """
        default_handler = WorksheetHandler(Sheet().sheet)
        return default_handler

    def display_choices_for_task(self):
        """
        Method to display a number of choices to manage a task. The user
        is prompt to make a choice by enter the letter of the action they want
        to perform.
        The choices are:
        - add task
        - update task
        - sort task
        - delete task
        - quit
        Depending on the users choice other methods are called.
        """
        print()
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
                task_data = \
                self.user_input_handler.get_add_task_input(self.worksheet)
                if task_data is not None:
                    self.task_handler.add_task(task_data, \
                    self.worksheet_name, self.worksheet)
            elif choice == 'b':
                self.task_handler.display_all_tasks()
                task_name_to_update = input('Please enter the name of the task'
                ' you would like to update: ')
                if task_name_to_update.lower() == 'q':
                    print()
                    print('Going back to main menu')
                    self.worksheet_handler.start_worksheet_loop()
                    return
                self.task_handler.update_task(task_name_to_update)
            elif choice == 'c':
                self.task_handler.sort_tasks()
            elif choice == 'd':
                task_to_delete = \
                self.user_input_handler.get_delete_task_input()
                self.task_handler.delete_task(task_to_delete)
            elif choice == 'e':
                self.task_handler.display_all_tasks()
                self.worksheet_handler.start_worksheet_loop()
            elif choice == 'q':
                print()
                print('Going back to main menu')
                self.worksheet_handler.start_worksheet_loop()
                return
            else:
                choice = input('Invalid choice. Please enter your choice '
                'again: ')

def main():
    """
    The main function of the program witch initalizes Sheet, WorksheetHandler
    and call method start_worksheet_loop()
    """
    sheet = Sheet().sheet
    worksheet_handler = WorksheetHandler(sheet)
    worksheet_handler.start_worksheet_loop()

if __name__ == '__main__':
    main()
