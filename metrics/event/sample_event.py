import re
import time

from prometheus_client import Counter, Histogram

from metrics.event import Event


class SampleEvent(Event):
    METRICS = {
        "result": Counter("request_result", "request result"),
        "latency": Histogram("request_latency", "request latency"),
    }

    def record_realtime(self, result):
        start_time = result["created_at"]
        duration = (time.time() - start_time) * 1000

        self.METRICS["latency"].observe(duration)

    def record_success(self, result):
        self.METRICS["result"].inc()

    def record_failure(self, e):
        e = self._camel_to_snake(e)
        self.METRICS["result"].inc()

    # protected

    def _camel_to_snake(self, instance=None) -> str:
        name = instance.__class__.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
