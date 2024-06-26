# STDLIB
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# THIRD PARTY
from sqlalchemy import Column, DateTime

# FIRST PARTY
from rpidash.scheduled_tasks import (
    delete_old_records,
    record_cpu_percentage,
    record_cpu_temperature,
    record_memory_utilization,
)


class TestScheduledTasks(unittest.TestCase):
    """A test suite for the scheduled tasks."""

    @patch("rpidash.scheduled_tasks.logging")
    @patch("rpidash.system_utilization.SystemUtilization.get_cpu_temperature")
    @patch("rpidash.scheduled_tasks.db_session")
    def test_record_cpu_temperature_success(
        self,
        mock_db_session,
        mock_get_cpu_temperature,
        mock_logging,
    ):
        """
        Test record_cpu_temperature when get_cpu_temperature returns
        a valid reading.
        """
        mock_get_cpu_temperature.return_value.cpu_temperature = 49.0
        record_cpu_temperature()
        mock_get_cpu_temperature.assert_called_once()
        mock_logging.info.assert_called_once_with(
            "Storing CPU temperature: %s °C",
            49.0,
        )
        mock_db_session.commit.assert_called_once()
        self.assertEqual(
            mock_db_session.add.call_args[0][0].temperature,
            49.0,
        )

    @patch("rpidash.scheduled_tasks.logging")
    @patch("rpidash.system_utilization.SystemUtilization.get_cpu_temperature")
    @patch("rpidash.scheduled_tasks.db_session")
    def test_record_cpu_temperature_no_reading(
        self,
        mock_db_session,
        mock_get_cpu_temperature,
        mock_logging,
    ):
        """
        Test record_cpu_temperature when get_cpu_temperature returns None.
        """
        mock_get_cpu_temperature.return_value.cpu_temperature = None
        record_cpu_temperature()
        mock_get_cpu_temperature.assert_called_once()
        mock_logging.info.assert_not_called()
        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()

    @patch("rpidash.scheduled_tasks.logging")
    @patch("rpidash.system_utilization.SystemUtilization.get_cpu_percentage")
    @patch("rpidash.scheduled_tasks.db_session")
    def test_record_cpu_percentage_success(
        self,
        mock_db_session,
        mock_get_cpu_percentage,
        mock_logging,
    ):
        """
        Test record_cpu_percentage when get_cpu_percentage returns
        a valid reading.
        """
        mock_get_cpu_percentage.return_value.cpu_percentage = 50.0
        record_cpu_percentage()
        mock_get_cpu_percentage.assert_called_once()
        mock_logging.info.assert_called_once_with(
            "Storing CPU utilization: %s%%",
            50.0,
        )
        mock_db_session.commit.assert_called_once()
        self.assertEqual(
            mock_db_session.add.call_args[0][0].percentage,
            50.0,
        )

    @patch("rpidash.scheduled_tasks.logging")
    @patch("rpidash.system_utilization.SystemUtilization.get_cpu_percentage")
    @patch("rpidash.scheduled_tasks.db_session")
    def test_record_cpu_percentage_no_reading(
        self,
        mock_db_session,
        mock_get_cpu_percentage,
        mock_logging,
    ):
        """Test record_cpu_percentage when get_cpu_percentage returns None."""
        mock_get_cpu_percentage.return_value.cpu_percentage = None
        record_cpu_percentage()
        mock_get_cpu_percentage.assert_called_once()
        mock_logging.info.assert_not_called()
        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()

    @patch("rpidash.scheduled_tasks.logging")
    @patch(
        "rpidash.system_utilization.SystemUtilization.get_memory_utilization"
    )
    @patch("rpidash.scheduled_tasks.db_session")
    def test_record_memory_utilization(
        self,
        mock_db_session,
        mock_get_memory_utilization,
        mock_logging,
    ):
        """Test record_memory_utilization function."""
        mock_get_memory_utilization.return_value.memory_percentage = 51.0
        record_memory_utilization()
        mock_get_memory_utilization.assert_called_once()
        mock_logging.info.assert_called_once_with(
            "Storing memory utilization: %s%%",
            51.0,
        )
        mock_db_session.commit.assert_called_once()
        self.assertEqual(
            mock_db_session.add.call_args[0][0].percentage,
            51.0,
        )

    @patch("rpidash.scheduled_tasks.inspect", new_callable=MagicMock)
    @patch("rpidash.scheduled_tasks.models")
    @patch("rpidash.scheduled_tasks.db_session")
    @patch("rpidash.scheduled_tasks.config")
    def test_delete_old_records(
        self,
        mock_config,
        mock_db_session,
        mock_models,
        mock_inspect,
    ):
        """Test delete_old_records function."""
        config = {
            "scheduled_tasks": {
                "intervals": {
                    "deletion": 60,
                },
                "deletion": {
                    "enabled": True,
                    "delete_older_than": 3600,
                },
            }
        }
        mock_config.__getitem__.side_effect = config.__getitem__
        mock_model1 = MagicMock()
        mock_model1.date = Column(DateTime())
        mock_model1.__tablename__ = "mock_table1"
        mock_model2 = MagicMock()
        mock_model2.date = Column(DateTime())
        mock_model2.__tablename__ = "mock_table2"
        mock_models.__name__ = mock_model1.__module__
        mock_inspect.isclass.return_value = True
        mock_inspect.getmembers.return_value = [
            (None, mock_model1),
            (None, mock_model2),
        ]
        delete_old_records()
        cutoff_date = datetime.now() - timedelta(seconds=3600)
        self.assertAlmostEqual(
            mock_model1.query.filter.call_args[0][0].right.value,
            cutoff_date,
            delta=timedelta(seconds=1),
        )
        self.assertAlmostEqual(
            mock_model2.query.filter.call_args[0][0].right.value,
            cutoff_date,
            delta=timedelta(seconds=1),
        )
        mock_model1.query.filter().delete.assert_called_once()
        mock_model2.query.filter().delete.assert_called_once()
        mock_db_session.commit.assert_called()

    @patch("rpidash.scheduled_tasks.db_session")
    @patch("rpidash.scheduled_tasks.config")
    def test_delete_old_records_not_run(
        self,
        mock_config,
        mock_db_session,
    ):
        """Test delete_old_records function is not run."""
        config = {
            "scheduled_tasks": {
                "deletion": {
                    "enabled": False,
                },
            }
        }
        mock_config.__getitem__.side_effect = config.__getitem__
        delete_old_records()
        mock_db_session.commit.assert_not_called()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
