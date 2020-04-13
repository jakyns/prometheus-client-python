import time

from prometheus_client import start_http_server

from metrics import Metrics

if __name__ == "__main__":
    start_http_server(80)

    while True:
        # record metric every second
        with Metrics("sample") as metrics:
            result = {}

            try:
                time.sleep(1)
            except Exception as e:
                result["error"] = e

            metrics.record(result)
