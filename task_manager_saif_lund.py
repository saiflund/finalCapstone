# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


# function for registering user
def reg_user():
    '''Add a new user to the user.txt file'''
    new_username = input("New Username: ")
    
    # check for duplicate username
    if new_username in username_password:
        print("Username taken. Please try again.")
        return
    
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    else:
        print("Passwords do not match")


# function for adding task, using same code as original file
def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


# function to view all tasks
def view_all():
    '''Reads the tasks from tasks.txt file and prints them to the console'''
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)


# function to view the current logged in users' tasks
def view_mine():
    # loops through tasks and retrieves total number of tasks assigned to user
    # if tasks = 0
    task_count = len(task_list)
    if task_count == 0:
        print("No tasks assigned to you.")
        return

    # if tasks exist
    print("Tasks assigned to you:")
    for i, t in enumerate(task_list):
        if t['username'] == curr_user:
            print(f"{i+1}. Task: \t\t {t['title']}")
            print(f"   Assigned to: \t {t['username']}")
            print(f"   Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"   Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"   Task Description: \n {t['description']}")
            print(f"   Completed: \t\t {'Yes' if t['completed'] else 'No'}")
            print()

    # allows the user to select a task or go back to the main menu
    while True:
        task_choice = input("Enter the number of the task you want to select (or -1 to return to the main menu): ")
        if task_choice == '-1':
            return
        # checks the user makes a valid choice
        elif not task_choice.isdigit() or int(task_choice) < 1 or int(task_choice) > task_count:
            print("Invalid task number. Please try again.")
            continue
        else:
            task_index = int(task_choice) - 1
            selected_task = task_list[task_index]

            print(f"Selected Task: \t{selected_task['title']}")
            print(f"Assigned to: \t{selected_task['username']}")
            print(f"Due Date: \t{selected_task['due_date'].strftime(DATETIME_STRING_FORMAT)}")
            print(f"Description: \n{selected_task['description']}")
            print(f"Completed: \t{'Yes' if selected_task['completed'] else 'No'}")
            print()

            # allows the user to mark a task as completed
            action_choice = input("Select an action: \n1. Mark task as complete\n2. Edit task\n3. Go back\nChoice: ")
            if action_choice == '1':
                # tells the user the task is already completed if they attempt to mark as complete
                if selected_task['completed']:
                    print("Task is already marked as complete.")
                else:
                    selected_task['completed'] = True
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in task_list:
                            str_attrs = [
                                t['username'],
                                t['title'],
                                t['description'],
                                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                "Yes" if t['completed'] else "No"
                            ]
                            task_list_to_write.append(";".join(str_attrs))
                        task_file.write("\n".join(task_list_to_write))
                    print("Task marked as complete.")
            elif action_choice == '2':
                # prevents the editing of a task marked as complete
                if selected_task['completed']:
                    print("Task cannot be edited as it is already marked as complete.")
                else:
                    edit_choice = input("What would you like to edit?\n1. Username\n2. Due Date\n3. Cancel\nChoice: ")
                    if edit_choice == '1':
                        new_username = input("Enter the new username: ")
                        selected_task['username'] = new_username
                        with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))
                        print("Username updated.")
                    elif edit_choice == '2':
                        while True:
                            new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                            try:
                                due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                                break
                            except ValueError:
                                print("Invalid datetime format. Please use the format specified.")
                        selected_task['due_date'] = due_date_time
                        with open("tasks.txt", "w") as task_file:
                            task_list_to_write = []
                            for t in task_list:
                                str_attrs = [
                                    t['username'],
                                    t['title'],
                                    t['description'],
                                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                                    "Yes" if t['completed'] else "No"
                                ]
                                task_list_to_write.append(";".join(str_attrs))
                            task_file.write("\n".join(task_list_to_write))
                        print("Due date updated.")
                    elif edit_choice == '3':
                        continue
                    else:
                        print("Invalid choice. Please try again.")
            elif action_choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

