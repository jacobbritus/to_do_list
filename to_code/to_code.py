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
        self.adapt_box_length()
        sides_space = 5

        print(self.box_length)
        print("┏" + "━" * sides_space + "┳" + "━" * self.box_length + "┳" + "━" * sides_space + "┓")
        print("┃{key}┃{task}┃{status}┃".format(key="Key".center(sides_space), task="Task".center(self.box_length), status="Check".center(sides_space)))

        for index, task in enumerate(self.tasks):
            keybind = "[" + str(index + 1) + "]"
            status = self.tasks[task]["status"]



            print("┣" + "━" * sides_space + "╋" + "━" * self.box_length + "╋" + "━" * sides_space + "┫")
            print("┃{key}┃{name}┃{c}┃".format(key = keybind.center(sides_space), name = task.center(self.box_length), c = status.center(sides_space)))


        print("┗" + "━" * sides_space + "┻" + "━" * self.box_length + "┻" + "━" * sides_space + "┛")

    # scales dynamically if task name doesn't fit anymore
    def adapt_box_length(self):
        for task in self.tasks:
            if len(task) > self.box_length: self.box_length += len(task) - self.box_length






    def add_tasks(self):
        while True:
            print("Please give this new task a name.")
            print("Or press \"Enter\" to go back.")
            user_input = input("> ").strip().lower()

            if user_input == "":
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

code_list = ToDoList(20)

while True:
    code_list.add_tasks()
    code_list.display_tasks()

    clear_terminal()
    # code_list.mark_tasks()

