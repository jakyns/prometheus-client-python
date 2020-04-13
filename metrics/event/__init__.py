class Event:
    def record(self, result):
        self.record_realtime(result)

        if "error" in result:
            self.record_failure(result["error"])
        else:
            self.record_success(result)
