import os
import logging
from typing import Optional
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_environment_variables(env_file: str) -> None:
    """
    Load environment variables from the specified .env file.

    Args:
        env_file (str): The path to the .env file.
    """
    load_dotenv(dotenv_path=env_file)


def get_env_variable(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Retrieve an environment variable with an optional default value.

    Args:
        key (str): The environment variable key.
        default (Optional[str]): The default value if the key is not found.

    Returns:
        Optional[str]: The value of the environment variable or the default
        value.
    """
    value = os.getenv(key, default)
    if value is None:
        logger.warning(f"{key} is not set. Using default: {default}")
    return value


def get_int_env_variable(key: str, default: int = 0) -> int:
    """
    Retrieve an integer environment variable with a default value.

    Args:
        key (str): The environment variable key.
        default (int): The default value if the key is not found.

    Returns:
        int: The integer value of the environment variable or the default 
        value.
    """
    try:
        return int(get_env_variable(key, str(default)))
    except ValueError:
        logger.error(f"Invalid value for {key}, using default {default}.")
        return default


# Load .env and set environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_environment_variables(env_path)

# Load environment variables
BOT_TOKEN: str = get_env_variable("BOT_TOKEN", "your_bot_token")
