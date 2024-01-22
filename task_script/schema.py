from todoist_api_python.api import TodoistAPI
from typing import Any


class TodoistProject:
    name: str | None
    id: str | None

    def __init__(self, data: dict[str, Any]):
        name, id = data.get("name", ""), data.get("id", "")

        if not ((name == "") ^ (id == "")):
            raise ValueError("only specify either one of project name or id")

        self.name = name
        self.id = id

    def add_project(self, api: TodoistAPI):
        """
        Only works if project id is None and name is not None
        """

        assert self.id == None
        assert self.name != None

        project = api.add_project(name=self.name)
        self.id = project.id


class TodoistTask:
    content: str
    description: str | None
    labels: list[str] | None
    priority: int | None
    due: str | None  # human defined task due date ex. next Monday, Tomorrow etc.
    date: str | None  # yyyy-mm-dd format
    subtasks: list["TodoistTask"]

    def __init__(self, data: dict[str, Any]):
        self.content = data["content"]  # required
        self.description = data.get("description")
        self.labels = data.get("labels")
        self.priority = data.get("priority")
        self.due = data.get("due")
        self.date = data.get("date")
        self.subtasks = [TodoistTask(subtask_data) for subtask_data in data.get("subtasks", [])]

    def add_task(
        self,
        api: TodoistAPI,
        project_id: str | None,
        section_id: str | None,
        parent_id: str | None,
    ):
        task = api.add_task(
            content=self.content,
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            labels=self.labels,
            priority=self.priority,
            due_string=self.due,
            due_date=self.date,
        )

        for subtask in self.subtasks:
            subtask.add_task(api, project_id, section_id, task.id)


class TodoistSection:
    name: str
    tasks: list[TodoistTask]

    def __init__(self, data: dict[str, Any]):
        self.name = data["name"]  # required
        self.tasks = [TodoistTask(task_data) for task_data in data.get("tasks", [])]

    def add_section(self, api: TodoistAPI, project_id: str):
        assert project_id != None

        section = api.add_section(project_id=project_id, name=self.name)
        self.add_tasks(api, project_id, section.id)

    def add_tasks(self, api: TodoistAPI, project_id: str, section_id: str):
        assert project_id != None

        for task in self.tasks:
            task.add_task(api, project_id, section_id, None)


class TodoistTaskInfo:
    project: TodoistProject
    sections: list[TodoistSection]
    tasks: list[TodoistTask]  # tasks without sections

    def __init__(self, data: dict[str, Any]):
        self.project = TodoistProject(data["project"])

        self.sections = [TodoistSection(section_data) for section_data in data.get("sections", [])]
        self.tasks = [TodoistTask(task_data) for task_data in data.get("tasks", [])]

    def add(self, api: TodoistAPI):
        """
        Add everything contained in the `TodoistTaskInfo` object.
        """

        if self.project.id == None:
            self.project.add_project(api)

        assert self.project.id != None

        for section in self.sections:
            section.add_section(api, self.project.id)

        for task in self.tasks:
            task.add_task(api, self.project.id, None, None)
