# STDLIB
import unittest
from unittest.mock import patch

# FIRST PARTY
from rpidash.services.task_scheduler import TaskScheduler


class TestTaskScheduler(unittest.TestCase):
    """A test suite for the task scheduler."""

    @patch("rpidash.services.task_scheduler.load_app_config")
    @patch("rpidash.services.task_scheduler.APScheduler")
    def setUp(self, mock_scheduler, mock_load_config):  # pylint: disable=arguments-differ
        """Set up common attributes for tests."""
        self.mock_config = {
            "scheduled_tasks": {
                "intervals": {
                    "cpu_temperature": 10,
                    "cpu_percentage": 20,
                    "memory_percentage": 30,
                    "deletion": 40,
                },
                "deletion": {
                    "enabled": True,
                    "delete_older_than": 7,
                }
            }
        }
        mock_load_config.return_value = self.mock_config
        self.mock_scheduler = mock_scheduler.return_value
        self.task_scheduler = TaskScheduler()

    @patch(
        "rpidash.services.system_utilization"
        ".SystemUtilization.get_cpu_temperature"
    )
    @patch("rpidash.services.task_scheduler.ModelManager.store_record")
    def test_record_cpu_temperature(
        self,
        mock_store_record,
        mock_get_cpu_temperature,
    ):
        """Test record_cpu_temperature method."""
        mock_get_cpu_temperature.return_value.cpu_temperature = 49.0
        self.task_scheduler.record_cpu_temperature()
        mock_store_record.assert_called_with(reading=49.0)

    @patch(
        "rpidash.services.system_utilization"
        ".SystemUtilization.get_cpu_percentage"
    )
    @patch("rpidash.services.task_scheduler.ModelManager.store_record")
    def test_record_cpu_percentage(
        self,
        mock_store_record,
        mock_get_cpu_percentage,
    ):
        """Test record_cpu_percentage method."""
        mock_get_cpu_percentage.return_value.cpu_percentage = 50.0
        self.task_scheduler.record_cpu_percentage()
        mock_store_record.assert_called_with(reading=50.0)

    @patch(
        "rpidash.services.system_utilization"
        ".SystemUtilization.get_memory_utilization"
    )
    @patch("rpidash.services.task_scheduler.ModelManager.store_record")
    def test_record_memory_utilization(
        self,
        mock_store_record,
        mock_get_memory_utilization,
    ):
        """Test record_memory_utilization method."""
        mock_get_memory_utilization.return_value.memory_percentage = 51.0
        self.task_scheduler.record_memory_utilization()
        mock_store_record.assert_called_with(reading=51.0)

    @patch("rpidash.services.task_scheduler.ModelManager.delete_records")
    def test_delete_old_records(self, mock_delete_records):
        """Test delete_old_records method."""
        self.task_scheduler.delete_old_records()
        mock_delete_records.assert_called_with(
            older_than=self.mock_config["scheduled_tasks"]["deletion"][
                "delete_older_than"
            ]
        )

    def test_start(self):
        """Test method that starts the task scheduler."""
        self.task_scheduler.start()
        self.mock_scheduler.start.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
