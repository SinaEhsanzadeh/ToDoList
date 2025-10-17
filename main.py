from project import Project, ProjectValidationError
from memory import MemoryStore
from task import Task


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
    name = input("Enter project name: ").strip()
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

def project_submenu(project):
    """Menu shown when a specific project is selected."""
    while True:
        print(f"\n=== Project Menu: {project.name} ===")
        print("1. View project details")
        print("2. Add a new task")
        print("3. Return to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            print(project.pretty())
        elif choice == "2":
            add_task_to_project(project)
        elif choice == "3":
            print("\n")
            break
        else:
            print("Invalid option, try again.\n")


def add_task_to_project(project):
    name = input("Enter task name: ").strip()
    desc = input("Enter task description (optional): ").strip()

    try:
        task = Task(name=name, description=desc)
        project.add_task(task)
        print(f"Task '{task.name}' added to project '{project.name}'.\n")
    except Exception as e:
        print(f"Error creating task: {e}\n")


def main():
    store = MemoryStore()

    while True:
        print("=== Project Menu ===")
        print("1. List projects")
        print("2. Create new project")
        print("3. Select a project")
        print("4. Quit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            show_projects(store)

        elif choice == "2":
            create_project_interactively(store)

        elif choice == "3":
            project = select_project_interactively(store)

            if project:
                project_submenu(project)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()
