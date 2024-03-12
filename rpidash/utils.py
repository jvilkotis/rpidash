# STDLIB
import logging
import os
from typing import Optional, Tuple, Union

# THIRD PARTY
import psutil
import toml
import yaml


def get_cpu_temperature() -> Union[str, None]:
    """Get current average temperature between CPU cores."""
    temps = psutil.sensors_temperatures()
    cores = temps.get("coretemp", [])
    core_temps = [core[1] for core in cores]
    try:
        return f"{sum(core_temps) / len(core_temps):.2f}"
    except ZeroDivisionError as exc:
        logging.warning("Couldn't calculate average CPU temperate: %s", exc)
        return None


def get_cpu_percentage() -> Union[str, None]:
    """Get current system-wide CPU utilization as a percentage."""
    utilization = psutil.cpu_percent()
    if utilization > 0:
        return f"{utilization:.2f}"
    return None


def get_memory_utilization() -> Tuple[str, str, str]:
    """Get current system memory usage statistics."""
    utilization = psutil.virtual_memory()
    percentage = f"{utilization.percent:.2f}"
    used = f"{int(utilization.used / (1024 * 1024))}"
    total = f"{int(utilization.total / (1024 * 1024))}"
    return percentage, used, total


def get_storage_utilization() -> Tuple[str, str, str]:
    """Get current storage usage statistics."""
    utilization = psutil.disk_usage(path="/")
    percentage = f"{utilization.percent:.2f}"
    used = f"{int(utilization.used / (1024 * 1024 * 1024))}"
    total = f"{int(utilization.total / (1024 * 1024 * 1024))}"
    return percentage, used, total


def load_app_config(testing: Optional[bool] = False) -> dict:
    """Load app configuration from YAML file."""
    file_name = "test_config.yaml" if testing else "config.yaml"
    dir_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(dir_path, file_name)
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
