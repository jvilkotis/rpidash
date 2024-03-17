# STDLIB
import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

# FIRST PARTY
from rpidash.utils import (
    get_cpu_percentage,
    get_cpu_temperature,
    get_memory_utilization,
    get_project_version,
    get_storage_utilization,
    load_app_config,
)


class TestUtils(unittest.TestCase):
    """Unit tests for utility functions."""

    @patch(
        "psutil.sensors_temperatures",
        return_value={"coretemp": [(1, 50), (2, 60), (3, 55)]},
    )
    def test_get_cpu_temperature_valid(self, mock_sensors_temperatures):  # pylint: disable=unused-argument
        """Test get_cpu_temperature with valid sensors data."""
        result = get_cpu_temperature()
        self.assertEqual(result, "55.00")

    @patch("psutil.sensors_temperatures", return_value={})
    def test_get_cpu_temperature_no_cores(self, mock_sensors_temperatures):  # pylint: disable=unused-argument
        """Test get_cpu_temperature with missing sensors data."""
        result = get_cpu_temperature()
        self.assertIsNone(result)

    @patch("psutil.cpu_percent", return_value=50)
    def test_get_cpu_percentage_valid_utilization(self, mock_cpu_percent):  # pylint: disable=unused-argument
        """Test get_cpu_percentage with valid CPU utilization."""
        self.assertEqual(get_cpu_percentage(), "50.00")

    @patch("psutil.cpu_percent", return_value=0)
    def test_get_cpu_percentage_zero_tilization(self, mock_cpu_percent):  # pylint: disable=unused-argument
        """Test get_cpu_percentage with zero CPU utilization."""
        self.assertIsNone(get_cpu_percentage())

    @patch(
        "psutil.virtual_memory",
        return_value=MagicMock(percent=50, used=536870912, total=1073741824),
    )
    def test_get_memory_utilization(self, mock_virtual_memory):  # pylint: disable=unused-argument
        """Test get_memory_utilization function."""
        expected_result = ("50.00", "512", "1024")
        self.assertEqual(get_memory_utilization(), expected_result)

    @patch(
        "psutil.disk_usage",
        return_value=MagicMock(percent=50, used=536870912, total=1073741824),
    )
    def test_get_storage_utilization(self, mock_disk_usage):  # pylint: disable=unused-argument
        """Test get_storage_utilization function."""
        expected_result = ("50.00", "0", "1")
        self.assertEqual(get_storage_utilization(), expected_result)

    @patch.dict("os.environ", {"FLASK_ENV": "production"})
    @patch("yaml.safe_load")
    @patch("builtins.open")
    def test_load_app_config_production(
            self,
            mock_open_file,
            mock_yaml_load,
    ):  # pylint: disable=unused-argument
        """Test load_app_config in production environment."""
        load_app_config()
        mock_open_file.assert_called_once_with(
            "/path/in/container/config/config.yaml",
            "r",
            encoding="utf-8",
        )

    @patch.dict("os.environ", {"FLASK_ENV": "development"})
    @patch("os.path")
    @patch("yaml.safe_load", return_value={"key": "value"})
    @patch("builtins.open", new_callable=mock_open)
    def test_load_app_config_development(
            self,
            mock_open_file,
            mock_yaml_load,
            mock_os_path,
    ):  # pylint: disable=unused-argument
        """Test load_app_config in development environment."""
        mock_os_path.dirname.return_value = "/path/to/package"
        mock_os_path.join.side_effect = lambda *args: "/".join(args)
        result = load_app_config()
        mock_open_file.assert_called_once_with(
            "/path/to/package/config.dev.yaml",
            "r",
            encoding="utf-8",
        )
        self.assertEqual(result, {"key": "value"})

    @patch("os.path")
    @patch("yaml.safe_load", return_value={"key": "value"})
    @patch("builtins.open", new_callable=mock_open)
    def test_load_app_config_testing(
            self,
            mock_open_file,
            mock_yaml_load,
            mock_os_path,
    ):  # pylint: disable=unused-argument
        """Test load_app_config in testing environment."""
        mock_os_path.dirname.return_value = "/path/to/package"
        mock_os_path.join.side_effect = lambda *args: "/".join(args)
        result = load_app_config()
        mock_open_file.assert_called_once_with(
            "/path/to/package/config.test.yaml",
            "r",
            encoding="utf-8",
        )
        self.assertEqual(result, {"key": "value"})

    @patch.dict(os.environ, {"FLASK_ENV": "invalid"})
    def test_load_app_config_invalid_environment(self):
        """Test load_app_config with invalid environment."""
        with self.assertRaises(ValueError):
            load_app_config()

    @patch("os.path")
    @patch("toml.load", return_value={"project": {"version": "1.0"}})
    @patch("builtins.open", new_callable=mock_open)
    def test_get_project_version(
            self,
            mock_open_file,
            mock_toml_load,
            mock_os_path,
    ):  # pylint: disable=unused-argument
        """Test get_project_version."""
        mock_os_path.dirname.return_value = "/path/to/project/root"
        mock_os_path.join.side_effect = lambda *args: "/".join(args)
        result = get_project_version()
        mock_open_file.assert_called_once_with(
            "/path/to/project/root/pyproject.toml",
            "r",
            encoding="utf-8",
        )
        self.assertEqual(result, "1.0")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
