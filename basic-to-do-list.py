tasks = []  # Store all tasks here

def addtask():
    task = input("Please enter a task: ")    # lets u input a new task to the list..
    tasks.append(task)                          # adds the new task to the list 
    print(f"Task '{task}' added to the list.")

def listtask():
    if not tasks:
        print("There are no tasks currently.")  # it will print this if there are no tasks
    else:
        print("Current tasks:")                 # it will prpint this and show the tasks available and their numbers  
        for index, task in enumerate(tasks):
            print(f"Task #{index}: {task}")

def deletetask():            # this function deletes lists
    listtask()
    try:
        tasktodelete = int(input("Enter the task number to delete: "))  # this lets u input the number of the file so it could be deleted
        if 0 <= tasktodelete < len(tasks):
            removed = tasks.pop(tasktodelete)
            print(f"Task '{removed}' has been removed.")
        else:
            print(f"Task #{tasktodelete} was not found.")   # this will be printed if the tasks does not exist or cant be found 
    except ValueError:
        print("Invalid input, please enter a number.")      # this will be printed if the number u inputed does not exist 

if __name__ == "__main__":
    print("Welcome to the To-Do List App :)")
    while True:
        print("\nPlease select one of the following options:")
        print("----------------------------------")
        print("1. Add a new task")
        print("2. Delete a task")
        print("3. List tasks")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            addtask()
        elif choice == "2":
            deletetask()
        elif choice == "3":
            listtask()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid input, please try again.")