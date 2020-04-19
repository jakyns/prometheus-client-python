import time
from typing import Any

from metrics.event.sample_event import SampleEvent


class Metrics:
    WHITELISTED_EVENT = [SampleEvent()]

    def __init__(self, event: str):
        self.event = event

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *exc):
        return

    def record(self, result: Any) -> None:
        try:
            event = self.__known_events()[self.event]
            event.record(result, start_time=self.start_time)
        except KeyError:
            raise NotImplementedError("unknown metrics event")

    # private

    def __known_events(self) -> dict:
        event_list = {}

        for event in self.WHITELISTED_EVENT:
            event_name = event._camel_to_snake(event).replace("_event", "")
            event_list[str(event_name)] = event

        return event_list
