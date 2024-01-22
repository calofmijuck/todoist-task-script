import csv
from typing import Any

from todoist_api_python.api import Task, TodoistAPI
from tqdm import tqdm


class CsvTaskAdder:
    """
    CsvTaskAdder adds tasks from CSV file.

    Note: does not set `section_id` back to `None`,
    so tasks without sections must be put first in the csv file.
    """

    api: TodoistAPI
    project_id: str
    task_file: str

    section_id: str | None
    parent_task_ids: list[int]

    def __init__(self, api, project_id, task_file) -> "CsvTaskAdder":
        self.api = api
        self.project_id = project_id
        self.task_file = task_file
        self.parent_task_ids = [None, 0, 0, 0, 0]
        self.section_id = None

    def run(self):
        with open(self.task_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in tqdm(reader):
                match row["TYPE"]:
                    case "section":
                        self.create_section(row)

                    case "task":
                        self.create_task(row)

    def create_section(self, row: dict[str, Any]):
        section = self.api.add_section(project_id=self.project_id, name=row["CONTENT"])
        self.section_id = section.id

    def create_task(self, row: dict[str, Any]) -> Task:
        level = int(row.get("INDENT", 1)) - 1
        task = self.api.add_task(
            content=row["CONTENT"],
            description=row["DESCRIPTION"],
            priority=row["PRIORITY"],
            due_string=row["DATE"],
            project_id=self.project_id,
            section_id=self.section_id,
            parent_id=self.parent_task_ids[level],
        )
        self.parent_task_ids[level + 1] = task.id
