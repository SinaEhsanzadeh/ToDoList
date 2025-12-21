class InMemoryProjectRepo:
    def __init__(self):
        self.projects = {}
        self._id = 1

    def add(self, data):
        data["id"] = self._id
        self.projects[self._id] = data
        self._id += 1
        return data["id"]

    def get(self, project_id):
        return self.projects.get(project_id)

    def delete(self, project_id):
        self.projects.pop(project_id, None)


class InMemoryTaskRepo:
    def __init__(self):
        self.tasks = {}
        self._id = 1

    def add(self, data):
        data["id"] = self._id
        self.tasks[self._id] = data
        self._id += 1
        return data["id"]

    def get(self, task_id):
        return self.tasks.get(task_id)

    def list_by_project(self, project_id):
        return [t for t in self.tasks.values() if t["project_id"] == project_id]

    def update(self, task_id, data):
        self.tasks[task_id].update(data)

    def delete(self, task_id):
        self.tasks.pop(task_id, None)
