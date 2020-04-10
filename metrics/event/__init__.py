class Event:
    def record(self, result):
        self.record_realtime(result)

        if not result["error"]:
            self.record_success(result)
        else:
            self.record_failure(result["error"])
