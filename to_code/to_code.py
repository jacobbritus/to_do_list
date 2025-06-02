# a simple to do list that i'll use specifically when coding
from helper_functions import clear_terminal



# print("┌" + "─" * (BOX_LENGTH + 1) + "┐")
#         print("│ " + message.ljust(82) + "│")
#         print("└" + "─" * (BOX_LENGTH + 1) + "┘")

to_do_list = []

class ToDoList:

    def __init__(self, box_length):
        self.tasks = []
        self.box_length = box_length

    def display_tasks(self):
        self.adapt_box_length()
        sides_space = 5

        print(self.box_length)
        print("┏" + "━" * sides_space + "┳" + "━" * self.box_length + "┳" + "━" * sides_space + "┓")
        print("┃{key}┃{task}┃{status}┃".format(key="Key".center(sides_space), task="Task".center(self.box_length), status="Check".center(sides_space)))

        for index, task in enumerate(self.tasks):
            keybind = "[" + str(index + 1) + "]"
            task_name = task


            print("┣" + "━" * sides_space + "╋" + "━" * self.box_length + "╋" + "━" * sides_space + "┫")
            print("┃{key}┃{task}┃{status}┃".format(key = keybind.center(sides_space), task = task_name.center(self.box_length), status = "[ ]".center(sides_space)))


        print("┗" + "━" * sides_space + "┻" + "━" * self.box_length + "┻" + "━" * sides_space + "┛")

    # scales dynamically if task name doesn't fit anymore
    def adapt_box_length(self):
        for task in self.tasks:
            if len(task) > self.box_length: self.box_length += len(task) - self.box_length






    def add_tasks(self):
        new_task = input("Add a task: ")
        self.tasks.append(new_task)

    def mark_tasks(self):
        ...


code_list = ToDoList(20)

while True:
    code_list.display_tasks()
    code_list.add_tasks()
    clear_terminal()
