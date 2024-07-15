# STDLIB
import logging

# THIRD PARTY
from flask_apscheduler import APScheduler

# FIRST PARTY
from rpidash.models.model_manager import ModelManager
from rpidash.services.system_utilization import SystemUtilization
from rpidash.utils.utils import load_app_config


class TaskScheduler:
    """A service for scheduling and executing system utilization tasks."""

    def __init__(self):
        logging.getLogger("apscheduler").setLevel(logging.WARNING)

        self.scheduler = APScheduler()
        self.config = load_app_config()
        self.intervals = self.config["scheduled_tasks"]["intervals"]
        self.delete_config = self.config["scheduled_tasks"]["deletion"]
        self.utilization = SystemUtilization()

        self._setup_tasks()

    def _setup_tasks(self) -> None:
        """Set up the scheduled tasks with their respective intervals."""
        self.scheduler.add_job(
            id="record_cpu_temperature",
            func=self.record_cpu_temperature,
            trigger="interval",
            seconds=self.intervals["cpu_temperature"],
        )
        self.scheduler.add_job(
            id="record_cpu_percentage",
            func=self.record_cpu_percentage,
            trigger="interval",
            seconds=self.intervals["cpu_percentage"],
        )
        self.scheduler.add_job(
            id="record_memory_utilization",
            func=self.record_memory_utilization,
            trigger="interval",
            seconds=self.intervals["memory_percentage"],
        )
        if self.delete_config["enabled"]:
            self.scheduler.add_job(
                id="delete_old_records",
                func=self.delete_old_records,
                trigger="interval",
                seconds=self.intervals["deletion"],
            )

    def start(self) -> None:
        """Start the scheduler to begin executing tasks."""
        self.scheduler.start()

    def record_cpu_temperature(self) -> None:
        """Get CPU temperature and store it in the database."""
        reading = self.utilization.get_cpu_temperature().cpu_temperature
        if reading:
            ModelManager("cpu_temperature").store_record(reading=reading)

    def record_cpu_percentage(self) -> None:
        """Get CPU utilization percentage and store it in the database."""
        reading = self.utilization.get_cpu_percentage().cpu_percentage
        if reading:
            ModelManager("cpu_utilization").store_record(reading=reading)

    def record_memory_utilization(self) -> None:
        """Get memory utilization percentage and store it in the database."""
        reading = self.utilization.get_memory_utilization().memory_percentage
        if reading:
            ModelManager("memory_utilization").store_record(reading=reading)

    def delete_old_records(self) -> None:
        """Delete records older than the configured date."""
        ModelManager().delete_records(
            older_than=self.delete_config["delete_older_than"],
        )
