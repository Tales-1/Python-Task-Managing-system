# =====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import date
from datetime import datetime
import os
# Get today's date
today = date.today()

# Convert date into textual format
current_date = today.strftime("%d %a %Y")

# Global variable
# Store currently logged in user
current_user = ""
# Flag to check if user has logged in
logged_in = False

# ====Functions====

# Format date into dd/mm/yyyy


def format_date(date_string):
    due_date = datetime.strptime(date_string, "%d %b %Y")
    formatted_date = due_date.strftime("%d/%m/%Y")
    return datetime.strptime(formatted_date, "%d/%m/%Y")


def check_credentials(username, password):
    # Read user.txt and loop through it to check if the inputted user and pass is correct
    status = ""
    with open("user.txt", "r") as users:
        for line in users:
            # Remove commas in the line
            line = line.split(", ")
            # Assign the username and password in the current line to a variable to make it easier to look at and understand
            check_username = line[0].strip("\n")
            check_password = line[1].strip("\n")
            # If bool statement evaluates to true then set the logged_in flag to true
            if username == check_username and password == check_password:
                status = "authenticated"
                break
            else:
                status = "not authenticated"
    return status


def register_user():
    # boolean to act as a condition for 'while' loop
    create_username = True
    # Intiate empty string to store the new username
    new_username = ""
    # Ask the admin to enter a unique username and password
    while create_username:
        new_username = input("Please enter a unique username: ")
        # Check if username exists
        with open("user.txt", "r") as user_txt:
            # Store usernames in data
            data = user_txt.readlines()
            # get number of usernames
            usernames_total = len(data)
            # track which line we are on during each iteration of for loop
            user_no = 1
            for line in data:
                # Retrieve username by splitting line and retrieving it at index 0
                line = line.split(", ")[0]
                check_username = line.strip()
                # If username exists prompt a new one
                if new_username == check_username:
                    print("Username taken. Please enter a unique username.")
                    break
                # If if current user is not the last one on the list, increment user_no to reflect the line/username
                # we are comparing the input with.
                elif user_no != usernames_total:
                    user_no += 1
                else:
                    create_username = False
    new_password = input("Please enter a unique password: ")
    confirm_password = input("Please re-enter your password to confirm it: ")
    # check if the two entries of the same password are correct
    if new_password == confirm_password:
        # If true then add the new username and password to the user.txt file
        with open("user.txt", "a+") as user_credentials:
            user_credentials.write(f"\n{new_username}, {new_password}")
    else:
            print("\n``````\nPasswords did not match. User not registered.\n\n`````` \n")


def add_task():
    # Ask for user input for the various task details
    task_username = input(
        "Enter the username of the person the ask is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")
    task_date_due = input("Enter the due date of the task: ")
    # Open task.txt and append all the details of the new task
    with open("tasks.txt", "a+") as tasks_file:
        tasks_file.write(
            f"{task_username}, {task_title}, {task_description}, {current_date}, {task_date_due}, No \n")


def view_all():
    with open("tasks.txt", "r") as all_tasks:
        for line in all_tasks:
            # Split and separate task line excluding space and commas
            # Assign each detail of the task to a readable variable
            task_title = line.split(", ")[1]
            task_assigned_to = line.split(", ")[0]
            task_date_assigned = line.split(", ")[3]
            task_date_due = line.split(", ")[4]
            task_completed = line.split(", ")[5]
            task_description = line.split(", ")[2]
            print(f"\n''''''''''''''''''''\n\nTask: {task_title} \nAssigned to: {task_assigned_to} \nDate assigned: {task_date_assigned} \nDue date: {task_date_due} \nTask Complete? {task_completed}Task Description: {task_description}\n\n''''''''''''''''''''")


