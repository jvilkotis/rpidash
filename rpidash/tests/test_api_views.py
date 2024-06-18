# STDLIB
import unittest
from unittest.mock import MagicMock, patch

# FIRST PARTY
from rpidash import create_app
from rpidash.views.api_views import (
    CurrentUtilization,
    UtilizationBase,
    UtilizationHistory,
)


class TestUtilizationBase(unittest.TestCase):
    """A test suite for the UtilizationBase class."""

    @patch.multiple(UtilizationBase, __abstractmethods__=set())
    def setUp(self):
        """Set up common attributes for tests."""
        self.app = create_app()
        self.instance = UtilizationBase()  # pylint: disable=abstract-class-instantiated

    @patch("rpidash.views.api_views.UtilizationBase.prepare_response")
    def test_dispatch_request_success(self, mock_prepare_response):
        """Test dispatch_request method with successful response."""
        mock_prepare_response.return_value = {"data": "example"}
        with self.app.test_request_context():
            response = self.instance.dispatch_request()
        self.assertEqual(response.json, {"data": "example"})

    @patch("rpidash.views.api_views.UtilizationBase.prepare_response")
    def test_dispatch_request_error(self, mock_prepare_response):
        """Test dispatch_request method with error response."""
        mock_prepare_response.side_effect = ValueError("Test error")
        with self.app.test_request_context():
            response, status = self.instance.dispatch_request()
        self.assertEqual(
            response.json,
            {"error": "Failed to retrieve data: Test error"},
        )
        self.assertEqual(status, 400)


class TestCurrentUtilization(unittest.TestCase):
    """A test suite for the CurrentUtilization class."""

    @patch("rpidash.system_utilization.SystemUtilization.all")
    def test_prepare_response(
            self,
            mock_system_utilization,
    ):
        """Test prepare_response method."""
        mock_system_utilization.return_value = MagicMock()
        mock_system_utilization.return_value.to_dict.return_value = {
            "test_metric1": 50.0,
            "test_metric2": 49.9,
        }
        utilization = CurrentUtilization()
        response = utilization.prepare_response()
        expected_response = {
            "test_metric1": 50.0,
            "test_metric2": 49.9,
        }

        self.assertEqual(response, expected_response)
        mock_system_utilization.assert_called_once()
        mock_system_utilization.return_value.to_dict.assert_called_once()


class TestUtilizationHistory(unittest.TestCase):
    """A test suite for the UtilizationHistory class."""

    @patch("rpidash.views.api_views.inspect", new_callable=MagicMock)
    @patch("rpidash.views.api_views.models")
    def test_get_model(self, mock_models, mock_inspect):
        """Test get_model method."""
        mock_model = MagicMock()
        mock_model.__tablename__ = "some_table"
        mock_models.__name__ = mock_model.__module__
        mock_inspect.isclass.return_value = True
        mock_inspect.getmembers.return_value = [(None, mock_model)]
        result = UtilizationHistory.get_model("some_table")
        self.assertEqual(result, mock_model)

    def test_get_model_raises_error(self):
        """Test get_model method when table does not exist."""
        with self.assertRaises(ValueError):
            UtilizationHistory.get_model("non_existent_table")

    def test_retrieve_data_temperature(self):
        """Test retrieve_data method with temperature value key."""
        mock_model = MagicMock()
        mock_model.__tablename__ = "cpu_temperature"
        item_dict = {
            "id": 1,
            "temperature": "99",
            "date": "1970-01-01",
            "_sa_instance_state": "something",
        }
        item = type("Item", (), item_dict)()
        mock_model.query.all.return_value = [item]
        result = UtilizationHistory.retrieve_data(mock_model)
        self.assertEqual(result, {"values": ["99"], "dates": ["1970-01-01"]})

    def test_retrieve_data_percentage(self):
        """Test retrieve_data method with percentage value key."""
        mock_model = MagicMock()
        mock_model.__tablename__ = "cpu_percentage"
        item_dict = {
            "id": 1,
            "percentage": "99",
            "date": "1970-01-01",
            "_sa_instance_state": "something",
        }
        item = type("Item", (), item_dict)()
        mock_model.query.all.return_value = [item]
        result = UtilizationHistory.retrieve_data(mock_model)
        self.assertEqual(result, {"values": ["99"], "dates": ["1970-01-01"]})

    @patch("rpidash.views.api_views.UtilizationHistory.get_model")
    @patch("rpidash.views.api_views.UtilizationHistory.retrieve_data")
    def test_get_data(self, mock_retrieve_data, mock_get_model):
        """Test get_data method."""
        table_name = "some_table"
        mock_model = MagicMock()
        mock_retrieve_data.return_value = [{"id": 1, "attribute": "test"}]
        mock_get_model.return_value = mock_model
        instance = UtilizationHistory()
        result = instance.get_data(table_name)
        mock_get_model.assert_called_once_with(table_name)
        mock_retrieve_data.assert_called_once_with(mock_model)
        self.assertEqual(result, [{"id": 1, "attribute": "test"}])

    @patch("rpidash.views.api_views.UtilizationHistory.get_data")
    def test_prepare_response(self, mock_get_data):
        """Test prepare_response method."""
        mock_get_data.return_value = [{"attribute": "value"}]
        instance = UtilizationHistory()
        result = instance.prepare_response(table_name="some_table")
        self.assertEqual(result, [{"attribute": "value"}])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
