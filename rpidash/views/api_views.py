# STDLIB
import inspect
from typing import TypeVar

# THIRD PARTY
from flask.typing import ResponseReturnValue
from flask.views import View
from sqlalchemy.orm import DeclarativeMeta

# FIRST PARTY
from rpidash import models
from rpidash.utils import (
    get_cpu_percentage,
    get_cpu_temperature,
    get_memory_utilization,
    get_storage_utilization,
)

UtilizationModel = TypeVar("UtilizationModel", bound=DeclarativeMeta)


class UtilizationBase(View):
    """System utilization base view."""

    def dispatch_request(self, **kwargs) -> ResponseReturnValue:
        """Render API view."""
        response = self.prepare_response(**kwargs)
        return response

    def prepare_response(self, **kwargs):
        """Prepare JSON response."""
        raise NotImplementedError


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
    def get_model(**kwargs) -> UtilizationModel:
        """Get model by table name path parameter."""
        for _, obj in inspect.getmembers(models):
            if inspect.isclass(obj) and obj.__module__ == models.__name__:
                if getattr(obj, "__tablename__") == kwargs["table_name"]:
                    return obj
        raise NotImplementedError

    @staticmethod
    def retrieve_data(model: UtilizationModel) -> list:
        """Retrieve data from database."""
        data = model.query.all()
        results = []
        for item in data:
            data_dict = item.__dict__
            del data_dict["_sa_instance_state"]
            results.append(data_dict)
        return results

    def prepare_response(self, **kwargs):
        """Prepare system utilization history JSON response."""
        model = self.get_model(**kwargs)
        response = self.retrieve_data(model)
        return response
