from project import Project, ProjectValidationError
from memory import MemoryStore
from task import Task, TaskState, InvalidDeadlineError, TaskValidationError
from config import PROJECT_MAX_COUNT, TASK_MAX_COUNT
from utils import is_project_name_taken, is_task_name_taken

def show_projects(store: MemoryStore):
    print("\n--- Projects in Memory ---")
    projects = store.list_projects()

    if not projects:
        print("No projects available.")
    else:
        for idx, project in enumerate(projects, start=1):
            print(f"{idx}. {project.name} (ID: {project.id})")

    print("--------------------------\n")

def create_project_interactively(store: MemoryStore):
    projects = store.list_projects()
    if len(projects) >= PROJECT_MAX_COUNT:
        print(f"Cannot create more projects. Maximum limit of {PROJECT_MAX_COUNT} reached.\n")
        return

    name = input("Enter project name: ").strip()
    if is_project_name_taken(store, name):
        print(f"A project with the name '{name}' already exists.\n")
        return

    desc = input("Enter project description (optional): ").strip()

    try:
        project = Project(name, desc)
        store.add_project(project)
        print(f"Project '{project.name}' created successfully.\n")

    except ProjectValidationError as e:
        print(f"Error creating project: {e}\n")

def select_project_interactively(store: MemoryStore):
    show_projects(store)
    projects = store.list_projects()
    if not projects:
        return None

    pid = input("Enter the project ID to select: ").strip()
    project = store.get_project(pid)

    if not project:
        print("No project found with that ID.\n")
    return project

def view_project_details(store: MemoryStore):
    show_projects(store)

    if not store.list_projects():
        return

    pid = input("Enter the project ID to view: ").strip()
    project = store.get_project(pid)
    if project:
        print(project.pretty())
    else:
        print("No project found with that ID.\n")

