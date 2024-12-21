import os
from dotenv import load_dotenv
from typing import Any

load_dotenv()


def get_env_var(key) -> Any:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Key dosen't exist: {key}")
    return value


class Config:
    GEMINI_API_KEY: str = get_env_var("GEMINI_API_KEY")
    MODEL: str = get_env_var("MODEL")
