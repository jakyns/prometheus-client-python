import time
import unittest

import mock

from metrics import Metrics
from metrics.event.sample_event import SampleEvent


class TestMetrics(unittest.TestCase):
    @mock.patch.object(SampleEvent, "record")
    def test_that_metric_can_record(self, mock_record: mock.MagicMock):
        result = {"status": True}

        metric = Metrics("sample")
        metric.start_time = time.time()

        metric.record(result)

        mock_record.assert_called_once_with(result, start_time=metric.start_time)

    def test_that_raises_unknown_metrics_when_metric_is_not_in_whitelise(self):
        metric = Metrics("unknown")
        metric.start_time = time.time()

        with self.assertRaises(NotImplementedError):
            metric.record({"status": True})
