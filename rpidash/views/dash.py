# THIRD PARTY
from flask import render_template
from flask.typing import ResponseReturnValue
from flask.views import View


class Dash(View):
    """Dashboard view."""

    def dispatch_request(self) -> ResponseReturnValue:
        """Render dashboard template view."""
        return render_template("index.html")
