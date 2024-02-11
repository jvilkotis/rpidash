from flask import Flask
from rpidash.routes import routes


def create_app() -> Flask:
    """Create and configure the app."""
    app = Flask(__name__)

    app.register_blueprint(routes)

    return app
