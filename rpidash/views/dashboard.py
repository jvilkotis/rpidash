# THIRD PARTY
from flask import render_template
from flask.typing import ResponseReturnValue
from flask.views import View

# FIRST PARTY
from rpidash.utils.utils import get_project_version


class Dashboard(View):
    """Dashboard view."""

    def __init__(self):
        self.context = {}
        self.setup_context()

    def setup_context(self):
        """Setup template context."""
        self.context["version"] = get_project_version()

    def dispatch_request(self) -> ResponseReturnValue:
        """Render dashboard template view."""
        return render_template("dashboard.html", **self.context)
