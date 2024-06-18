# STDLIB
import logging

# THIRD PARTY
import psutil


class SystemUtilization:
    """A class to represent the system utilization metrics."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.cpu_temperature = 0.0
        self.cpu_percentage = 0.0

        self.memory_percentage = 0.0
        self.memory_used = 0.0
        self.memory_total = 0.0

        self.storage_percentage = 0.0
        self.storage_used = 0.0
        self.storage_total = 0.0

    def all(self) -> "SystemUtilization":
        """Update all system utilization metrics."""
        self.get_cpu_temperature()
        self.get_cpu_percentage()
        self.get_memory_utilization()
        self.get_storage_utilization()
        return self

    def to_dict(self) -> dict:
        """Convert the system utilization metrics to a dictionary."""
        return {
            "cpu_temperature": self.cpu_temperature,
            "cpu_percentage": self.cpu_percentage,
            "memory_percentage": self.memory_percentage,
            "memory_used": self.memory_used,
            "memory_total": self.memory_total,
            "storage_percentage": self.storage_percentage,
            "storage_used": self.storage_used,
            "storage_total": self.storage_total,
        }

    def get_cpu_temperature(self) -> "SystemUtilization":
        """Get current average temperature between CPU cores."""
        try:
            temps = psutil.sensors_temperatures()
            core_temps = self.extract_core_temps(temps)
            self.cpu_temperature = round(sum(core_temps) / len(core_temps), 2)
        except (AttributeError, ZeroDivisionError) as exc:
            logging.warning(
                "Couldn't get CPU temperate: %s",
                exc,
            )
        return self

    @staticmethod
    def extract_core_temps(temps: dict) -> list:
        """Extract core temperatures from sensor data."""
        keys = ["cpu_thermal", "coretemp"]
        for key in keys:
            if key in temps:
                return [core[1] for core in temps[key]]
        return []

    def get_cpu_percentage(self) -> "SystemUtilization":
        """Get current system-wide CPU utilization as a percentage."""
        self.cpu_percentage = psutil.cpu_percent()
        return self

    def get_memory_utilization(self) -> "SystemUtilization":
        """Get current system memory usage statistics."""
        utilization = psutil.virtual_memory()
        self.memory_percentage = round(utilization.percent, 2)
        self.memory_used = round(utilization.used / (1024 * 1024), 2)
        self.memory_total = round(utilization.total / (1024 * 1024), 2)
        return self

    def get_storage_utilization(self) -> "SystemUtilization":
        """Get current storage usage statistics."""
        utilization = psutil.disk_usage(path="/")
        self.storage_percentage = round(utilization.percent, 2)
        self.storage_used = round(utilization.used / (1024 * 1024 * 1024), 2)
        self.storage_total = round(utilization.total / (1024 * 1024 * 1024), 2)
        return self