def view_mine():
    # Open tasks and iterate through each task line
    tasks_dict = {}
    with open("tasks.txt", "r") as all_tasks:
        # Track which task number we are read
        task_number = 1
        # Track which line we are on starting at index 0
        line_number = 0
        for line in all_tasks:
            # Split and separate task line excluding space and commas
            # Assign each detail of the task to a readable variable
            task_assigned_to = line.split(", ")[0]
            task_title = line.split(", ")[1]
            task_date_assigned = line.split(", ")[3]
            task_date_due = line.split(", ")[4]
            task_completed = line.split(", ")[5]
            task_description = line.split(", ")[2]
            # Check if the task we are on is assigned to the current user viewing it
            if task_assigned_to == current_user:
                print(f"\n-------{task_number}------- \n\nTask: {task_title} \nAssigned to: {task_assigned_to} \nDate assigned: {task_date_assigned} \nDue date: {task_date_due} \nTask Complete? {task_completed} \nTask Description: {task_description}\n\n''''''''''''''''''''")
                # Store values of details that can be editted in a dict
                current_task_dict = {
                    # Remove whitespace at the end
                    "completed": task_completed.split(" ")[0].strip(),
                    "username": task_assigned_to,
                    "due date": task_date_due,
                    # Store line number to reference it when updating tasks
                    "line number": line_number,
                    # Store full task line which will be joined together later and written to the tasks.txt file
                    "full task": [task_assigned_to, task_title, task_description, task_date_assigned, task_date_due, task_completed]
                }
                # Store task which is assigned to current user using the task number as reference
                tasks_dict[task_number] = current_task_dict
                # Increment task and line variables
                task_number += 1
            line_number += 1
    edit_task(tasks_dict)


def edit_task(tasks_dict):
    # Get task number from user which is used to find the task in tasks_dict
    while True:
        edit_or_return = input("Enter a Task number to edit or -1 to return to the main menu. ")
        # Check if the number inputted is not -1 and is a valid task number
        if int(edit_or_return) > 0 and int(edit_or_return) < len(tasks_dict):
            selected_task_number = int(edit_or_return)
            print(f"\nTask {selected_task_number} selected.")
            menu = input('''Please select one of the following options: 
            1 - mark task as complete
            2 - edit task
            -1 - return to main menu
             ''')
            if menu == "1":
                # Retrieve chosen task using task number inputted
                selected_task = tasks_dict[selected_task_number]                
                complete = input("Complete? yes/no: ")
                if complete.lower() == "yes":
                    selected_task["completed"] = "Yes"
                elif complete.lower() == "no":
                    selected_task["completed"] = "No"
                else:
                    print("Please select correct option.")

            elif menu == "2":
                # Retrieve chosen task using task number inputted
                selected_task = tasks_dict[selected_task_number]
                # Check if task is complete, if not then user can edit the task
                if selected_task["completed"] == "No":
                    # Ask if user would like to change their username
                    change_username = input("Change username? yes/no: ")
                    if change_username.lower() == "yes":
                        selected_task["username"] = input("Enter username of the person this task should be assigned to: ")
                    elif change_username.lower() == "no":
                        print("Username was not changed. \n\n")
                    # Ask if user would like to change due date
                    change_due_date = input("Change due date of this task? yes/no")
                    if change_due_date.lower() == "yes":
                        selected_task["due date"] = input("Enter a new due date for this task.")
                    elif change_due_date.lower() == "no":
                        print("Due date was not change")
                # If task is marked as complete, let the user know.
                else:
                    print("You cannot edit this task. It is marked as complete.")

            elif menu == "-1":
                # Initialise empty data list
                data = []
                # Before exiting the menu, update tasks.txt if any edits were made
                with open("tasks.txt", "r") as f:
                    # Retrieve all the lines in the file
                    data = f.readlines()
                    # iterate through each task assigned to current user
                    for task in range(1, len(tasks_dict) + 1):
                        current_task = tasks_dict[task]
                        # Rewrite / update details of current task
                        update_task_dict(current_task)
                        # Join the newly updated task array into a string
                        full_task_joined = ", ".join(tasks_dict[task]["full task"])
                        # Replace / rewrite the task in the data variable using line_number to track which line the task was on
                        line_number = current_task["line number"]
                        data[line_number] = full_task_joined
                # Overwrite the previous tasks.txt
                with open("tasks.txt", "w+") as f:
                    for i in range(0, len(data)):
                        # before overwriting, ensure there is a single line break at the end of each line
                        divide_string = data[i].split(", ")
                        # Retrieve last part of the setnence, remove extra characters after it
                        add_line_break = divide_string[5].strip()
                        # Add a single line break
                        divide_string[5] = add_line_break + "\n"
                        # Put the string back together and replace the line with the newly updated version
                        data[i] = ", ".join(divide_string)
                    f.writelines(data)
                print("Returning back to main menu.")
                break
            else:
                print("select a valid option")
        # break out of loop if -1 is selected
        elif edit_or_return == "-1":
            break
        # if any other number is inputted, prompt the user to enter a correct task number
        else:
            print("Please enter a correct task number")

