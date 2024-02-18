# THIRD PARTY
from flask import Flask

# FIRST PARTY
from rpidash.services.current_utilization import CurrentUtilization
from rpidash.views.dash import Dash


def create_app() -> Flask:
    """Create and configure the app."""
    app = Flask(__name__)

    # Template views
    app.add_url_rule("/", view_func=Dash.as_view("dash"))

    # API views
    app.add_url_rule(
        "/services/current_utilization",
        view_func=CurrentUtilization.as_view("current_utilization"),
    )

    return app
