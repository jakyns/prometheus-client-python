from prometheus_client import Counter, Histogram

from metrics.event import Event


class SampleEvent(Event):
    LABELS = ["error"]
    METRICS = {
        "result": Counter("sample_result", "sample result", LABELS),
        "latency": Histogram(
            "sample_latency",
            "sample latency",
            LABELS,
            buckets=[
                1000,
                2000,
                3000,
                5000,
                10000,
                30000,
                60000,
                120000,
                300000,
            ],  # 1s to 5m
        ),
    }

    # protected

    def _transform_result(self, result):
        if isinstance(result, dict) and "error" in result:
            return {"error": result["error"]}
        else:
            return {"error": None}
