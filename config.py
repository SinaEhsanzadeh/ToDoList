import os
from dotenv import load_dotenv

load_dotenv()

def get_int(key: str, default: int) -> int:
    val = os.getenv(key)

    if val is None:
        return default

    try:
        return int(val)

    except ValueError:
        return default

def get_str(key: str, default: str) -> str:
    return os.getenv(key, default)

PROJECT_MAX_COUNT = get_int("PROJECT_MAX_COUNT", 10)
PROJECT_MAX_NAME_LEN = get_int("PROJECT_MAX_NAME_LEN", 30)
PROJECT_MAX_DESCRIPTION_LEN = get_int("PROJECT_MAX_DESCRIPTION_LEN", 150)

TASK_MAX_COUNT = get_int("TASK_MAX_COUNT", 20)
TASK_MAX_NAME_LEN = get_int("TASK_MAX_NAME_LEN", 30)
TASK_MAX_DESCRIPTION_LEN = get_int("TASK_MAX_DESCRIPTION_LEN", 150)

