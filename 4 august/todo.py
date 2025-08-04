# todo.py

def load_tasks(filename="tasks.txt"):
    """Load tasks from the file into a list"""
    try:
        with open(filename, "r") as f:
            tasks = [line.strip() for line in f]
        return tasks
    except FileNotFoundError:
        return []


def save_tasks(tasks, filename="tasks.txt"):
    """Save the tasks list to a file"""
    with open(filename, "w") as f:
        for task in tasks:
            f.write(task + "\n")


def show_tasks(tasks):
    print("\n📋 Your To-Do List:")
    if not tasks:
        print(" - No tasks yet!")
    else:
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")
    print()


def add_task(tasks):
    task = input("Enter new task: ").strip()
    if task:
        tasks.append(task)
        print("✅ Task added!")


def remove_task(tasks):
    show_tasks(tasks)
    try:
        task_no = int(input("Enter task number to remove: "))
        if 1 <= task_no <= len(tasks):
            removed = tasks.pop(task_no - 1)
            print(f"❌ Removed: {removed}")
        else:
            print("❗ Invalid task number")
    except ValueError:
        print("❗ Please enter a number")


def main():
    tasks = load_tasks()
    while True:
        print("📝 To-Do List Menu:")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Remove Task")
        print("4. Save and Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            save_tasks(tasks)
            print("💾 Tasks saved. Goodbye!")
            break
        else:
            print("❗ Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
