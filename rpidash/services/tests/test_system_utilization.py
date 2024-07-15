# STDLIB
import unittest
from unittest.mock import MagicMock, patch

# FIRST PARTY
from rpidash.services.system_utilization import SystemUtilization


class TestSystemUtilization(unittest.TestCase):
    """A test suite for the system utilization metric class."""

    @patch("rpidash.services.system_utilization.psutil")
    def test_get_cpu_temperature(self, mock_psutil):
        """Test get_cpu_temperature with valid coretemp return value."""
        mock_psutil.sensors_temperatures.return_value = {
            "coretemp": [(1, 50), (2, 60), (3, 55)]
        }
        system_util = SystemUtilization().get_cpu_temperature()
        self.assertEqual(system_util.cpu_temperature, 55.0)

    @patch("rpidash.services.system_utilization.psutil")
    def test_get_cpu_temperature_valid_cpu_thermal(self, mock_psutil):
        """Test get_cpu_temperature with valid cpu_thermal return value."""
        mock_psutil.sensors_temperatures.return_value = {
            "cpu_thermal": [(1, 50), (2, 60), (3, 70)],
        }
        system_util = SystemUtilization().get_cpu_temperature()
        self.assertEqual(system_util.cpu_temperature, 60.0)

    @patch("rpidash.services.system_utilization.psutil")
    def test_get_cpu_temperature_no_cores(self, mock_psutil):
        """Test get_cpu_temperature with missing sensor data."""
        mock_psutil.sensors_temperatures.return_value = {}
        system_util = SystemUtilization().get_cpu_temperature()
        self.assertEqual(system_util.cpu_temperature, 0.0)

    @patch("rpidash.services.system_utilization.psutil")
    def test_get_cpu_temperature_no_attribute(self, mock_psutil):
        """Test get_cpu_temperature with no sensors_temperatures attribute."""
        mock_psutil.sensors_temperatures.side_effect = AttributeError
        system_util = SystemUtilization().get_cpu_temperature()
        self.assertEqual(system_util.cpu_temperature, 0.0)

    @patch("psutil.cpu_percent", return_value=50)
    def test_get_cpu_percentage_valid_utilization(self, mock_cpu_percent):  # pylint: disable=unused-argument
        """Test get_cpu_percentage with valid CPU utilization."""
        system_util = SystemUtilization().get_cpu_percentage()
        self.assertEqual(system_util.cpu_percentage, 50.0)

    @patch(
        "psutil.virtual_memory",
        return_value=MagicMock(percent=50, used=536870912, total=1073741824),
    )
    def test_get_memory_utilization(self, mock_virtual_memory):  # pylint: disable=unused-argument
        """Test get_memory_utilization function."""
        system_util = SystemUtilization().get_memory_utilization()
        self.assertEqual(system_util.memory_percentage, 50.0)
        self.assertEqual(system_util.memory_used, 512.0)
        self.assertEqual(system_util.memory_total, 1024.0)

    @patch(
        "psutil.disk_usage",
        return_value=MagicMock(percent=50, used=536870912, total=1073741824),
    )
    def test_get_storage_utilization(self, mock_disk_usage):  # pylint: disable=unused-argument
        """Test get_storage_utilization function."""
        system_util = SystemUtilization().get_storage_utilization()
        self.assertEqual(system_util.storage_percentage, 50.0)
        self.assertEqual(system_util.storage_used, 0.5)
        self.assertEqual(system_util.storage_total, 1.0)

    @patch(
        "rpidash.services.system_utilization"
        ".SystemUtilization.get_cpu_temperature"
    )
    @patch(
        "rpidash.services.system_utilization"
        ".SystemUtilization.get_cpu_percentage"
    )
    @patch(
        "rpidash.services.system_utilization"
        ".SystemUtilization.get_memory_utilization"
    )
    @patch(
        "rpidash.services.system_utilization"
        ".SystemUtilization.get_storage_utilization"
    )
    def test_all_methods_called(
        self,
        mock_get_storage_utilization,
        mock_get_memory_utilization,
        mock_get_cpu_percentage,
        mock_get_cpu_temperature,
    ):
        """Test that all methods are called by the all() method."""
        system_util = SystemUtilization()
        system_util.all()

        mock_get_cpu_temperature.assert_called_once()
        mock_get_cpu_percentage.assert_called_once()
        mock_get_memory_utilization.assert_called_once()
        mock_get_storage_utilization.assert_called_once()

    def test_to_dict(self):
        """Test to_dict method returns correct dictionary."""
        system_util = SystemUtilization()
        result = system_util.to_dict()

        expected_dict = {
            "cpu_temperature": 0.0,
            "cpu_percentage": 0.0,
            "memory_percentage": 0.0,
            "memory_used": 0.0,
            "memory_total": 0.0,
            "storage_percentage": 0.0,
            "storage_used": 0.0,
            "storage_total": 0.0,
        }

        self.assertEqual(result, expected_dict)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
