# THIRD PARTY
from flask.typing import ResponseReturnValue
from flask.views import View

# FIRST PARTY
from rpidash.utils import (
    get_cpu_temperature,
    get_cpu_utilization,
    get_memory_utilization,
    get_storage_utilization,
)


class CurrentUtilization(View):
    """Current system utilization view."""

    def dispatch_request(self) -> ResponseReturnValue:
        """Render current system utilization API view."""
        memory_percentage, memory_used, memory_total = get_memory_utilization()
        storage_percentage, storage_used, storage_total = get_storage_utilization()
        response = {
            "cpu_temperature": get_cpu_temperature(),
            "cpu_percentage": get_cpu_utilization(),
            "memory_percentage": memory_percentage,
            "memory_used": memory_used,
            "memory_total": memory_total,
            "storage_percentage": storage_percentage,
            "storage_used": storage_used,
            "storage_total": storage_total,
        }
        return response
