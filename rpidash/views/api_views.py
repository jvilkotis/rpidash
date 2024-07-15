# STDLIB
from abc import ABC, abstractmethod

# THIRD PARTY
from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import View

# FIRST PARTY
from rpidash.models.model_manager import ModelManager
from rpidash.services.system_utilization import SystemUtilization


class UtilizationBase(ABC, View):
    """System utilization base view."""

    def dispatch_request(self, **kwargs) -> ResponseReturnValue:
        """Render API view."""
        kwargs.update(request.args)
        try:
            return jsonify(self.prepare_response(**kwargs))
        except ValueError as exc:
            response = {
                "error": f"Failed to retrieve data: {exc}"
            }
            return jsonify(response), 400

    @abstractmethod
    def prepare_response(self, **kwargs):
        """Prepare JSON response."""


class CurrentUtilization(UtilizationBase):
    """Current system utilization view."""

    def prepare_response(self, **kwargs) -> dict:
        """Prepare current system utilization JSON response."""
        return SystemUtilization().all().to_dict()


class UtilizationHistory(UtilizationBase):
    """System utilization history view."""

    def prepare_response(self, **kwargs) -> dict:
        """Prepare system utilization history JSON response."""
        return ModelManager(kwargs["table_name"]).retrieve_data(
            kwargs.get("recorded_after"),
        )
