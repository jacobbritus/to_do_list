import time
import pickle
import os

# main menu
def application():
        tasks("Welcome!")
        choice = input("1. Add\n2. Delete\n3. Change Order\n4. Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~\n> ").lower()
        clear_terminal()

        if choice in ["1", "add"]:
            adding()

        elif choice in ["2", "delete"]:
            deleting()

        elif choice in ["3", "change order"]:
            change_order()

        elif choice in ["4", "exit"]:
            saving()
            print("Closing to-do list app.")
            time.sleep(2)
            exit()

        else:
            input("Invalid input.\nPress \"Enter\" to stop adding.")
            clear_terminal()
            application()


# function to add to to-do list
def adding():
    tasks("Add something to your to-do list.\nPress \"Enter\" to stop adding.")
    add = input("> ")

    if add:
        to_do_list.append(add)
        save_list() # saves added item
        clear_terminal()
        input(f"\"{add}\" was added to your to-do_list.\nPress \"Enter\" to continue.\n")
        clear_terminal()
        adding()
    else:
        clear_terminal()
        application()



# function to delete from to-do list
def deleting():
    if not to_do_list:
        input("Your to-do list is empty.\nPress \"Enter\" to continue.")
    else:
        tasks("Delete something from your to-do list.\nType \"CLEAR\" to clear your to-do list.\nPress \"Enter\" to stop deleting.")

        # deleting using number order
        delete = input("> ")
        if delete.isdigit():
            index_delete = int(delete)
            if 0 < index_delete <= len(to_do_list):
                input(f"\"{to_do_list[index_delete - 1]}\" was deleted from your to-do_list.\nPress \"Enter\" to continue.\n")
                to_do_list.pop(index_delete - 1)
                save_list()
            else:
                input(f"Your to-do list doesn't have include number \"{index_delete}\" .\nPress \"Enter\" to continue.\n")

        # option to clear to-do list
        if delete == "CLEAR":
            to_do_list.clear()
            save_list()
            input("Your to-do list was cleared.\nPress \"Enter\" to continue.")

        #deleting using to-do list task names
        if delete and not delete.isdigit() and delete != "CLEAR":
            if not delete in to_do_list:
                input(f"\"{delete}\" was not found in your to-do_list.\nPress \"Enter\" to continue.\n")
                clear_terminal()
                deleting()
            to_do_list.remove(delete)
            save_list()
            input(f"\"{delete}\" was deleted from your to-do_list.\nPress \"Enter\" to continue.\n")


        #closes deleting function if no input is given
        if delete == "":
            clear_terminal()
            application()

        clear_terminal()
        deleting()

def change_order():
    global edit
    if not to_do_list:
        input("Your to-do list is empty.\nPress \"Enter\" to continue.")

    else:
        editing = True
        while editing:
            tasks("Pick an item you would like to change order.\nPress \"Enter\" to stop changing order.")
            picked_item = input("> ")


            if picked_item == "":
                break

            while not picked_item.isdigit():
                input("Invalid input.\nPress \"Enter\" to continue.\n")
                clear_terminal()
                tasks("Pick an item you would like to change order.\nPress \"Enter\" to stop changing order.")
                picked_item = input("> ")

            else:
                picked_item = int(picked_item)
                picked_item -= 1

                while picked_item > len(to_do_list) or picked_item < 0:
                    input("Invalid input.\nPress \"Enter\" to continue.\n")
                    clear_terminal()
                    tasks("Pick an item you would like to change order.\nPress \"Enter\" to stop changing order.")
                    picked_item = input("> ")




                edit = input("At which number would you like to put it?\n> ")

                while not edit.isdigit():
                    input("Invalid input.\nPress \"Enter\" to continue.\n")
                    clear_terminal()
                    tasks("At which number would you like to put it?")
                    edit = input("> ")

                edit = int(edit) - 1



                while edit > len(to_do_list) or edit < 0:
                    input("Invalid input.\nPress \"Enter\" to continue.\n")
                    clear_terminal()
                    tasks("At which number would you like to put it?")
                    edit = input("> ")

                change = to_do_list[picked_item]
                to_do_list.remove(change)
                to_do_list.insert(edit, change)

            input(f"The order was successfully changed.\nPress \"Enter\" to continue.")
            clear_terminal()


        clear_terminal()
        application()

def saving():
    if to_do_list:
        save_data = input("Would you like to save your to-do list?\n>")
        if save_data in ["No", "no"]:
            to_do_list.clear()
            save_list()
            input("Your to-do list was cleared.\nPress \"Enter\" to continue.")

        else:
            input("Your to-do list was saved.\nPress \"Enter\" to continue.")



# function for vertical to-do list
def vertical_list():
    if not to_do_list:
        print("Your to-do list is empty.")
    for task in to_do_list:
        print(f"{to_do_list.index(task) + 1}. {task}")

# function for to-do list design
def tasks(function):
    print("TO-DO LIST")
    print(function)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")
    vertical_list()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~")


# file for saving and loading
FILE_NAME = "to_do_list3.pkl"

# function that tries to load to-do list from file
def load_list():
    try:
        with open(FILE_NAME, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

# function to save to-do list to a file
def save_list():
    with open(FILE_NAME, "wb") as f:
        pickle.dump(to_do_list, f)
to_do_list = load_list()

# welcome message and old to-do list if data was loaded
def welcome_back():

    if to_do_list:
        tasks("Welcome back! You left some tasks in your to-do list.")
        input("Press \"Enter\" to continue.")
        clear_terminal()

# function for clearing terminal
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")




welcome_back()
application()

