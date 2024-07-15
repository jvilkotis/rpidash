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

    @patch("rpidash.services.system_utilization.SystemUtilization.all")
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

    @patch("rpidash.views.api_views.ModelManager")
    def test_prepare_response(
        self,
        mock_model_manager,
    ):
        """Test prepare_response method."""
        mock_model_manager.return_value = MagicMock()
        mock_model_manager.return_value.retrieve_data.return_value = {
            "values": [50, 50],
            "dates": ["2024-01-01", "2024-01-02"],
        }
        history = UtilizationHistory()
        kwargs = {
            "table_name": "test",
            "recorded_after": "2024-01-01"
        }
        response = history.prepare_response(**kwargs)
        expected_response = {
            "values": [50, 50],
            "dates": ["2024-01-01", "2024-01-02"],
        }

        self.assertEqual(response, expected_response)
        mock_model_manager.assert_called_once_with("test")
        mock_model_manager.return_value.retrieve_data.assert_called_once_with(
            "2024-01-01",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
