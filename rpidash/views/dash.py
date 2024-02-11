from flask import render_template
from flask.typing import ResponseReturnValue
from flask.views import View


class Dash(View):
    def dispatch_request(self) -> ResponseReturnValue:
        return render_template(template_name_or_list="index.html")
