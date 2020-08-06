import random
import time

from prometheus_client import start_http_server

from metrics import Metrics

if __name__ == "__main__":
    start_http_server(80)

    while True:
        # record metric every second
        with Metrics("sample") as metrics:
            try:
                # random between 1s and 10s
                time.sleep(random.randint(1000, 10000) / 1000)
                result = "response"
            except Exception as e:
                result = {}
                result["error"] = e

            metrics.record(result)
