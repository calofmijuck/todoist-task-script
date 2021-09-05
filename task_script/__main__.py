"""
Todoist API 를 이용해서 대량의 Task 를 자동으로 추가합니다.

기본 사용 방법
=========================

python -m task_script --tasks TASKS
"""

import argparse

import yaml

from .constants import TODOIST_API_KEY

# fmt: off
parser = argparse.ArgumentParser()
parser.add_argument("--tasks", type=str, required=True, help="Task 목록 파일 위치")
# fmt: on


def main(args: argparse.Namespace):

    if TODOIST_API_KEY is None:
        raise RuntimeError("TODOIST_API_KEY is not found. Did you specify `.env` file properly?")

    with open(args.tasks, "r", encoding="utf-8") as f:
        tasks = yaml.load(f, Loader=yaml.BaseLoader)

    print("Done! Let's go finish some tasks! ✨ 🍰 ✨")


main(parser.parse_args())
