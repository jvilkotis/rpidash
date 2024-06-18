# STDLIB
import os
import unittest
from unittest.mock import mock_open, patch

# FIRST PARTY
from rpidash.utils import get_project_version, load_app_config


class TestUtils(unittest.TestCase):
    """Unit tests for utility functions."""

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
            "/data/config.yaml",
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