def update_task_dict(dict):
    # Update username / due date / completed by replacing their old values in the
    # full task array
    dict["full task"][0] = dict["username"]
    dict["full task"][4] = dict["due date"]
    dict["full task"][5] = dict["completed"]


def generate_report():
    # Dict to track diff stats required for final report
    report_details = {
            "tasks_freq": 0,
            "tasks_complete_freq": 0,
            "tasks_incomplete_freq": 0,
            "tasks_incomplete_overdue": 0,
            "percentage_incomplete": 0,
            "percentage_overdue": 0,
    }
    # Initialise empty list
    user_details = []
    with open("user.txt", "r") as f:
        # loop through user.txt and assign it a dict to track its stats
        for line in f:
            user_details.append({
            "name":"",
            "tasks_assigned": 0,
            "tasks_complete_freq": 0,
            "tasks_incomplete_freq": 0,
            "tasks_incomplete_overdue": 0,
            "percentage_total_tasks": 0,
            "percentage_complete": 0,
            "percentage_incomplete": 0,
            "percentage_overdue": 0
    })
    calculate_stats(report_details, user_details)
    calculate_percentages(report_details, user_details)
    write_report(report_details, user_details)


def calculate_stats(report_details, user_details):
    users_txt = open("user.txt")
    data = users_txt.readlines()
    with open("tasks.txt", "r") as tasks:
        for line in tasks:
            # increment 1 for each task in report_details
            report_details["tasks_freq"] += 1
            # Assign required values to easy to read variable names
            completed = line.split(", ")[5].lower().strip() == "yes"
            due_date = format_date(line.split(", ")[4])
            assigned_to = line.split(", ")[0]
            now = datetime.now()
            # If complete or incomplete update report_details accordingly
            if completed:
                report_details["tasks_complete_freq"] += 1
            else:
                report_details["tasks_incomplete_freq"] += 1
                # Check if the task is overdue
                if due_date < now:
                    report_details["tasks_incomplete_overdue"] += 1
            # Iterate through each user for every task that is read and update user_details
            for i in range(0, len(data)):
                # Retrieve user and update it in user_details
                target_user = data[i].split(", ")[0]
                user_details[i]["name"] = target_user
                if target_user == assigned_to:
                    user_details[i]["tasks_assigned"] += 1
                    if completed:
                        user_details[i]["tasks_complete_freq"] += 1
                    else:
                        user_details[i]["tasks_incomplete_freq"] += 1
                        if due_date < now:
                            user_details[i]["tasks_incomplete_overdue"] += 1
    users_txt.close()

