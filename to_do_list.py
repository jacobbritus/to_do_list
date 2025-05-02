import time
import random
import pickle
import os
import sys
from datetime import datetime, timedelta
from colorama import init, Fore, Style


init(autoreset=True)

FILE_NAME = "to_do_list.pkl"
to_do_list, marked_done = [], []

def load_list():
    try:
        with open(FILE_NAME, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return [], []

def save_data():
    try:
        with open(FILE_NAME, "wb") as file:
            pickle.dump((to_do_list, marked_done), file)
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error saving file: {e}")

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def scrolling_text(sentence):
    for character in sentence:
        sys.stdout.write(Fore.LIGHTBLACK_EX + character)
        sys.stdout.flush()
        time.sleep(0.01)

def pause(message):
    if message:
        print(Fore.LIGHTRED_EX + message)
    input(Fore.LIGHTWHITE_EX + "\nPress \"Enter\" to continue.")
    clear_terminal()

def format_deadline(deadline):
    today = datetime.now()
    if not deadline:
        return ""

    if isinstance(deadline, str):
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return deadline # fallback

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

def format_priority(priority):
    if not priority:
        return ""

    if priority == "!":
        return Fore.LIGHTYELLOW_EX + "!"
    elif priority == "!!":
        return Fore.YELLOW + "!!"
    elif priority == "!!!":
        return Fore.LIGHTRED_EX + "!!!"


def vertical_list():
    print("TASK NAME                 DEADLINE                        PRIORITY")
    print(Fore.LIGHTBLACK_EX + "─" * 66)
    if not to_do_list:
        print(Fore.LIGHTBLACK_EX + "Your to-do list is empty, add some tasks!")
        print(Fore.LIGHTBLACK_EX + "─" * 66)


    for index, task in enumerate(to_do_list):
        name = task["name"]
        deadline = format_deadline(task["deadline"])
        priority = format_priority(task["priority"])
        task_color = Fore.WHITE if index % 2 == 0 else Fore.LIGHTWHITE_EX
        whitespace1 = " " * (18 - len(name))
        # whitespace2 = " " * 36 - len(deadline) if task["deadline"] else " " * 31 - 0

        whitespace2 = " " * (31 - 0) if not task["deadline"] else " " * (36 - len(deadline))

        # whitespace2 = " " * (36 - len(deadline))

        if index in marked_done:
            print(Fore.LIGHTGREEN_EX + f"[x] {index + 1}. {name} {whitespace1} {deadline} {whitespace2} {priority}")
        else:
            print(task_color + f"[ ] {index + 1}. {name} {whitespace1} {deadline} {whitespace2} {priority}")

        print(Fore.LIGHTBLACK_EX + "─" * 66)


def logo():
    return r"""
 __  __         _____         _        
|  \/  |_   _  |_   _|_ _ ___| | _____ 
| |\/| | | | |   | |/ _` / __| |/ / __|
| |  | | |_| |   | | (_| \__ \   <\__ \
|_|  |_|\__, |   |_|\__,_|___/_|\_\___/
        |___/                   
"""

def user_interface(message):
    print(Fore.LIGHTBLACK_EX + logo())
    if message:
        print(Style.BRIGHT + Fore.LIGHTBLACK_EX + message)
    print(Fore.LIGHTBLACK_EX + "─" * 66)
    vertical_list()

def adding():
    global to_do_list
    while True:
        user_interface("Add a task (or press Enter to stop):")
        task_name = input(Fore.LIGHTWHITE_EX + "> ")
        if not task_name:
            clear_terminal()
            break



        task = {"name": "", "deadline": "", "priority": ""}
        to_do_list.append(task)
        task.update({"name": task_name})
        clear_terminal()
        task.update({"deadline": get_deadline()})
        clear_terminal()
        task.update({"priority": get_priority()})
        save_data()
        clear_terminal()


def marking_as_done():
    if not to_do_list:
        pause("Your to-do list is empty.")
    else:
        while True:
            user_interface("Mark task done (by number or name).\nPress Enter to stop.")
            done = input(Fore.LIGHTWHITE_EX + "> ")
            if not done:
                clear_terminal()
                break
            if done.isdigit():
                index = int(done) - 1
                if 0 <= index < len(to_do_list):
                    if index in marked_done:
                        marked_done.remove(index)
                    else:
                        marked_done.append(index)
                    save_data()
                    clear_terminal()
                else:
                    pause("Invalid number.")
            elif done in to_do_list:
                index = to_do_list.index(done)
                if index in marked_done:
                    marked_done.remove(index)
                else:
                    marked_done.append(index)
                save_data()
                clear_terminal()
            else:
                pause("Invalid input.")

def deleting():
    global to_do_list, marked_done
    if not to_do_list:
        pause("Your to-do list is empty.")

    else:
        while True:
            user_interface("Delete by number or name.\nType \"clear\" to remove all.\nPress Enter to stop.")
            delete = input(Fore.LIGHTWHITE_EX + "> ")

            if delete.isdigit():
                index = int(delete)
                if 0 < index <= len(to_do_list):
                    to_do_list.pop(index - 1)
                    marked_done = [i for i in marked_done if i != index - 1]
                    save_data()
                    clear_terminal()
                else:
                    pause("Invalid number.")
            elif delete.lower() == "clear":
                to_do_list.clear()
                marked_done.clear()
                save_data()
                pause("To-do list cleared.")
            elif any(task["name"] == delete for task in to_do_list):
                index_to_remove = next(i for i, task in enumerate(to_do_list) if task["name"] == delete)
                to_do_list.pop(index_to_remove)
                save_data()
                clear_terminal()
            elif not delete:
                clear_terminal()
                break
            else:
                pause(f"\"{delete}\" not found in your to-do list.")

            if not to_do_list:
                clear_terminal()
                break





def change_order():
    if not to_do_list:
        pause("Your to-do list is empty.")
    else:
        while True:
            user_interface("Move a task (select by number).\nPress Enter to stop.")
            item = input(Fore.LIGHTWHITE_EX + "> ")
            if not item:
                clear_terminal()
                break
            if item.isdigit():
                idx = int(item) - 1
                clear_terminal()
                if 0 <= idx < len(to_do_list):
                    while True:
                        user_interface(Fore.LIGHTBLACK_EX + f"Move \"{to_do_list[idx]["name"]}\" to what position?\nPress Enter twice to cancel.")
                        new_pos = input(Fore.LIGHTWHITE_EX + "> ")
                        if not new_pos:
                            clear_terminal()
                            break
                        if new_pos.isdigit():
                            new_pos = int(new_pos) - 1
                            if 0 <= new_pos < len(to_do_list):
                                task = to_do_list.pop(idx)
                                to_do_list.insert(new_pos, task)
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

def exiting():
    while True:
        print(Fore.LIGHTWHITE_EX + "Are you sure you want to exit? (yes/no)")
        confirm = input(Fore.LIGHTWHITE_EX + "> ").lower()
        if confirm in ["yes", "y"]:
            if to_do_list:
                save_choice = input(Fore.LIGHTWHITE_EX + "Save your to-do list? (yes/no)\n> ")
                if save_choice.lower() == "no":
                    to_do_list.clear()
                    marked_done.clear()
                    save_data()
                    pause("To-do list cleared.")
                else:
                    pause("To-do list saved.")
            print(Fore.LIGHTGREEN_EX + "Closing to-do list app...")
            time.sleep(1)
            exit()
        elif confirm in ["no", "n"]:
            break
        else:
            pause("Invalid input. (Type \"yes\" or \"no\")")

def start_up_screen():
    scrolling_text(logo())
    pause(None)

#main menu
MENU_ADD = ["1", "add"]
MENU_DELETE = ["2", "delete"]
MENU_EDIT = ["3", "edit"]
MENU_MARK_DONE = ["4", "mark as done"]
MENU_EXIT = ["5", "exit"]

#edit menu
MENU_CHANGE_NAME = ["1", "change name"]
MENU_CHANGE_DEADLINE = ["2", "change priority"]
MENU_CHANGE_PRIORITY = ["3", "change name"]
MENU_SORT_TASKS = ["4", "sort tasks"]
MENU_EXIT_EDIT = ["5", "back"]

def display_menu_options(menu_type):
    if menu_type == "main_menu":
        print(Fore.LIGHTBLACK_EX + "Main Menu")
        print(Style.BRIGHT + Fore.WHITE + "1. Add Tasks")
        print(Fore.LIGHTWHITE_EX + "2. Delete Tasks")
        print(Fore.LIGHTWHITE_EX + "3. Edit Tasks")
        print(Fore.LIGHTWHITE_EX + "4. Mark Tasks As Done")
        print(Fore.LIGHTWHITE_EX + "5. Exit Program")
        print(Fore.LIGHTBLACK_EX + "─" * 25)

    elif menu_type == "edit_menu":
        print(Fore.LIGHTBLACK_EX + "Edit Menu")
        print(Style.BRIGHT + Fore.WHITE + "1. Change Task Name")
        print(Fore.LIGHTWHITE_EX + "2. Change Deadline")
        print(Fore.LIGHTWHITE_EX + "3. Change Priority")
        print(Fore.LIGHTWHITE_EX + "4. Sort Tasks")
        print(Fore.LIGHTWHITE_EX + "5. Back")
        print(Fore.LIGHTBLACK_EX + "─" * 25)


def handle_choice(choice):
    global to_do_list

    choice = choice.lower()

    if current_menu == "main_menu":

        if choice in MENU_ADD:
            adding()
        elif choice in MENU_DELETE:
            deleting()
        elif choice in MENU_EDIT:
            if not to_do_list:
                pause("Your to-do list is empty.")
            else:
                return "edit_menu"
        elif choice in MENU_MARK_DONE:
                marking_as_done()
        elif choice in MENU_EXIT:
                exiting()
        else:
            pause("Invalid input")
        return "main_menu"

    elif current_menu == "edit_menu":
        if choice in MENU_CHANGE_NAME:
            change_task_name()
        elif choice in MENU_CHANGE_DEADLINE:
            change_deadline()
        elif choice in MENU_CHANGE_PRIORITY:
            change_priority()
        elif choice in MENU_SORT_TASKS:
            task_sorting()
        elif choice in MENU_EXIT_EDIT:
            return "main_menu"
        else:
            pause("Invalid input.")
        return "edit_menu"





def application():
    global to_do_list, marked_done, current_menu
    to_do_list, marked_done = load_list()

    # start_up_screen()

    current_menu = "main_menu"

    while True:

        user_interface(random_quote())
        display_menu_options(current_menu)


        choice = input(Fore.LIGHTWHITE_EX + "> ").strip().lower()

        clear_terminal()
        next_menu = handle_choice(choice)
        current_menu = next_menu
        clear_terminal()



def get_deadline():

    today = datetime.today()

    while True:
        user_interface("Task Details")
        print(Fore.LIGHTBLACK_EX + "Set a deadline (or press Enter for none):")
        print(Fore.LIGHTWHITE_EX + "1. Today")
        print(Fore.LIGHTWHITE_EX + "2. Tomorrow")
        print(Fore.LIGHTWHITE_EX + "3. Custom (MM/DD)")
        print(Fore.LIGHTBLACK_EX + "─" * 25)
        choice = input(Fore.LIGHTWHITE_EX + "> ").strip()

        if choice == "":
            return today + timedelta(9999)
        if choice == "1":
            return today
        elif choice == "2":
            return today + timedelta(1)
        elif choice == "3":
            custom = input(Fore.LIGHTBLACK_EX + "Enter a date (MM/DD): ").strip()
            try:
                month, day = map(int, custom.split("/"))
                return datetime(today.year, month, day)
            except ValueError:
                pause("Invalid input. Please use MM/DD.")
        else:
            pause("Invalid input.")





#new features
########################################################################################################################
#30 / 04 / 2025
def change_task_name():
    while True:
        user_interface("Which task name would like to change? (select by number).\nPress Enter to stop.")
        selected_task = input("> ").strip()
        clear_terminal()
        if not selected_task:
            break

        if selected_task.isdigit():
            idx = int(selected_task) - 1


            if 0 <= idx < len(to_do_list):
                while True:
                    user_interface(Fore.LIGHTBLACK_EX + f"Change \"{to_do_list[idx]["name"]}\" to what?\nPress Enter twice to cancel.")
                    new_name = input(Fore.LIGHTWHITE_EX + "> ")

                    if not new_name:
                        clear_terminal()
                        break

                    to_do_list[idx]["name"] = new_name
                    save_data()
                    clear_terminal()
                    break




            else:
                pause("Invalid input.")
        else:
            pause("Invalid input.")








def change_deadline():
    while True:
        user_interface("Which task's deadline would like to change? (select by number).\nPress Enter to stop.")
        selected_task = input("> ").strip()
        clear_terminal()
        if not selected_task:
            break

        if selected_task.isdigit():


            idx = int(selected_task) - 1
            if 0 <= idx < len(to_do_list):

                to_do_list[idx]["deadline"] = get_deadline()
                save_data()
                clear_terminal()
            else:
                pause("Invalid input.")

        else:
            pause("Invalid input.")



def get_priority():
    while True:
        user_interface("Task Details")
        print(Fore.LIGHTBLACK_EX + "How much priority? (or press Enter for none):")
        print(Fore.LIGHTWHITE_EX + "1. Low")
        print(Fore.LIGHTWHITE_EX + "2. Medium")
        print(Fore.LIGHTWHITE_EX + "3. High")
        print(Fore.LIGHTBLACK_EX + "─" * 25)
        choice = input(Fore.LIGHTWHITE_EX + "> ").strip()


        if choice == "":
            return ""

        if choice == "1":
            return "!"
        elif choice == "2":
            return "!!"
        elif choice == "3":
            return "!!!"
        else:
            pause("Invalid input.")



def change_priority():
    while True:
        user_interface("Which task's priority would you like to change? (select by number)\nPress Enter to stop.")
        selected_task = input("> ").strip()
        clear_terminal()
        
        if not selected_task:
            break
        
        if selected_task.isdigit():
            
            idx = int(selected_task) - 1

            if 0 <= idx < len(to_do_list):
            
                to_do_list[idx]["priority"] = get_priority()
                save_data()
                clear_terminal()
            else:
                pause("Invalid input.")
        
        else:
            pause("Invalid Input.")
                


#01 / 05 / 2025
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



#02 / 05 / 2025
def task_sorting():
    global to_do_list
    while True:
        user_interface("Tasks Sorting")
        print(Fore.LIGHTBLACK_EX + "What would you like to sort by? (or press Enter for none):")
        print(Fore.LIGHTWHITE_EX + "1. Alphabetic")
        print(Fore.LIGHTWHITE_EX + "2. Earliest Deadline")
        print(Fore.LIGHTWHITE_EX + "3. Highest Priority")
        print(Fore.LIGHTWHITE_EX + "4. Manually")
        print(Fore.LIGHTBLACK_EX + "─" * 25)
        choice = input(Fore.LIGHTWHITE_EX + "> ").strip()


        if choice == "":
            return ""

        if choice == "1":
            to_do_list = sorted(to_do_list, key=lambda task:task["name"])
        elif choice == "2":
            to_do_list = sorted(to_do_list, key=lambda task:task["deadline"])
        elif choice == "3":
            to_do_list = sorted(to_do_list, key=lambda task:task["priority"], reverse=True)
        elif choice == "4":
            clear_terminal()
            change_order()
        else:
            pause("Invalid input.")
        save_data()
        clear_terminal()
        break



########################################################################################################################




application()

