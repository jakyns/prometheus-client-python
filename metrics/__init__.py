from metrics.event.sample_event import SampleEvent


class Metrics:
    WHITELISTED_EVENT = [SampleEvent()]

    @classmethod
    def record(cls, event, result):
        try:
            event = cls().__known_events()[event]
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
