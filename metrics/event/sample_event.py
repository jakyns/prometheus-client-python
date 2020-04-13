import re
import time

from prometheus_client import Counter, Histogram

from metrics.event import Event


class SampleEvent(Event):
    METRICS = {
        "result": Counter("sample_result", "sample result", ["error"]),
        "latency": Histogram("sample_latency", "sample latency"),
    }

    def record_realtime(self, result):
        start_time = result["start_time"]
        duration = (time.time() - start_time) * 1000

        self.METRICS["latency"].observe(duration)

    def record_success(self, result):
        self.METRICS["result"].labels(error=None).inc()

    def record_failure(self, e):
        e = self._camel_to_snake(e)
        self.METRICS["result"].labels(error=e).inc()

    # protected

    def _camel_to_snake(self, instance=None) -> str:
        name = instance.__class__.__name__
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
