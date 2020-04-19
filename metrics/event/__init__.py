import re
import time
from typing import Any, Type


class Event:
    def record(self, result: Any, **kwargs: dict) -> None:
        result = self._transform_result(result)

        self.record_realtime(result, **kwargs)

        if result["error"]:
            self.record_failure(result)
        else:
            self.record_success(result)

    def record_realtime(self, result: dict, **kwargs: dict) -> None:
        start_time = kwargs["start_time"]
        duration = (time.time() - start_time) * 1000

        self.METRICS["latency"].labels(**result).observe(duration)

    def record_success(self, result: dict) -> None:
        self.METRICS["result"].labels(**result).inc()

    def record_failure(self, result: dict) -> None:
        exception = result["error"]
        result["error"] = self._camel_to_snake(exception)

        self.METRICS["result"].labels(**result).inc()

        raise exception

    # protected

    def _camel_to_snake(self, instance: Type[Any]) -> str:
        name = instance.__class__.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