def project_submenu(project, store: MemoryStore):
    while True:
        print(f"\n=== Project Menu: {project.name} ===")
        print("1. View project details")
        print("2. Add a new task")
        print("3. Edit project")
        print("4. Manage tasks")
        print("5. Return to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print(project.pretty())
        elif choice == "2":
            add_task_to_project(project)
        elif choice == "3":
            edit_project(project, store)
        elif choice == "4":
            manage_tasks_menu(project)
        elif choice == "5":
            print("\n")
            break
        else:
            print("Invalid option, try again.\n")

def edit_project(project, store: MemoryStore):
    print(f"\n--- Editing Project: {project.name} ---")
    print("Leave fields empty to keep current values.")

    new_name = input(f"New name: ").strip()
    if new_name and is_project_name_taken(store, new_name, exclude_id=project.id):
        print(f"A project with the name '{new_name}' already exists.\n")
        return

    new_desc = input(f"New description: ").strip()

    try:
        if new_name:
            project.update_name(new_name)

        if new_desc:
            project.update_description(new_desc)
        elif new_desc == "":
            project.update_description(None)

        print("Project updated successfully.\n")

    except ProjectValidationError as e:
        print(f"Error updating project: {e}\n")

def delete_project_interactively(store: MemoryStore):
    show_projects(store)
    projects = store.list_projects()
    if not projects:
        return

    pid = input("Enter the project ID to delete: ").strip()
    project = store.get_project(pid)
    if not project:
        print("No project found with that ID.\n")
        return

    confirm = input(f"Are you sure you want to delete project '{project.name}' and all its tasks? (Y/N): ").strip().lower()
    if confirm == "y":
        store.remove_project(pid)
        print(f"Project '{project.name}' and all its tasks have been deleted.\n")
    else:
        print("Deletion cancelled.\n")

def manage_tasks_menu(project):
    if not project.tasks:
        print("This project has no tasks.\n")
        return

    while True:
        if not project.tasks:
            print("This project has no tasks.\n")
            return

        print("\n--- Tasks ---")

        for idx, task in enumerate(project.tasks, start=1):
            deadline_str = task.deadline if task.deadline else "(no deadline)"
            print(f"{idx}. {task.name} | status: {task.state.value} | deadline: {deadline_str} | id: {task.id}")
            print(f"   Description: {task.description or '(none)'}")

        print(f"{len(project.tasks) + 1}. Return to project menu")

        choice = input("Select a task number to manage or go back: ").strip()

        if not choice.isdigit():
            print("Invalid option.\n")
            continue

        idx = int(choice)

        if idx == len(project.tasks) + 1:
            break

        if not (1 <= idx <= len(project.tasks)):
            print("Invalid task number.\n")
            continue

        task = project.tasks[idx - 1]

        while True:
            if task not in project.tasks:
                break

            print(f"\n--- Task Menu: {task.name} ---")
            print("1. Edit task")
            print("2. Delete task")
            print("3. View task details")
            print("4. Return to tasks list")

            action = input("> ").strip()

            if action == "1":
                edit_task(task, project)
            elif action == "2":
                confirm = input(f"Are you sure you want to delete task '{task.name}'? (Y/N): ").strip().lower()
                if confirm == "y":
                    project.remove_task(task.id)
                    print(f"Task '{task.name}' deleted.\n")

                    if not project.tasks:
                        print("No tasks left in this project. Returning to project menu.\n")
                        return

                    break
            elif action == "3":
                print(task.pretty())
            elif action == "4":
                break
            else:
                print("Invalid option.\n")

def edit_task(task: Task, project: Project):
    print(f"\n--- Editing Task: {task.name} ---")
    print("Leave a field empty to keep the current value.")

    name = input(f"New name: ").strip()
    if is_task_name_taken(project, name):
        print(f"A task with the name '{name}' already exists in this project.\n")
        return
    new_desc = input(f"New description: ").strip()

    print(f"Current status: {task.state.value}")
    print("Change status? (1: TODO, 2: DOING, 3: DONE, Enter to keep)")
    state_choice = input("> ").strip()

    print(f"Current deadline: {task.deadline or '(none)'}")
    new_deadline = input("New deadline (YYYY-MM-DD) or leave empty to keep/remove: ").strip()

    if name:
        task.name = name
    if new_desc:
        task.description = new_desc
    elif new_desc == "":
        task.description = None

    if state_choice == "1":
        task.state = TaskState.TODO
    elif state_choice == "2":
        task.state = TaskState.DOING
    elif state_choice == "3":
        task.state = TaskState.DONE

    try:
        if new_deadline:
            task.update_deadline(new_deadline)
        elif new_deadline == "":
            task.update_deadline(None)
    except InvalidDeadlineError as e:
        print(f"Error updating deadline: {e}\n")
        return

    print("Task updated successfully.\n")

def add_task_to_project(project):
    if len(project.tasks) >= TASK_MAX_COUNT:
        print(f"Cannot add more tasks. Maximum of {TASK_MAX_COUNT} tasks per project reached.\n")
        return

    name = input("Enter task name: ").strip()
    if is_task_name_taken(project, name):
        print(f"A task with the name '{name}' already exists in this project.\n")
        return
    desc = input("Enter task description (optional): ").strip()
    deadline = input("Enter task deadline (YYYY-MM-DD) or leave blank: ").strip()

    try:
        task = Task(name=name, description=desc, deadline=deadline if deadline else None)
        project.add_task(task)
        print(f"Task '{task.name}' added to project '{project.name}'.\n")
    except (TaskValidationError, InvalidDeadlineError) as e:
        print(f"Error creating task: {e}\n")


def main():
    store = MemoryStore()

    while True:
        print("=== Project Menu ===")
        print("1. List projects")
        print("2. Create new project")
        print("3. Select a project")
        print("4. Delete a project")
        print("5. Quit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            show_projects(store)
        elif choice == "2":
            create_project_interactively(store)
        elif choice == "3":
            project = select_project_interactively(store)
            if project:
                project_submenu(project, store)
        elif choice == "4":
            delete_project_interactively(store)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()