def calculate_percentages(report_details,user_details):
    report_details["percentage_incomplete"] = round(report_details["tasks_incomplete_freq"] / report_details["tasks_freq"] * 100)
    report_details["percentage_overdue"] = round(report_details["tasks_incomplete_overdue"] / report_details["tasks_freq"] * 100)
    # Loop through each user
    for i in range(0, len(user_details)):
        # Percentage of total tasks assigned to this user
        if user_details[i]["tasks_assigned"] != 0:
            user_details[i]["percentage_total_tasks"] = round(user_details[i]["tasks_assigned"] / report_details["tasks_freq"] * 100)
            # Percentage of tasks complete
            user_details[i]["percentage_complete"] = round(user_details[i]["tasks_complete_freq"] / user_details[i]["tasks_assigned"] * 100)
            # Percentage of tasks incomplete
            user_details[i]["percentage_incomplete"] = round(user_details[i]["tasks_incomplete_freq"] / user_details[i]["tasks_assigned"] * 100)
            # Percentage of tasks overdue
            user_details[i]["percentage_overdue"] = round(user_details[i]["tasks_incomplete_overdue"] / user_details[i]["tasks_assigned"] * 100)
        else:
            print("No tasks assigned to user")

def write_report(report_details, user_details):
    # Write to task_overview.txt and user_overview.txt and display in a readable format
    with open("task_overview.txt", "w+") as f:
        f.write(f"TASK OVERVIEW REPORT \n" +
                f'\nTotal number of tasks: {report_details["tasks_freq"]}'
                f'\nCompleted tasks: {report_details["tasks_complete_freq"]}'
                f'\nIncompleted: {report_details["tasks_incomplete_freq"]}'
                f'\nOverdue and incomplete: {report_details["tasks_incomplete_overdue"]}'
                f'\nPercentage of incomplete tasks: {report_details["percentage_incomplete"]}%'
                f'\nPercentage of overdue tasks: {report_details["percentage_overdue"]}% \n\n')

    with open("user_overview.txt","w+") as f:
        f.write(f"USER OVERVIEW REPORT \n")
        f.write(f"\nTotal number of users: {len(user_details)}")
        f.write(f'\nTotal number of tasks generated and tracked: {report_details["tasks_freq"]}')
        for i in range(0, len(user_details)):
            # Assigned current task to this_user to avoid messy nesting
            this_user = user_details[i]
            f.write(f'\n\n----- Tasks assigned to: {this_user["name"]} -----' 
                    f'\nTotal number of tasks: {this_user["tasks_assigned"]}'
                    f'\nPercentage of total tasks assigned: {this_user["percentage_total_tasks"]}%'
                    f'\nPercentage of tasks complete: {this_user["percentage_complete"]}%'
                    f'\nPercentage of incomplete tasks: {this_user["percentage_incomplete"]}%'
                    f'\nPercentage of overdue tasks: {this_user["percentage_overdue"]}%')

# ====Login Section====

while not logged_in:
    # Prompt a username and password
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    if check_credentials(username, password) == "authenticated":
        current_user = username
        logged_in = True
    elif check_credentials(username, password) == "not authenticated":
        print("Wrong credentials, please re-enter your username and password.")

while True:
    # presenting the menu to the user and
    # making sure that the user input is coneverted to lower case.
    if current_user == "admin":
        menu = input('''\nSelect one of the following Options below:
        r - registering a user (admin only)
        a - add task
        va - view all tasks
        vm - view my task
        gr - generate reports
        ds - display statistics (admin only)
        e - exit
        : \n\n''').lower()
    else:
        menu = input('''Select one of the following Options below:
        a - add a task
        va - view all tasks
        vm - view my task
        e - exit
        : \n\n''').lower()

    if menu == 'r':
        register_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        # View all tasks option
        view_all()

    elif menu == 'vm':
        # View tasks specific to the user
        view_mine()
    elif menu == "gr":
        generate_report()
        print("```````````````````````````\nReport Generated. Select 'ds' in the menu to display report. \n")

    elif menu == 'ds':
        paths = ["task_overview.txt", "user_overview.txt"]
        # If files do not exist then generate them 
        if not os.path.exists(paths[0]) or os.path.exists(paths[1]):
            generate_report()
        # Open each file and print its contents
        for path in paths:
                with open(path) as f:
                    print(f.read())
    elif menu == 'e':
        print('Goodbye!!!')
        logged_in = False
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
