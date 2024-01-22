import os

from dotenv import load_dotenv

load_dotenv()


TODOIST_API_KEY = os.environ.get("TODOIST_API_KEY", None)
