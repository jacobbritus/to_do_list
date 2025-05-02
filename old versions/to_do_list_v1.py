#simple to do list

# we gotta make sure it's running unless closed
application = True
to_do_list = []
choice = input("TO-DO LIST\n-------------------------\n1. Add to list\n2. Delete from list\n3. View list\n4. Exit Program\n-------------------------\n>")


while application == True:
    if choice == "1":
        to_do_list.append(input("Add something to your to-do list"))
    elif choice == "2":
        to_do_list.remove(input("Remove something from the list: "))
    elif choice == "3":
        print(to_do_list)
    elif choice == "4":
        print("Exit")
        break
    choice = input("\nTO-DO LIST\n-------------------------\n1. Add to list\n2. Delete from list\n3. View list\n4. Exit Program\n-------------------------\n>")











#I DID IT! THE JOY FELT GREAT! IT ISNT MUCH BUT IM STILL PROUD! I COULDNT DO THIS A WEEK AGO!
