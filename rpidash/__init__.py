# STDLIB
import logging

# THIRD PARTY
from flask import Flask

# FIRST PARTY
from rpidash import database as db
from rpidash import models
from rpidash.scheduled_tasks import scheduler
from rpidash.utils import load_app_config
from rpidash.views.api_views import CurrentUtilization, UtilizationHistory
from rpidash.views.dashboard import Dashboard


def create_app() -> Flask:
    """Create and configure the app."""
    app = Flask(__name__)

    config = load_app_config()
    app.config.update(config)

    logging.basicConfig(
        level=config["logging"]["level"],
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Template views
    app.add_url_rule("/", view_func=Dashboard.as_view("dash"))

    # API views
    app.add_url_rule(
        "/services/current_utilization",
        view_func=CurrentUtilization.as_view("current_utilization"),
    )
    app.add_url_rule(
        "/services/<table_name>",
        view_func=UtilizationHistory.as_view("utilization_history"),
    )

    if config["scheduled_tasks"]["enabled"]:  # pragma: no cover
        scheduler.init_app(app)
        scheduler.start()

    db.init_db(database_uri=config["database"]["uri"])

    @app.teardown_appcontext
    def shutdown_session(exception=None):  # pylint: disable=unused-argument
        """
        Remove database sessions at the end of the requests and
        on the app shutdown.
        """
        db.db_session.remove()

    return app
