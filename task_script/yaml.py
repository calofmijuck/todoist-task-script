import yaml
from todoist_api_python.api import TodoistAPI

from task_script.schema import TodoistTaskInfo


class YamlTaskAdder:
    """
    YamlTaskAdder adds tasks from yaml files.
    """

    api: TodoistAPI
    task_file: str

    def __init__(self, api: TodoistAPI, task_file: str):
        self.api = api
        self.task_file = task_file

    def run(self):
        with open(self.task_file, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
            task_info = TodoistTaskInfo(data)
            task_info.add(self.api)
