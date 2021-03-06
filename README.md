# Prometheus Client - Python

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
- add your new event class into constant `WHITELISTED_EVENT` in `metrics/__init__.py`
- add `Metrics.record("{event_name}", "{value}")` in the last line of
  code block `with Metrics("{event_name}") as metrics:`.

eg. sample event in `metrics/event/sample_event.py`

```python
from metrics import Metrics

with Metrics("sample") as metrics:
    try:
        result = "response"
    except Exception as e:
        result = {"error": e}

    metrics.record(result)
```

## Custom Labels

- add label(s) you want to save to metric into `LABELS` constant

```python
LABELS["error", "status"]
```

- modify `_transform_result_to_labels` method which is responsible for wrapping
  labels to dict before saving to Prometheus in event class.

```python
def _transform_result_to_labels(self, result: Union[dict, Any]) -> dict:
    if isinstance(result, dict) and "error" in result:
        return {"status": "error", "error": result["error"]}
    else:
        return {"status": result["status"], "error": None}
```