# function to generate reports
def generate_reports():
    '''Generates reports based on tasks'''
    # Task overview
    total_tasks = len(task_list)
    completed_tasks = sum(t['completed'] for t in task_list)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = 0

    # loops through tasks in task_list and classes incomplete tasks past due date as overdue
    for t in task_list:
        if not t['completed'] and t['due_date'].date() < date.today():
            overdue_tasks += 1

    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
    overdue_percentage = (overdue_tasks / total_tasks) * 100

    task_overview = f"Task Overview\n\n"
    task_overview += f"Total tasks: {total_tasks}\n"
    task_overview += f"Completed tasks: {completed_tasks}\n"
    task_overview += f"Uncompleted tasks: {uncompleted_tasks}\n"
    task_overview += f"Overdue tasks: {overdue_tasks}\n"
    task_overview += f"Incomplete percentage: {incomplete_percentage:.2f}%\n"
    task_overview += f"Overdue percentage: {overdue_percentage:.2f}%"

    # opens a new txt file 'task_overview.txt' where it writes task_overview lines to it
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(task_overview)

    # User overview
    total_users = len(username_password)

    # returns the total number of users
    user_overview = f"User Overview\n\n"
    user_overview += f"Total users: {total_users}\n"

    # loops through the keys and values in the username_password dictionary 
    # for each key-value in dictionary, returns number of tasks assigned to user
    # checks for task completion, and sets initial number of overdue tasks = 0
    for user, password in username_password.items():
        user_tasks = [t for t in task_list if t['username'] == user]
        total_user_tasks = len(user_tasks)
        completed_user_tasks = sum(t['completed'] for t in user_tasks)
        uncompleted_user_tasks = total_user_tasks - completed_user_tasks
        overdue_user_tasks = 0

        # if any tasks for that user are uncompleted past the due date, they become overdue
        for t in user_tasks:
            if not t['completed'] and t['due_date'].date() < date.today():
                overdue_user_tasks += 1

        user_task_percentage = (total_user_tasks / total_tasks) * 100
        completed_user_percentage = (completed_user_tasks / total_user_tasks) * 100
        uncompleted_user_percentage = (uncompleted_user_tasks / total_user_tasks) * 100
        overdue_user_percentage = (overdue_user_tasks / total_user_tasks) * 100

        user_overview += f"\nUser: {user}\n"
        user_overview += f"Total tasks assigned: {total_user_tasks}\n"
        user_overview += f"Percentage of total tasks: {user_task_percentage:.2f}%\n"
        user_overview += f"Percentage of completed tasks: {completed_user_percentage:.2f}%\n"
        user_overview += f"Percentage of uncompleted tasks: {uncompleted_user_percentage:.2f}%\n"
        user_overview += f"Percentage of overdue tasks: {overdue_user_percentage:.2f}%\n"

    # opens a new txt file 'user_overview.txt' where it writes user_overview lines to it
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(user_overview)

    print("Reports generated successfully!")

# function to generate files if tasks.txt and user.txt do not exist
def generate_files():
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as tasks_file:
            tasks_file.write("")

    # Create user.txt if it doesn't exist
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as users_file:
            users_file.write("")

    print("Files generated: tasks.txt, users.txt")

while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()
    elif menu == 'ds' and curr_user == 'admin':
        # Generate the files if they don't exist
        if not os.path.exists("tasks.txt") or not os.path.exists("user.txt"):
            generate_files()

        # Read the number of users from "user.txt"
        with open("user.txt", 'r') as users_file:
            users_data = users_file.readlines()
            num_users = len(users_data)

        # Read the number of tasks from "tasks.txt"
        with open("tasks.txt", 'r') as tasks_file:
            tasks_data = tasks_file.readlines()
            num_tasks = len(tasks_data)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        ("-----------------------------------")
    elif menu == 'e':
        print('Goodbye!!!')
        break
    else:
        print("Invalid selection. Please try again.")
