# STDLIB
from typing import Tuple

# THIRD PARTY
import psutil


def get_cpu_temperature() -> str:
    """Get current average temperature between CPU cores."""
    temps = psutil.sensors_temperatures()
    cores = temps.get("coretemp", [])
    core_temps = [core[1] for core in cores]
    if len(core_temps):
        return f"{sum(core_temps) / len(core_temps):.2f}"
    return "0.00"


def get_cpu_utilization() -> str:
    """Get current system-wide CPU utilization as a percentage."""
    return f"{psutil.cpu_percent():.2f}"


def get_memory_utilization() -> Tuple[str, str, str]:
    """Get current system memory usage statistics."""
    memory_utilization = psutil.virtual_memory()
    percentage = memory_utilization.percent
    used = memory_utilization.used / (1024 * 1024)
    total = memory_utilization.total / (1024 * 1024)
    return f"{percentage:.2f}", f"{int(used)}", f"{int(total)}"


def get_storage_utilization() -> Tuple[str, str, str]:
    """Get current storage usage statistics."""
    memory_utilization = psutil.disk_usage(path="/")
    percentage = memory_utilization.percent
    used = memory_utilization.used / (1024 * 1024 * 1024)
    total = memory_utilization.total / (1024 * 1024 * 1024)
    return f"{percentage:.2f}", f"{used:.2f}", f"{total:.2f}"
