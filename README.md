
# ToDo App

The todo app is a digital tool designed to help users organize and manage their tasks. It allows users to create, edit, and delete tasks, set due dates and priorities. 

Deployed site
https://todo--app-bd22256d01b5.herokuapp.com/ 


## Flowchart

The flowchart below, constructed using [draw.io](https://app.diagrams.net/), illustrates the planning process for this application.

add flowchart####
## Design and organizational structure

The design of the user interface was constrained due to its simplicity, as this is a basic terminal-based application.

The code for the title of the app is generated by https://patorjk.com/software/taag/#p=display&c=echo&f=Alpha&t=Todo%20App 

printscreeen###


### Organizational Structure
The code organizes its functionality into classes, including Task, TaskHandler, Sheet, WorksheetHandler, UserInputHandler, and TodoList, each dedicated to managing specific aspects of the application for Todo-lists.

#### WorksheetHandler Class
The main functionality is encapsulated within the WorksheetHandler class, which control the overall flow of the application. This includes creating, opening, and deleting worksheets.

printscreeen###

#### Dependency on Google Sheets:
To interact with Google Sheets, the application relies on the gspread library. OAuth2 credentials (creds.json) are utilized for secure authentication.

#### Error Handling
The code incorporates try-except blocks for handling exceptions such as gspread.exceptions and ValueError, ensuring robust error management.

#### User Input Handling
Responsibility for collecting user input for tasks like creating, opening, viewing, and deleting todo-lists lies with the UserInputHandler class. Additionally, this class manages user input related to tasks, such as adding, updating, sorting, and deleting tasks.
printscreeen###

#### Task Handling
The TaskHandler class is dedicated to managing tasks within a worksheet. Its responsibilities include loading tasks from the worksheet, displaying tasks, adding tasks, updating tasks, and deleting tasks.

#### TodoList Class
The TodoList class serves as a user interface for interacting with tasks. It presents options for users to add, update, sort, delete, and view tasks.

#### Main Function
The main function initializes essential components and initiates the worksheet loop to control the application's execution.

#### Interactive User Interface
The application offers an interactive user interface through a console, enabling users to navigate various options.

#### Exit Strategy
In the event of errors or when users decide to quit their current activity, the code employs the statement print('Going back to the main menu') self.worksheet_handler.start_worksheet_loop() to facilitate a transition back to the main menu.

#### Structured Data Handling
To represent tasks, the code utilizes a Task class, incorporating attributes like task name, description, due date, and priority for effective data organization.


## Program goal
The goal of the program is to provide the user a tool to create todo-lists and manage the tasks in every todolist. The program aims to provide users with a tool for creating and managing todo-lists, enabling effective task management within each list.

## User and administrator stories
As a user I want to:
- be able to create a new todo-list so that I can organize and categorize my tasks based on different projects or priorities.
- add tasks to my todo-lists, specifying details such as task name, description, due date, and priority, to keep track of what needs to be done.
- have the ability to view all tasks within a specific todo-list so that I can have a comprehensive overview of my pending tasks.
- edit existing tasks, allowing me to update details like task name, description, due date, or priority, ensuring my todo-list remains accurate and up-to-date.
- have the option to delete tasks that are no longer relevant or necessary, maintaining the cleanliness and relevance of my todo-list.
- be able to sort tasks within a todo-list based on different criteria, such as due date or priority, to help me prioritize and manage my tasks more efficiently.
- be able to create multiple todo-lists to organize tasks for different aspects of my life, work, or personal projects.

As a site administrator I want to:
- have  the capability to modify the application and provide users with a tool for effectively organizing and managing tasks within lists.

## Features

### Logo
Displays app title using ascii generator#####

### Welcome Message
A welcome message is displayed upon starting the application, providing a introduction to the user.

### Clear Instructions
The application offers clear instructions guiding the user on how to create and effectively manage a to-do list. The instructions aim to make the process intuitive and user-friendly.

### Data Validation
Data validation mechanisms are implemented to ensure that user inputs are accurate and within the expected format. This helps prevent errors and enhances the overall user experience by guiding them to enter valid information.

### Error Handling
The application incorporates error-handling mechanisms to manage unexpected situations. Error messages are provided to the user, offering guidance on how to address issues or providing alternatives to proceed.

### Possible Future Features
#### Future user and administrator stories
As a user I want to
- mark tasks as completed so that I can easily track my progress and identify the tasks that still need attention.
- receive notifications or reminders for upcoming tasks or deadlines to help me stay on top of my responsibilities.
- have the option to share my todo-lists with others, facilitating collaboration and coordination on shared projects or tasks.
- be able to integrate the tasks with calendar apps to sync tasks and deadlines.

As a site administrator I want to

- have the ability to manage users, add or remove members, and control access to specific to-do lists.
- track and provide insights into user activity, such as completed tasks, common categories, and peak usage times.
- implement a data backup system for administrators to safeguard user data, along with a recovery mechanism in case of accidental deletions or data loss.

## Language, libraries and packages used
- Language: Python
- [gspread](https://docs.gspread.org/en/v5.12.0/) Google API for GoogleSheets
- [google.oauth2.service_account](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html) provides functionality for working with Google Cloud service accounts. Service accounts are special Google accounts that belong to the application , rather than to an individual end user.
- [Datetime](https://docs.python.org/3/library/datetime.html) for manipulating dates and times
- [Re](https://docs.python.org/3/library/re.html) provides regular expression support.
- colorama used to add color for ......####

### Other tools
- [GitHub](https://github.com/) Used to host the application source code.
- [Gitpod](https://www.gitpod.io/) Cloud development environment to write the application source code.
- [Heroku](www.heroku.com) Used to host the application
- [Draw.io](https://app.diagrams.net/) Used to make flowcharts

## Testing

### Automated testing
Automated testing was performed using the Code Institutes' own linter, available at https://pep8ci.herokuapp.com/ and Pylint at https://pypi.org/project/pylint/ to check the code. ####The file run.py revealed no errors or warnings in the code.


Error: 

Solution:

No further errors or warnings.

####printscreen


[Lighthouse](https://chromewebstore.google.com/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk?hl=sv&pli=1)

####printscreen

### Browser Testing

Ensuring all parts of the program function as expected in all major browsers. Tested browsers are Google Chrome, Mozilla Firefox and #####Safari

### Manual testing
The code has been extensively tested on both the local terminal and the simulated terminal on the deployed Heroku site. Deliberate entry of invalid inputs was done during testing.The app was navigated through while different options were experimented with.

## Debugging

### Fixed Bugs
#####add
### Unfixed Bugs
No unfixed bugs to date. #####

## Deployment

This project was deployed using Code Insitute's mock terminal for Heroku.
- Visit Heroku and set up a profile if you haven't already.
- Click on the "New" button located in the upper right corner, then select "Create New App" from the ensuing menu.
- Provide a distinct name for your application and choose the region (Europe). Subsequently, click on the "Create App" button.
- Navigate to the "Settings" tab and scroll down to the "Config Vars" section.
- Click on "Reveal Config Vars" and add "PORT" to the Key field and "8000" to the Value field. Afterward, click "Add."
- Include "CREDS" in the Key field and input your credentials in the Value field if applicable.
- Under "Buildpacks," click on "Add Buildpack," choose "Python," and save the selection. Repeat this process for Node.js in the correct sequence.
- Return to the top and select the "Deploy" tab.
- Opt for GitHub as the deployment method and authorize the connection.
- Search for your repository and establish the connection.
- At the bottom, choose your preferred deployment type.
- Opt for "Enable Automatic Deploys" to deploy automatically when there are pushes on GitHub, or select manual deployment.

## Credits

### Code from

###Add

Method validate_due_date() comes from code at [Stackoverflow](https://stackoverflow.com/questions/15491894/regex-to-validate-date-formats-dd-mm-yyyy-dd-mm-yyyy-dd-mm-yyyy-dd-mmm-yyyy) 

The utilization of the [Code Institute p3-template](https://github.com/Code-Institute-Org/p3-template) facilitated the development of this project. This template includes the necessary code to enable the execution of my Python run.py within a console window embedded in a web page.
The tasks of activating API credentials, establishing a connection to the API, and importing the gspread library were accomplished by following the Love Sandwiches walkthrough provided by Code Institute.

### Acknowledgements
In shaping the trajectory of this project, I owe credit to my respected mentor, Jad Mokdad, whose crucial guidance and wise counsel have been instrumental. His perceptive advice has not only illuminated the path for me to focus my efforts but has also offered guidance for optimal impact and success.

