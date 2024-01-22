"""
Todoist API 를 이용해서 대량의 Task 를 자동으로 추가합니다.

기본 사용 방법
=========================

python -m task_script --tasks TASKS
"""

import argparse

from todoist_api_python.api import TodoistAPI

from task_script.csv import CsvTaskAdder

from .constants import TODOIST_API_KEY

# fmt: off
parser = argparse.ArgumentParser()
parser.add_argument("--tasks", type=str, required=True, help="Location of task file")
parser.add_argument("--csv", action='store_true', help="Whether the file is in csv format")
parser.add_argument("--project", type=str, required=True, help="Whether the file is in csv format")
# fmt: on


def main(args: argparse.Namespace):
    if TODOIST_API_KEY is None:
        raise RuntimeError("TODOIST_API_KEY is not found. Did you specify `.env` file properly?")

    api = TodoistAPI(TODOIST_API_KEY)

    if args.csv:
        csv_task_adder = CsvTaskAdder(api, args.project, args.tasks)
        csv_task_adder.run()
    else:
        # TODO: handle_yaml(api)
        pass

    # with open(args.tasks, "r", encoding="utf-8") as f:
    #     tasks = yaml.load(f, Loader=yaml.BaseLoader)

    print("Done! Let's go finish some tasks! ✨ 🍰 ✨")


main(parser.parse_args())
