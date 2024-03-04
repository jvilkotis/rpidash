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
from rpidash.utils import (
    get_cpu_percentage,
    get_cpu_temperature,
    get_memory_utilization,
    get_storage_utilization,
)


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
        memory_percentage, memory_used, memory_total = get_memory_utilization()
        storage_percentage, storage_used, storage_total = \
            get_storage_utilization()
        cpu_percentage = get_cpu_percentage()
        cpu_temperature = get_cpu_temperature()
        response = {
            "cpu_temperature": cpu_temperature if cpu_temperature else "0.00",
            "cpu_percentage": cpu_percentage if cpu_percentage else "0.00",
            "memory_percentage": memory_percentage,
            "memory_used": memory_used,
            "memory_total": memory_total,
            "storage_percentage": storage_percentage,
            "storage_used": storage_used,
            "storage_total": storage_total,
        }
        return response


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
    def retrieve_data(model: Any) -> List[Dict[str, Any]]:
        """Retrieve data from database."""
        data = model.query.all()
        processed_data = []
        for item in data:
            data_dict = item.__dict__
            del data_dict["_sa_instance_state"]
            processed_data.append(data_dict)
        return processed_data

    def get_data(self, table_name: str) -> Any:
        """Get model and retrieve data."""
        model = self.get_model(table_name)
        return self.retrieve_data(model)

    def prepare_response(self, **kwargs) -> List[Dict[str, Any]]:
        """Prepare system utilization history JSON response."""
        data = self.get_data(kwargs["table_name"])
        return data
