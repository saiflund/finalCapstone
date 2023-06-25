# finalCapstone
HyperionDev SWE Bootcamp capstone project

This program has the functionality of a simple task management system
This program is designed for a small business to help it to manage tasks assigned to each member of a team

The program allows the admin to register users to a database, add tasks to corresponding users and view all tasks assigned to all users using the following functions:
reg_user
add_task
view_all

Once registered, users can login and to view tasks specifically assigned to them by using the view_mine function

The program has steps taken to ensure usernames are not duplicated, and will display relevant error messages if the admin attemps to add a duplicate user
The user is able to navigate through a menu to see their tasks, mark the task as complete or edit the task parameters

The admin can also generate reports and display statistics which will generate a new text file task_overview.txt containing the following:
The number of total taskt that have been generated and tracked
The total number of completed tasks
The total number of uncompleted tasks
The total number of tasks that haven't been completed and that are overdue
The percentage of tasks that are incomplete
The percentage of tasks that are overdue

The same function will also generate another text file user_overview.txt which will contain the following:
The total number of users registered with task_manager.py
The total number of tasks that have been generated and tracked using task_manager.py

For each user it will also describe:
The total number of tasks assigned to that user
The percentage of the total number of tasks that have been assigned to that user
The percentage of the tasks assigned to that user that have been completed
The percentage of the tasks assigned to that user that must still be completed
The percentage of the tasks assigned to that user that have not yet been completed and are overdue
