# STDLIB
import os

# THIRD PARTY
import toml
import yaml


def load_app_config() -> dict:
    """Load app configuration from YAML file."""
    environment = os.environ["FLASK_ENV"]
    dir_path = os.path.dirname(os.path.abspath(__file__))
    if environment == "production":
        config_path = "/data/config.yaml"
    elif environment == "development":
        config_path = os.path.join(dir_path, "config.dev.yaml")
    elif environment == "testing":
        config_path = os.path.join(dir_path, "config.test.yaml")
    else:
        raise ValueError(f"Invalid environment provided: {environment}")
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def get_project_version() -> str:
    """Get project version from pyproject.toml."""
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pyproject_path = os.path.join(dir_path, "pyproject.toml")
    with open(pyproject_path, "r", encoding="utf-8") as file:
        pyproject = toml.load(file)
    version = pyproject["project"]["version"]
    return version
