def is_project_name_taken(store, name: str, exclude_id: str = None) -> bool:
    return any(
        p.name == name and (exclude_id is None or p.id != exclude_id)
        for p in store.list_projects()
    )

def is_task_name_taken(project, name: str, exclude_id: str = None) -> bool:
    return any(
        t.name == name and (exclude_id is None or t.id != exclude_id)
        for t in project.tasks
    )