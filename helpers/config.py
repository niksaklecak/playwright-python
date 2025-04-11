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
WEINFUSE_BASE_URL = get_env_variable("WEINFUSE_BASE_URL")
WEINFUSE_USERNAME = get_env_variable("WEINFUSE_USERNAME")
WEINFUSE_PASSWORD = get_env_variable("WEINFUSE_PASSWORD")
WEINFUSE_OTP_SECRET = get_env_variable("WEINFUSE_OTP_SECRET")

