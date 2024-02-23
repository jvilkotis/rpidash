# THIRD PARTY
from flask import Flask

# FIRST PARTY
from rpidash import database as db
from rpidash import models
from rpidash.views.api_views import CurrentUtilization, UtilizationHistory
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
    app.add_url_rule(
        "/services/<table_name>",
        view_func=UtilizationHistory.as_view("utilization_history"),
    )

    db.init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-argument
        """Remove database sessions at the end of the requests and on the app shutdown."""
        db.db_session.remove()

    return app
