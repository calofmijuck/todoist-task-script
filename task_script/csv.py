import csv
from typing import Any

from todoist_api_python.api import TodoistAPI


class CsvTaskAdder:
    """
    CsvTaskAdder adds tasks from CSV files.

    Note: does not set `section_id` back to `None`,
    so tasks without sections must be put first in the csv file.
    """

    api: TodoistAPI
    project_id: str
    task_file: str

    section_id: str | None
    parent_task_ids: list[str | None]

    def __init__(self, api: TodoistAPI, project_id: str, task_file: str):
        self.api = api
        self.project_id = project_id
        self.task_file = task_file
        self.parent_task_ids = [None] * 5
        self.section_id = None

    def run(self):
        with open(self.task_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                match row["TYPE"]:
                    case "section":
                        self.add_section(row)

                    case "task":
                        self.add_task(row)

    def add_section(self, row: dict[str, Any]):
        section = self.api.add_section(project_id=self.project_id, name=row["CONTENT"])
        self.section_id = section.id

    def add_task(self, row: dict[str, Any]):
        level = int(row.get("INDENT", 1)) - 1
        try:
            task = self.api.add_task(
                content=row["CONTENT"],
                description=row["DESCRIPTION"],
                priority=row.get("PRIORITY", 1),
                due_string=row["DATE"],
                project_id=self.project_id,
                section_id=self.section_id,
                # parent_id=self.parent_task_ids[level],
            )
        except Exception as e:
            print(e)
        self.parent_task_ids[level + 1] = task.id
