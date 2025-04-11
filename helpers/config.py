import os
from dotenv import load_dotenv

load_dotenv() 

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

def get_env_variable(var_name: str) -> str:
    """Gets an environment variable or raises an error if not found."""
    value = os.getenv(var_name)
    if value is None:
        raise ConfigError(f"Environment variable '{var_name}' not set.")
    return value

# Load specific configurations
EHR_URL = get_env_variable("EHR_URL")
EHR_USERNAME = get_env_variable("EHR_USERNAME")
EHR_PASSWORD = get_env_variable("EHR_PASSWORD")

