# =====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import date
## Get today's date
today = date.today()
# Convert date into textual format
current_date = today.strftime("%d %B %Y")
# ====Login Section====
# A boolean value to determine if the user is logged in or not
logged_in = False
# Initiate global current user variable which stores the username of the currently logged in user
current_user = ""
while not logged_in:
    # Prompt a username and password
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    # Read user.txt and loop through it to check if the inputted user and pass is correct
    with open("user.txt", "r+") as users:
        for line in users:
            # Remove commas in the line
            line = line.replace(",", "")
            # Assign the username and password in the current line to a variable to make it easier to look at and undestand
            check_username = line.split()[0]
            check_password = line.split()[1]
            # If bool statement evaluates to true then set the logged_in flag to true
            if username == check_username and password == check_password:
                logged_in = True
                current_user = username
                print("Successfully logged in")
    # If entered incorrectly, let the user know and prompt them to re-enter their details
    if not logged_in:
        print("Wrong credentials, please re-enter your username and password.")

while True:
    # presenting the menu to the user and
    # making sure that the user input is coneverted to lower case.
    menu = input(f'''Select one of the following Options below:
r - Registering a user (admin only)
a - Adding a task
va - View all tasks
vm - View my task
st - View statistics (admin only)
e - Exit
: ''').lower()

    if menu == 'r':
        # Conditional statement checking if the current user is admin. If not the program lets the user know it cannot access this option.
        if current_user == "admin":
            # Ask the admin to enter a unique username and password
            new_username = input("Please enter a unique username: ")
            new_password = input("Please enter a unique password: ")
            confirm_password = input("Please re-enter your password to confirm it: ")
            # check if the two entries of the same password are correct
            if new_password == confirm_password:
                # If true then add the new username and password to the user.txt file
                with open("user.txt","a+") as user_credentials:
                    user_credentials.write(f"\n{new_username}, {new_password}")
            else:
                print("Passwords did not match. User not registered.")
        else:
            print("''''''''''''\n\nRestricted access. Only admins can register users.\n\n''''''''''''")

    elif menu == 'a':
        # Ask for user input for the various task details
        username_task = input("Enter the username of the person the ask is assigned to: ")
        title_of_task = input("Enter the title of the task: ")
        description_of_task = input("Enter the description of the task: ")
        due_date_task = input("Enter the due date of the task: ")
        # Open task.txt and append all the details of the new task
        with open("tasks.txt", "a+") as tasks_file:
            tasks_file.write(f"\n{username_task}, {title_of_task}, {description_of_task}, {current_date}, {due_date_task}, No")

    elif menu == 'va':
        # View all tasks option
        with open("tasks.txt","r") as all_tasks:
            for line in all_tasks:
                # Split and separate task line excluding space and commas
                # Assign each detail of the task to a readable variable
                task = line.split(", ")[1]
                assigned_to = line.split(", ")[0]
                date_assigned = line.split(", ")[3]
                due_date = line.split(", ")[4]
                complete = line.split(", ")[5]
                description = line.split(", ")[2]
                # Print the Task details in a readable format
                print(f"''''''''''''''''''''\n\nTask: {task} \nAssigned to: {assigned_to} \nDate assigned: {date_assigned} \nDue date: {due_date} \nTask Complete? {complete} \nTask Description: {description}\n\n''''''''''''''''''''")
        
    elif menu == 'vm':
        # View tasks specific to the user
        with open("tasks.txt","r") as all_tasks:
            for line in all_tasks:
                # Split and separate task line excluding space and commas
                # Assign each detail of the task to a readable variable
                task = line.split(", ")[1]
                assigned_to = line.split(", ")[0]
                date_assigned = line.split(", ")[3]
                due_date = line.split(", ")[4]
                complete = line.split(", ")[5]
                description = line.split(", ")[2]
                # Print the Task details in a readable format
                if assigned_to == current_user:
                    print(f"''''''''''''''''''''\n\nTask: {task} \nAssigned to: {assigned_to} \nDate assigned: {date_assigned} \nDue date: {due_date} \nTask Complete? {complete} \nTask Description: {description}\n\n''''''''''''''''''''")
    
    elif menu == 'st':
        # Statistics menu for admin
        # Conditional statement to check if the current user opening this option is an admin
        if current_user == "admin":
            # Initiate empty counter variables
            user_counter = 0
            task_counter = 0
            # Loop through both user.txt and tasks.txt and for each line increment the user and task counter
            with open("user.txt", "r") as users:
                for user in users:
                    user_counter += 1
            with open("tasks.txt","r") as tasks:
                for task in tasks:
                    task_counter +=1
            # Print statistics out
            print(f"'''''''''''''''\nSTATISTICS\n\nTotal number of users: {user_counter} \nTotal number of tasks: {task_counter}\n\n'''''''''''''''")
        else:
            # If the current user is not an admin then let the user know it cannot access this option
            print("''''''''''''\n\nRestricted access. Only admins can view statistics\n\n''''''''''''")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
