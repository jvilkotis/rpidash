# STDLIB
import unittest
from unittest.mock import patch

# FIRST PARTY
from rpidash.views.dashboard import Dashboard


class TestDashboard(unittest.TestCase):
    """A test suite for the Dashboard class."""

    @patch("rpidash.views.dashboard.get_project_version", return_value="1.0")
    def test_setup_context(self, mock_get_project_version):  # pylint: disable=unused-argument
        """Test setup_context method."""
        dashboard = Dashboard()
        self.assertEqual(dashboard.context["version"], "1.0")

    @patch("rpidash.views.dashboard.render_template")
    @patch("rpidash.views.dashboard.Dashboard.setup_context")
    def test_dispatch_request(self, mock_setup_context, mock_render_template):  # pylint: disable=unused-argument
        """Test dispatch_request method."""
        dashboard = Dashboard()
        dashboard.context = {"data": "example"}
        dashboard.dispatch_request()
        mock_render_template.assert_called_once_with(
            "dashboard.html",
            data="example",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
