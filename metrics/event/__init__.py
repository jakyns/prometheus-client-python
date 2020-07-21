import re
import time
from typing import Any, Type


class Event:
    def record(self, result: Any, **kwargs: dict) -> None:
        labels = self._transform_result_to_labels(result)

        self.record_realtime(labels, **kwargs)

        if labels["error"]:
            self.record_failure(labels)
        else:
            self.record_success(labels)

    def record_realtime(self, labels: dict, **kwargs: dict) -> None:
        start_time = kwargs["start_time"]
        duration = (time.time() - start_time) * 1000

        self.METRICS["latency"].labels(**labels).observe(duration)

    def record_success(self, labels: dict) -> None:
        self.METRICS["result"].labels(**labels).inc()

    def record_failure(self, labels: dict) -> None:
        exception = labels["error"]
        labels["error"] = self._camel_to_snake(exception)

        self.METRICS["result"].labels(**labels).inc()

        raise exception

    # protected

    def _camel_to_snake(self, instance: Type[Any]) -> str:
        name = instance.__class__.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
