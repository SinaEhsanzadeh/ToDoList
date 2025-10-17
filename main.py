from project import Project, ProjectValidationError
from memory import MemoryStore


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


def main():
    store = MemoryStore()

    while True:
        print("=== Project Menu ===")
        print("1. List projects")
        print("2. Create new project")
        print("3. View project details")
        print("4. Quit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            show_projects(store)
        elif choice == "2":
            create_project_interactively(store)
        elif choice == "3":
            view_project_details(store)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.\n")


if __name__ == "__main__":
    main()
