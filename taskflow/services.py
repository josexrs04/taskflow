from .models import PRIORITIES, Task


class TaskService:
    def __init__(self, storage):
        self.storage = storage

    def add(self, title, priority="medium", due=None):
        if priority not in PRIORITIES:
            raise ValueError(f"Prioridad inválida: {priority}")
        tasks = self.storage.load()
        new_id = len(tasks) + 1
        task = Task(id=new_id, title=title, priority=priority, due=due)
        tasks.append(task)
        self.storage.save(tasks)
        return task

    def list(self, include_done=True, sort_by_priority=False):
        tasks = self.storage.load()
        if not include_done:
            tasks = [t for t in tasks if not t.done]
        if sort_by_priority:
            tasks.sort(key=lambda t: t.priority)
        return tasks

    def complete(self, task_id):
        tasks = self.storage.load()
        for task in tasks:
            if task.id == task_id:
                task.done = True
        self.storage.save(tasks)

    def delete(self, task_id):
        tasks = [t for t in self.storage.load() if t.id != task_id]
        self.storage.save(tasks)
