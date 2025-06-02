import time
import random
import pickle
import os
import sys
from datetime import datetime, timedelta

from colorama import init, Fore, Style

init(autoreset=True)

###SAVING AND LOADING DATA

#creates a file to hold task information
FILE_NAME = "to_do_list.pkl"


# function to try to load to_do_list and marked_done (it's done in the application() function)
def load_list():
    try:
        with open(FILE_NAME, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return [], []


# function to save the data everytime a change is made in to_do_list and marked_done variables
def save_data():
    try:
        with open(FILE_NAME, "wb") as file:
            pickle.dump((all_tasks_list, marked_done), file)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error saving file: {e}")

#######################################################################################

### USER INTERFACE

# the logo displayed at the top
def logo():
    return r"""
 __  __         _____         _        
|  \/  |_   _  |_   _|_ _ ___| | _____ 
| |\/| | | | |   | |/ _` / __| |/ / __|
| |  | | |_| |   | | (_| \__ \   <\__ \
|_|  |_|\__, |   |_|\__,_|___/_|\_\___/
        |___/                   
"""

# fun and cool little start up screen
def start_up_screen():
    scrolling_text(logo())
    pause(None)

# displays the logo,
def display_top(message):
    print(Fore.LIGHTBLACK_EX + logo())
    if message:
        print(Style.BRIGHT + Fore.LIGHTBLACK_EX + message)
    print(66 * "─")
    display_tasks()

# displays the tasks section
def display_tasks():
    print(f"TASK NAME{17*" "}DEADLINE{24*" "}PRIORITY")
    print(66 * "─")

    if not all_tasks_list:
        print(Fore.LIGHTBLACK_EX + "Your to-do list is empty, add some tasks!")
        print(66 * "─")

    else:
        for index, task in enumerate(all_tasks_list):
            name = task["name"]
            deadline = format_deadline(task["deadline"])
            priority = format_priority(task["priority"])

            whitespace1 = " " * (18 - len(name))
            whitespace2 = " " * 31 if deadline == "" else " " * (36 - len(deadline))

            if index in marked_done:
                print(Fore.LIGHTGREEN_EX + f"[x] {index + 1}. {name} {whitespace1} {deadline} {whitespace2} {priority}")
            else:
                print(f"[ ] {index + 1}. {name} {whitespace1} {deadline} {whitespace2} {priority}")
            print(66 * "─")

# the main window
def application():
    global all_tasks_list, marked_done, current_menu
    all_tasks_list, marked_done = load_list()
    # start_up_screen()
    current_menu = "main_menu"

    while True:
        display_top(random_quote())
        display_menu_options(current_menu)

        user_input = input(Fore.LIGHTWHITE_EX + "> ").strip().lower()
        clear_terminal()

        current_menu = handle_choice(user_input)
        clear_terminal()

#######################################################################################

### MENU HANDLING

# getting input

# menus
def display_menu_options(menu_type):
    if menu_type == "main_menu":
        print(Fore.LIGHTBLACK_EX + "Main Menu")
        print(Style.BRIGHT + Fore.WHITE + "1. Add Tasks")
        print(Fore.LIGHTWHITE_EX + "2. Delete Tasks")
        print(Fore.LIGHTWHITE_EX + "3. Mark Tasks As Done")
        print(Fore.LIGHTWHITE_EX + "4. Edit Tasks")
        print(Fore.LIGHTWHITE_EX + "5. Exit Program")
        print(25 * "─")

    elif menu_type == "edit_tasks_menu":
        print(Fore.LIGHTBLACK_EX + "Edit Tasks Menu")
        print(Style.BRIGHT + Fore.WHITE + "1. Edit Task Names")
        print(Fore.LIGHTWHITE_EX + "2. Edit Task Deadlines")
        print(Fore.LIGHTWHITE_EX + "3. Edit Task Priorities")
        print(Fore.LIGHTWHITE_EX + "4. Sort Tasks")
        print(Fore.LIGHTWHITE_EX + "5. Back")
        print(25 * "─")


# main menu options
ADD_TASKS = ["1", "add"]
DELETE_TASKS = ["2", "delete"]
MARK_TASKS_DONE = ["3", "mark tasks done"]
EDIT_TASKS = ["4", "edit tasks"]
MENU_EXIT = ["5", "exit"]

# edit tasks menu options
EDIT_TASK_NAMES = ["1", "edit task names"]
EDIT_TASK_DEADLINES = ["2", "edit task deadlines"]
EDIT_TASK_PRIORITIES = ["3", "edit task priorities"]
SORT_TASKS = ["4", "sort tasks"]
BACK = ["5", "back"]



# connects the user input to all the options, handles invalid input, and keeps track of which menu the user is on
def handle_choice(user_input):
    if current_menu == "main_menu":
        if user_input in ADD_TASKS:
            add_tasks()
        elif user_input in DELETE_TASKS:
            deleting()
        elif user_input in MARK_TASKS_DONE:
            marking_as_done()
        elif user_input in EDIT_TASKS:
            if not all_tasks_list:
                pause("Your to-do list is empty.")
            else:
                return "edit_tasks_menu"
        elif user_input in MENU_EXIT:
            exiting()
        else:
            pause("Invalid input")

        return "main_menu"

    elif current_menu == "edit_tasks_menu":
        if user_input in EDIT_TASK_NAMES:
            change_task_name()
        elif user_input in EDIT_TASK_DEADLINES:
            change_deadline()
        elif user_input in EDIT_TASK_PRIORITIES:
            change_priority()
        elif user_input in SORT_TASKS:
            task_sorting()
        elif user_input in BACK:
            return "main_menu"
        else:
            pause("Invalid input.")

        return "edit_tasks_menu"

#######################################################################################


### MAIN_MENU OPTIONS
def add_tasks():
    global all_tasks_list
    while True:
        display_top("Add a task (or press Enter to stop):")
        user_input = input(Fore.LIGHTWHITE_EX + "> ")
        if not user_input:
            clear_terminal()
            break

        task = {"name": "", "deadline": "", "priority": ""}
        all_tasks_list.append(task)

        task.update({"name": user_input})
        clear_terminal()

        task.update({"deadline": get_deadline()})
        clear_terminal()

        task.update({"priority": get_priority()})
        save_data()
        clear_terminal()

def get_deadline():
    today = datetime.today()

    while True:
        display_top("Task Details")
        print(Fore.LIGHTBLACK_EX + "Set a deadline (or press Enter for none):")
        print(Fore.LIGHTWHITE_EX + "1. Today")
        print(Fore.LIGHTWHITE_EX + "2. Tomorrow")
        print(Fore.LIGHTWHITE_EX + "3. Custom (MM/DD)")
        print(Fore.LIGHTBLACK_EX + "─" * 25)
        user_input = input(Fore.LIGHTWHITE_EX + "> ").strip()

        if user_input == "":
            return today + timedelta(9999)
        if user_input == "1":
            return today
        elif user_input == "2":
            return today + timedelta(1)
        elif user_input == "3":
            custom = input(Fore.LIGHTBLACK_EX + "Enter a date (MM/DD): ").strip()
            try:
                month, day = map(int, custom.split("/"))
                return datetime(today.year, month, day)
            except ValueError:
                pause("Invalid input. Please use MM/DD.")
        else:
            pause("Invalid input.")

def format_deadline(deadline):
    today = datetime.now()
    if not deadline:
        return ""

    if isinstance(deadline, str):
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return deadline  # fallback

    if deadline <= today + timedelta(-1):
        return Fore.RED + deadline.strftime("%b %d")
    elif deadline > today + timedelta(5000):
        return ""
    elif deadline <= today:
        return Fore.LIGHTWHITE_EX + "Today"
    elif deadline <= today + timedelta(1):
        return Fore.WHITE + "Tomorrow"
    else:
        return Fore.LIGHTBLACK_EX + deadline.strftime("%b %d")

def get_priority():
    while True:
        display_top("Task Details")
        print(Fore.LIGHTBLACK_EX + "How much priority? (or press Enter for none):")
        print(Fore.LIGHTWHITE_EX + "1. Low")
        print(Fore.LIGHTWHITE_EX + "2. Medium")
        print(Fore.LIGHTWHITE_EX + "3. High")
        print(Fore.LIGHTBLACK_EX + "─" * 25)
        user_input = input(Fore.LIGHTWHITE_EX + "> ").strip()

        if user_input == "":
            return ""

        if user_input == "1":
            return "!"
        elif user_input == "2":
            return "!!"
        elif user_input == "3":
            return "!!!"
        else:
            pause("Invalid input.")

def format_priority(priority):
    if not priority:
        return ""

    if priority == "!":
        return Fore.LIGHTYELLOW_EX + "!"
    elif priority == "!!":
        return Fore.YELLOW + "!!"
    elif priority == "!!!":
        return Fore.LIGHTRED_EX + "!!!"



def deleting():
    global all_tasks_list, marked_done
    if not all_tasks_list:
        pause("Your to-do list is empty.")

    else:
        while True:
            display_top("Delete by number or name.\nType \"clear\" to remove all.\nPress Enter to stop.")
            user_input = input(Fore.LIGHTWHITE_EX + "> ")

            if user_input.isdigit():
                index = int(user_input)
                if 0 < index <= len(all_tasks_list):
                    all_tasks_list.pop(index - 1)
                    marked_done = [i for i in marked_done if i != index - 1]
                    save_data()
                    clear_terminal()
                else:
                    pause("Invalid number.")
            elif user_input.lower() == "clear":
                all_tasks_list.clear()
                marked_done.clear()
                save_data()
                pause("To-do list cleared.")
            elif any(task["name"] == user_input for task in all_tasks_list):
                index_to_remove = next(i for i, task in enumerate(all_tasks_list) if task["name"] == user_input)
                all_tasks_list.pop(index_to_remove)
                save_data()
                clear_terminal()
            elif not user_input:
                clear_terminal()
                break
            else:
                pause(f"\"{user_input}\" not found in your to-do list.")

            if not all_tasks_list:
                clear_terminal()
                break


def marking_as_done():
    if not all_tasks_list:
        pause("Your to-do list is empty.")
    else:
        while True:
            display_top("Mark task done (by number or name).\nPress Enter to stop.")
            user_input = input(Fore.LIGHTWHITE_EX + "> ")
            if not user_input:
                clear_terminal()
                break
            if user_input.isdigit():
                index = int(user_input) - 1
                if 0 <= index < len(all_tasks_list):
                    if index in marked_done:
                        marked_done.remove(index)
                    else:
                        marked_done.append(index)
                    save_data()
                    clear_terminal()
                else:
                    pause("Invalid number.")
            elif user_input in all_tasks_list:
                index = all_tasks_list.index(user_input)
                if index in marked_done:
                    marked_done.remove(index)
                else:
                    marked_done.append(index)
                save_data()
                clear_terminal()
            else:
                pause("Invalid input.")

def exiting():
    while True:
        print(Fore.LIGHTWHITE_EX + "Are you sure you want to exit? (yes/no)")
        user_input = input(Fore.LIGHTWHITE_EX + "> ").lower()
        if user_input in ["yes", "y"]:
            if all_tasks_list:
                save_choice = input(Fore.LIGHTWHITE_EX + "Save your to-do list? (yes/no)\n> ")
                if save_choice.lower() == "no":
                    all_tasks_list.clear()
                    marked_done.clear()
                    save_data()
                    pause("To-do list cleared.")
                else:
                    pause("To-do list saved.")
            print(Fore.LIGHTGREEN_EX + "Closing to-do list app...")
            time.sleep(1)
            exit()
        elif user_input in ["no", "n"]:
            break
        else:
            pause("Invalid input. (Type \"yes\" or \"no\")")

#######################################################################################

### OPTIONS EDIT MENU

def change_task_name():
    while True:
        display_top("Which task name would like to change? (select by number).\nPress Enter to stop.")
        user_input = input("> ").strip()
        clear_terminal()
        if not user_input:
            break

        if user_input.isdigit():
            idx = int(user_input) - 1

            if 0 <= idx < len(all_tasks_list):
                while True:
                    display_top(
                        Fore.LIGHTBLACK_EX + f"Change \"{all_tasks_list[idx]["name"]}\" to what?\nPress Enter twice to cancel.")
                    user_input = input(Fore.LIGHTWHITE_EX + "> ")

                    if not user_input:
                        clear_terminal()
                        break

                    all_tasks_list[idx]["name"] = user_input
                    save_data()
                    clear_terminal()
                    break




            else:
                pause("Invalid input.")
        else:
            pause("Invalid input.")


def change_deadline():
    while True:
        display_top("Which task's deadline would like to change? (select by number).\nPress Enter to stop.")
        user_input = input("> ").strip()
        clear_terminal()
        if not user_input:
            break

        if user_input.isdigit():

            idx = int(user_input) - 1
            if 0 <= idx < len(all_tasks_list):

                all_tasks_list[idx]["deadline"] = get_deadline()
                save_data()
                clear_terminal()
            else:
                pause("Invalid input.")

        else:
            pause("Invalid input.")





def change_priority():
    while True:
        display_top("Which task's priority would you like to change? (select by number)\nPress Enter to stop.")
        user_input = input("> ").strip()
        clear_terminal()

        if not user_input:
            break

        if user_input.isdigit():

            idx = int(user_input) - 1

            if 0 <= idx < len(all_tasks_list):

                all_tasks_list[idx]["priority"] = get_priority()
                save_data()
                clear_terminal()
            else:
                pause("Invalid input.")

        else:
            pause("Invalid Input.")



def task_sorting():
    global all_tasks_list
    while True:
        display_top("Tasks Sorting")
        print(Fore.LIGHTBLACK_EX + "What would you like to sort by? (or press Enter for none):")
        print(Fore.LIGHTWHITE_EX + "1. Alphabetic")
        print(Fore.LIGHTWHITE_EX + "2. Earliest Deadline")
        print(Fore.LIGHTWHITE_EX + "3. Highest Priority")
        print(Fore.LIGHTWHITE_EX + "4. Manually")
        print(Fore.LIGHTBLACK_EX + "─" * 25)
        user_input = input(Fore.LIGHTWHITE_EX + "> ").strip()

        if user_input == "":
            return ""

        if user_input == "1":
            all_tasks_list = sorted(all_tasks_list, key=lambda task: task["name"])
        elif user_input == "2":
            all_tasks_list = sorted(all_tasks_list, key=lambda task: task["deadline"])
        elif user_input == "3":
            all_tasks_list = sorted(all_tasks_list, key=lambda task: task["priority"], reverse=True)
        elif user_input == "4":
            clear_terminal()
            change_order()
        else:
            pause("Invalid input.")
        save_data()
        clear_terminal()
        break

def change_order():
    if not all_tasks_list:
        pause("Your to-do list is empty.")
    else:
        while True:
            display_top("Move a task (select by number).\nPress Enter to stop.")
            user_input = input(Fore.LIGHTWHITE_EX + "> ")
            if not user_input:
                clear_terminal()
                break
            if user_input.isdigit():
                index = int(user_input) - 1
                clear_terminal()
                if 0 <= index < len(all_tasks_list):
                    while True:
                        display_top(Fore.LIGHTBLACK_EX + f"Move \"{all_tasks_list[index]["name"]}\" to what position?\nPress Enter twice to cancel.")

                        user_input = input(Fore.LIGHTWHITE_EX + "> ")
                        if not user_input:
                            clear_terminal()
                            break
                        if user_input.isdigit():
                            user_input = int(user_input) - 1
                            if 0 <= user_input < len(all_tasks_list):
                                task = all_tasks_list.pop(index)
                                all_tasks_list.insert(user_input, task)
                                clear_terminal()
                                break
                            else:
                                pause("Invalid position.")
                        else:
                            pause("Invalid input.")
                else:
                    pause("Invalid number.")
            else:
                pause("Invalid input.")

#######################################################################################

### Other

# 01 / 05 / 2025
def random_quote():
    quotes = ["“Amateurs sit and wait for inspiration, the rest of us just get up and go to work.” — Stephen King",

              "“Don’t watch the clock; do what it does. Keep going.” — Sam Levenson",

              "“Productivity is never an accident. It is always the result of a commitment to excellence, intelligent planning, and focused effort.” — Paul J. Meyer",

              "“The way to get started is to quit talking and begin doing.” — Walt Disney",

              "“Focus on being productive instead of busy.” — Tim Ferriss",

              "“You don’t have to be extreme, just consistent.” — Unknown",

              "“It’s not always that we need to do more but rather that we need to focus on less.” — Nathan W. Morris",

              "“Your future is created by what you do today, not tomorrow.” — Robert Kiyosaki",

              "“Ordinary people think merely of spending time, great people think of using it.” — Arthur Schopenhauer",

              "“Action is the foundational key to all success.” — Pablo Picasso",

              "“Lost time is never found again.” — Benjamin Franklin",

              "“Small daily improvements over time lead to stunning results.” — Robin Sharma",

              "“What gets measured gets managed.” — Peter Drucker",

              "“Start where you are. Use what you have. Do what you can.” — Arthur Ashe",

              "“Nothing will work unless you do.” — Maya Angelou",

              "“Success is the sum of small efforts repeated day in and day out.” — Robert Collier",

              "“The secret of getting ahead is getting started.” — Mark Twain",

              "“Never mistake motion for action.” — Ernest Hemingway",

              "“Simplicity boils down to two steps: Identify the essential. Eliminate the rest.” — Leo Babauta",

              "“Dream big. Start small. Act now.” — Robin Sharma"]

    return Fore.WHITE + random.choice(quotes)


# function to clear the terminal for design purposes
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


# function used for the start-up screen
def scrolling_text(sentence):
    for character in sentence:
        sys.stdout.write(Fore.LIGHTBLACK_EX + character)
        sys.stdout.flush()
        time.sleep(0.01)


# function used after invalid inputs
def pause(message):
    if message:
        print(Fore.LIGHTRED_EX + message)
    input(Fore.LIGHTWHITE_EX + "\nPress \"Enter\" to continue.")
    clear_terminal()


########################################################################################################################


application()
