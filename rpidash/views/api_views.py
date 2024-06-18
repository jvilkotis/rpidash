# STDLIB
import inspect
from abc import ABC, abstractmethod
from typing import Any, Dict, List

# THIRD PARTY
from flask import jsonify
from flask.typing import ResponseReturnValue
from flask.views import View

# FIRST PARTY
from rpidash import models
from rpidash.system_utilization import SystemUtilization


class UtilizationBase(ABC, View):
    """System utilization base view."""

    def dispatch_request(self, **kwargs) -> ResponseReturnValue:
        """Render API view."""
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

    @staticmethod
    def get_model(table_name: str) -> Any:
        """Get model by table name."""
        for _, model in inspect.getmembers(models):
            if inspect.isclass(model) and model.__module__ == models.__name__:
                if model.__tablename__ == table_name:
                    return model
        raise ValueError(f"Model for table '{table_name}' not found.")

    @staticmethod
    def retrieve_data(model: Any) -> dict[str, list[Any]]:
        """Retrieve data from database."""
        data = model.query.all()
        values = []
        dates = []
        if model.__tablename__ == "cpu_temperature":
            value_key = "temperature"
        else:
            value_key = "percentage"
        for item in data:
            values.append(getattr(item, value_key))
            dates.append(item.date)
        return {"values": values, "dates": dates}

    def get_data(self, table_name: str) -> Any:
        """Get model and retrieve data."""
        model = self.get_model(table_name)
        return self.retrieve_data(model)

    def prepare_response(self, **kwargs) -> List[Dict[str, Any]]:
        """Prepare system utilization history JSON response."""
        data = self.get_data(kwargs["table_name"])
        return data
