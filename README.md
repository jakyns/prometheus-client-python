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
- add `Metrics.record("{event_name}", "{dict_object}")` line inside context
  `with Metrics("{event_name}") as metrics:` to collect metric

eg.

```
with Metrics("sample") as metrics:
    try:
        time.sleep(1)
        result = "response"
    except Exception as e:
        result = {}
        result["error"] = e

    metrics.record(result)
```

### docker-compose

```sh
docker-compose up
```

You can see how it collects metrics in Prometheus from http://0.0.0.0 and can
observe all metrics by adding metrics souce from prometheus protocol by
http://0.0.0.0:9090 and configure to any types of dashboard as you wish in
Grafana by http://0.0.0.0:3000.
