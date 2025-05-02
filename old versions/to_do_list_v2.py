# simple to do list
# 25 / 02 / 2025
import time

to_do_list = []


# main menu with options like adding, deleting, viewing and exiting the application
# goes back to the main menu if input doesn't align with the options
def application():
    choice = input("\nTO-DO LIST - MAIN MENU\n-------------------------\n1. Add to list\n2. Delete from list\n3. View list\n4. Exit Program\n-------------------------\n> ")
    clear_terminal()
    if choice in ["1", "Add", "add", "Add to list"]:
        adding()
    elif choice in ["2", "delete", "Delete", "Delete from list"]:
        deleting()
    elif choice in ["3", "view", "View", "View list"]:
        viewing()
    elif choice in ["4", "exit", "Exit", "Exit program"]:
        print("Closing to-do list app.")
        time.sleep(2)
        exit()
    else:
        print("Invalid input.\n")
        time.sleep(1)
    application()


# adds given input, prints input was added to list
# main menu if not input is given
def adding():
    tasks()
    add = input("Add something to your to-do list. Press \"Enter\" to stop adding.\n> ")
    if not add == "":
        to_do_list.append(add)
        print(f"\"{add}\" was added to your to-do_list.\n")
        time.sleep(2)
        clear_terminal()
        adding()
    clear_terminal()


# deletes given input, prints input was deleted from list
# main menu if list is empty or no input is given
# resets function if input not in list, prints input wasn't found
def deleting():
    if to_do_list == []:
        input("Your to-do list is empty. Press \"Enter\" to continue.")
        clear_terminal()
    else:
        tasks()
        delete = input("Delete something from your to-do list. Press \"Enter\" to stop deleting.\n> ")
        if not delete in ["", to_do_list]:
            if not delete in to_do_list:
                print(f"\"{delete}\" was not found in your to-do_list.\n")
                time.sleep(2)
                deleting()
            to_do_list.remove(delete)
            print(f"\"{delete}\" was deleted from your to-do_list.\n")
            time.sleep(2)
            clear_terminal()
            deleting()
        clear_terminal()

# prints to do list
# enter to continue
# prints list is empty if list is empty
def viewing():
    if to_do_list == []:
        input("Your to-do list is empty. Press \"Enter\" to continue.")
    else:
        tasks()
        input("Press \"Enter\" to continue.")


# vertical listing
def vertical_list():
    for task in to_do_list:
        print(task)


def tasks():
    print("\nTO-DO LIST\n-------------------------")
    vertical_list()
    print("-------------------------")

#clearing terminal
import os
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")



application()

# log

# 25 / 02 / 2025
# I decided to improve this script from what it was first, as I learnt more stuff and wanted to improve my proficiency.
# I changed everything - main menu, adding, removing, viewing, and exiting the program. I've made it more user-friendly

#26 / 02 / 2025
#made the to-do list print vertically as individual strings to improve design