# STDLIB
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# FIRST PARTY
from rpidash.models.model_manager import ModelManager


class TestModelManager(unittest.TestCase):
    """A test suite for the model manager."""

    def setUp(self):
        """Set up common attributes for tests."""
        self.mock_cpu_temperature = MagicMock()
        self.mock_cpu_utilization = MagicMock()
        self.mock_memory_utilization = MagicMock()

        self.mock_cpu_temperature.__tablename__ = "cpu_temperature"
        self.mock_cpu_utilization.__tablename__ = "cpu_utilization"
        self.mock_memory_utilization.__tablename__ = "memory_utilization"

        self.mock_cpu_temperature.get_value_key.return_value = "temperature"
        self.mock_cpu_utilization.get_value_key.return_value = "percentage"
        self.mock_memory_utilization.get_value_key.return_value = "percentage"

        self.mock_cpu_temperature.date = datetime(2024, 1, 2, 12, 0, 0)
        self.mock_cpu_utilization.date = datetime(2024, 1, 2, 12, 0, 0)
        self.mock_memory_utilization.date = datetime(2024, 1, 2, 12, 0, 0)

        self.models = {
            "cpu_temperature": self.mock_cpu_temperature,
            "cpu_utilization": self.mock_cpu_utilization,
            "memory_utilization": self.mock_memory_utilization,
        }

    @patch("rpidash.models.model_manager.ModelManager.get_models")
    def test_get_model_success(self, mock_get_models):
        """Test get_model method with a valid table name."""
        mock_get_models.return_value = self.models

        manager = ModelManager()
        model = manager.get_model("cpu_temperature")
        self.assertEqual(model, self.mock_cpu_temperature)

    @patch("rpidash.models.model_manager.ModelManager.get_models")
    def test_get_model_invalid(self, mock_get_models):
        """Test get_model method with an invalid table name."""
        mock_get_models.return_value = self.models

        manager = ModelManager()
        with self.assertRaises(ValueError):
            manager.get_model("non_existent_table")

    @patch("rpidash.models.model_manager.ModelManager.get_models")
    def test_retrieve_data_no_filter(self, mock_get_models):
        """Test retrieve_data method without recorded_after filter."""
        mock_get_models.return_value = self.models
        manager = ModelManager("cpu_temperature")

        mock_data = [
            MagicMock(date=datetime(2024, 1, 1, 12, 0, 0), temperature=50),
            MagicMock(date=datetime(2024, 1, 2, 12, 0, 0), temperature=55),
        ]
        manager.model.query.all.return_value = mock_data

        data = manager.retrieve_data()
        expected_data = {
            "values": [50, 55],
            "dates": ["2024-01-01T12:00:00", "2024-01-02T12:00:00"],
        }
        self.assertEqual(data, expected_data)

    @patch("rpidash.models.model_manager.ModelManager.get_models")
    def test_retrieve_data_with_filter(self, mock_get_models):
        """Test retrieve_data method with recorded_after filter."""
        mock_get_models.return_value = self.models
        manager = ModelManager("cpu_temperature")

        mock_data = [
            MagicMock(date=datetime(2024, 1, 1, 12, 0, 0), temperature=50),
            MagicMock(date=datetime(2024, 1, 2, 12, 0, 0), temperature=55),
        ]
        manager.model.query.filter.return_value.all.return_value = mock_data

        recorded_after = "2024-01-01T00:00:00"
        data = manager.retrieve_data(recorded_after=recorded_after)
        expected_data = {
            "values": [50, 55],
            "dates": ["2024-01-01T12:00:00", "2024-01-02T12:00:00"],
        }
        self.assertEqual(data, expected_data)

    @patch("rpidash.models.model_manager.ModelManager.get_models")
    def test_retrieve_data_invalid_date(self, mock_get_models):
        """Test retrieve_data method with invalid recorded_after date."""
        mock_get_models.return_value = self.models
        manager = ModelManager("cpu_temperature")

        with self.assertRaises(ValueError):
            manager.retrieve_data(recorded_after="invalid_date")

    @patch("rpidash.models.model_manager.db_session")
    @patch("rpidash.models.model_manager.ModelManager.get_models")
    def test_store_record(self, mock_get_models, mock_db_session):
        """Test store_record method."""
        mock_get_models.return_value = self.models
        manager = ModelManager("cpu_temperature")

        manager.store_record(50)
        instance = manager.model()
        setattr(instance, "temperature", 50)
        mock_db_session.add.assert_called_with(instance)
        mock_db_session.commit.assert_called_once()

    @patch("rpidash.models.model_manager.db_session")
    @patch("rpidash.models.model_manager.ModelManager.get_models")
    def test_delete_records(self, mock_get_models, mock_db_session):
        """Test delete_records method."""
        mock_get_models.return_value = self.models
        manager = ModelManager()

        older_than = 3600
        cutoff_date = datetime.now() - timedelta(seconds=older_than)

        manager.delete_records(older_than)

        self.mock_cpu_temperature.query.filter.assert_called_with(
            self.mock_cpu_temperature.date < cutoff_date,
        )
        self.mock_cpu_temperature.query.filter().delete.assert_called_once()

        self.mock_cpu_utilization.query.filter.assert_called_with(
            self.mock_cpu_temperature.date < cutoff_date,
        )
        self.mock_cpu_utilization.query.filter().delete.assert_called_once()

        self.mock_memory_utilization.query.filter.assert_called_with(
            self.mock_cpu_temperature.date < cutoff_date,
        )
        self.mock_memory_utilization.query.filter().delete.assert_called_once()

        mock_db_session.commit.assert_called()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
