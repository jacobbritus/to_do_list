# a simple to do list that i'll use specifically when coding
from helper_functions import clear_terminal



# print("┌" + "─" * (BOX_LENGTH + 1) + "┐")
#         print("│ " + message.ljust(82) + "│")
#         print("└" + "─" * (BOX_LENGTH + 1) + "┘")

to_do_list = []

class ToDoList:

    def __init__(self, box_length):
        self.tasks = {}
        self.box_length = box_length

    def display_tasks(self):
        sides_space = 5
        middle_space = self.adapt_box_length(sides_space)



        print("┏" + "━" * sides_space + "┳" + "━" * middle_space + "┳" + "━" * sides_space + "┓")
        print("┃{key}┃{task}┃{status}┃".format(key="Key".center(sides_space), task="Task".center(middle_space), status="Check".center(sides_space)))

        for index, task in enumerate(self.tasks):
            keybind = "[" + str(index + 2) + "]"
            status = self.tasks[task]["status"]



            print("┣" + "━" * sides_space + "╋" + "━" * middle_space + "╋" + "━" * sides_space + "┫")
            print("┃{key}┃{task}┃{status}┃".format(key = keybind.center(sides_space), task = task.center(middle_space), status = status.center(sides_space)))


        print("┗" + "━" * sides_space + "┻" + "━" * middle_space + "┻" + "━" * sides_space + "┛")

    # scales dynamically if task name doesn't fit anymore
    def adapt_box_length(self, sides_space):
        middle_space = self.box_length - (sides_space *2)
        for task in self.tasks:
            if len(task) > middle_space:
                self.box_length += len(task) - middle_space
                middle_space += len(task) - middle_space



        return middle_space






    def add_tasks(self):
        while True:
            print("Please give this new task a name.")
            print("Or press \"Enter\" to go back.")
            user_input = input("> ")

            if user_input.strip() == "":
                break
            else:
                self.tasks.update({user_input: {"status":"[ ]"}})
                input(f"\"{user_input}\" was added.")
                break

    def mark_tasks(self):
        try:
            mark = input("Pick a task")
            self.tasks[mark]["status"] = "[x]"
        except KeyError:
            print("not found.")

class Menu:
    def __init__(self, box_length, page):
        self.box_length = box_length
        self.page = page

    def display_menu(self, box_length):
        box_length += 2 # to do list has some extra characters
        if self.page == "main":
            menu_options = ["[0] New task", "[1] Settings"]

            print("┏" + "━" * box_length + "┓")
            print(f"┃ {menu_options[0].ljust(box_length - len(menu_options[0]) - 3)} {menu_options[1]} ┃")
            print("┗" + "━" * box_length + "┛")


code_list = ToDoList(40)
menu_test = Menu(40, "main")




#
while True:
    code_list.add_tasks()
    code_list.display_tasks()
    menu_test.display_menu(code_list.box_length)
    input()
    clear_terminal()

    # code_list.mark_tasks()

