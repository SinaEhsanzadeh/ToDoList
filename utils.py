def is_project_name_taken(store, name: str, exclude_id: str = None) -> bool:
    return any(
        p.name == name and (exclude_id is None or p.id != exclude_id)
        for p in store.list_projects()
    )
