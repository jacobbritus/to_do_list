import pickle
import os

from colorama import init, Fore, Style
init(autoreset=True)




# main menu
def application():
    while True:
        ###############################################
        if len(to_do_list) == len(marked_done):
            user_interface("You have completed all your tasks!")
        else:
            user_interface("Don't forget to complete your tasks!")
        ###############################################
        display_menu()
        choice = input("> ").strip().lower()
        clear_terminal()

        handle_choice(choice)
        clear_terminal()




# function to add to to-do list
def adding():
    global to_do_list

    while True:
        user_interface("Add something to your to-do list.\nPress \"Enter\" to stop adding.")
        add = input("> ")

        if add:
            to_do_list.append(add)
            save_list()  # saves added item
            clear_terminal()

        else:
            clear_terminal()
            break




def marking_as_done():
    global to_do_list
    global marked_done

    if not to_do_list:
        pause("Your to-do list is empty.")
        clear_terminal()

    else:
        while True:
            user_interface("Which task (number or name) would you like to mark as done?.\nPress \"Enter\" to stop marking as done.")
            done = input("> ")

            if not done:
                clear_terminal()
                break

            # if user types a number
            if done.isdigit():
                index = int(done) - 1  # user sees 1,2,3... but python uses 0,1,2...
                if 0 <= index < len(to_do_list):
                    if index in marked_done:
                        marked_done.remove(index)
                    else:
                        marked_done.append(index)
                    save_list()
                    clear_terminal()
                else:
                    pause("Invalid input. (number out of range)")

            # if user types a task name
            elif done in to_do_list:
                index = to_do_list.index(done)  # find the task's position
                if index in marked_done:
                    marked_done.remove(index)
                else:
                    marked_done.append(index)
                save_list()
                clear_terminal()

            # If input is invalid
            else:
                pause("Invalid input.")


# function to delete from to-do list
def deleting():
    global to_do_list
    global marked_done

    while True:
        if not to_do_list:
            pause("Your to-do list is empty.")
            clear_terminal()
            break
        else:
            user_interface("Delete something from your to-do list.\nType \"clear\" to clear your to-do list.\nPress \"Enter\" to stop deleting.")
            delete = input("> ")

            # deleting using number order
            if delete.isdigit():
                index_delete = int(delete)

                if 0 < index_delete <= len(to_do_list):
                    clear_terminal()
                    to_do_list.pop(index_delete - 1)

                    if index_delete - 1 in marked_done:
                        marked_done.pop(index_delete - 1)

                    clear_terminal()
                    save_list()
                else:
                    clear_terminal()
                    pause(f"Your to-do list doesn't have include number \"{index_delete}\".")

            # option to clear to-do list
            elif delete.lower() == "clear":
                to_do_list.clear()
                save_list()
                pause("Your to-do list was cleared.")

            # deleting using to-do list task names
            elif delete and not delete.isdigit() and delete != "CLEAR":
                if not delete in to_do_list:
                    clear_terminal()
                    pause(f"\"{delete}\" was not found in your to-do_list.")
                else:
                    to_do_list.remove(delete)
                    save_list()
                    clear_terminal()

            # closes deleting function if no input is given
            else:
                clear_terminal()
                break


def change_order():
    global to_do_list

    if not to_do_list:
        pause("Your to-do list is empty.")

    else:
        while True:
            user_interface("Pick an item you would like to change order.\nPress \"Enter\" to stop changing number order.")
            item_to_replace = input("> ")

            if not item_to_replace:
                clear_terminal()
                break

            if item_to_replace.isdigit():
                item_to_replace = int(item_to_replace) - 1

                clear_terminal()
                if 0 <= item_to_replace < len(to_do_list):
                    while True:
                        user_interface(f"At which number do you want to put \"{to_do_list[item_to_replace]}\"?\nPress \"Enter\" twice to go one step back.")
                        edit = input("> ")

                        if not edit:
                            clear_terminal()
                            break

                        if edit.isdigit():
                            edit = int(edit) - 1

                            if 0 <= edit < len(to_do_list):
                                change = to_do_list[item_to_replace]
                                to_do_list.remove(change)
                                to_do_list.insert(edit, change)
                                clear_terminal()
                                break

                            else:
                                pause("Invalid input")



                        else:
                            pause("Invalid input")
            else:
                pause("Invalid input.")






# function for vertical to-do list
def vertical_list():
    global to_do_list
    if not to_do_list:
        print("Your to-do list is empty, add some things!")
    for index, task in enumerate(to_do_list):
        if index in marked_done:
            print(f"[x] {index + 1}. {task}")
        else:
            print(f"[ ]  {index + 1}. {task}")


# function for to-do list design
def user_interface(function):
    print("TO-DO LIST")
    print(function)
    print("-" * 30)
    vertical_list()
    print("-" * 30)


# file for saving and loading
FILE_NAME = "to_do_list4.pkl"

# function that tries to load to-do list from file
def load_list():
    try:
        with open(FILE_NAME, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return [], []

# function to save to-do list to a file
def save_list():
    try:
        with open(FILE_NAME, "wb") as f:
            pickle.dump((to_do_list, marked_done), f)
    except Exception as e:
        print(f"Error saving file: {e}")


to_do_list, marked_done = load_list()


# welcome message and old to-do list if data was loaded
def welcome_back():
    if to_do_list:
        user_interface("Welcome back! You left some tasks in your to-do list.")
        pause("")


# function for clearing terminal
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


# function for pausing
def pause(message):
    if message:
        print(message)
    input("\nPress \"Enter\" to continue.")
    clear_terminal()



def exiting():
    while True:
        print("Are you sure you want to exit?")

        confirm = input("> ").lower()

        if confirm in ["yes", "yeah", "yea", "sure"]:
            if to_do_list:
                save_data = input("Would you like to save your to-do list?\n>")
                if save_data in ["No", "no"]:
                    to_do_list.clear()
                    save_list()
                    pause("Your to-do list was cleared.")

                else:
                    pause("Your to-do list was saved.")

            print("Closing to-do list app.")
            time.sleep(2)
            exit()
        elif confirm in ["no", 'nah']:
            break
        else:
            pause("Invalid input (Enter \"Yes\" or \"No\").")


#improving the main menu, constants
MENU_ADD = ["1", "add"]
MENU_DELETE = ["2", "delete"]
MENU_REORDER = ["3", "reorder"]
MENU_MARK_DONE = ["4", "mark as done"]
MENU_EXIT = ["5", "exit"]


def display_menu():
    print("1. Add Tasks")
    print("2. Delete Tasks")
    print("3. Reorder Tasks")
    print("4. Mark Tasks As Done")
    print("5. Exit")
    print("-" * 30)

def handle_choice(choice):
    choice = choice.lower()
    if choice in MENU_ADD:
        adding()
    elif choice in MENU_DELETE:
        deleting()
    elif choice in MENU_REORDER:
        change_order()
    elif choice in MENU_MARK_DONE:
        marking_as_done()
    elif choice in MENU_EXIT:
        exiting()
    else:
        pause("Invalid input")


welcome_back()
application()