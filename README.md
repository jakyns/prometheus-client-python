# Prometheus Metrics Collector Model

Sample app for collecting metrics into Prometheus by specific event class.

## Dependencies

- Python 3.7.x or higher
- [Pipfile](https://github.com/pypa/pipfile)

## Installation

Initiate virtual environment and generate Pipfile and Pipfile.lock by running:

```sh
pipenv lock
```

Install dependencies and get into virtual environment.

```sh
pipenv install && pipenv shell
```

## Development

Running in local by

```sh
python app.py
```

## Usage

in case of you want to create your own event
- implement your event class (must end with `_event` suffix) to `metrics/event/`
- add your new event class to constant `WHITELISTED_EVENT` in `metrics/__init__.py`
- add `Metrics.record("{event_name}", "{value}")` line inside context
  `with Metrics("{event_name}") as metrics:` to collect metric

eg. it has a sample event in `metrics/event/sample_event.py`

```python
from metrics import Metrics

with Metrics("sample") as metrics:
    try:
        time.sleep(1)
        result = "response"
    except Exception as e:
        result = {}
        result["error"] = e

    metrics.record(result)
```

## Custom Labels

- add label to `LABELS` constant

```python
LABELS["error", "status"]
```

- modify `_transform_result` method in event class 

```python
def _transform_result(self, result: Any) -> dict:
    if isinstance(result, dict) and "error" in result:
        return {"status": "error", "error": result["error"]}
    else:
        return {"status": result.status, "error": None}
```

### docker-compose

```sh
docker-compose up
```

You can see how it collects metrics in Prometheus from http://0.0.0.0 and can
observe all metrics by adding metrics souce from prometheus protocol by
http://0.0.0.0:9090 and configure to any types of dashboard as you wish in
Grafana by http://0.0.0.0:3000.
