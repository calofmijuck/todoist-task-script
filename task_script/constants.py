import os

from dotenv import load_dotenv

load_dotenv()


TASKS_API_URL = "https://api.todoist.com/rest/v1/tasks"

TODOIST_API_KEY = os.environ.get("TODOIST_API_KEY", None)
