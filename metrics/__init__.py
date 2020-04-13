import time

from metrics.event.sample_event import SampleEvent


class Metrics:
    WHITELISTED_EVENT = [SampleEvent()]

    def __init__(self, event):
        self.event = event

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *exc):
        return

    def record(self, result):
        try:
            event = self.__known_events()[self.event]
            result = dict(result, **{"start_time": self.start_time})
            event.record(result)
        except KeyError:
            raise NotImplementedError("unknown metrics event")

    # private

    def __known_events(self):
        event_list = {}

        for event in self.WHITELISTED_EVENT:
            event_name = event._camel_to_snake(event).replace("_event", "")
            event_list[str(event_name)] = event

        return event_list
