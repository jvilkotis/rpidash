from flask import Blueprint

from rpidash.views.dash import Dash

routes = Blueprint(name="routes", import_name=__name__)

routes.add_url_rule(rule="/", view_func=Dash.as_view(name="dash"))
