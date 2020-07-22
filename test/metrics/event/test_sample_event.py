import time
import unittest

import mock
from prometheus_client import Counter, Histogram

from metrics.event.sample_event import SampleEvent


class TestSampleEvent(unittest.TestCase):
    def setUp(self):
        self.event = SampleEvent()

    @mock.patch.object(Histogram, "observe")
    @mock.patch.object(Counter, "inc")
    def test_that_record_success_metric_if_there_is_no_error(
        self, mock_record_success: mock.MagicMock, mock_record_realtime: mock.MagicMock
    ):
        self.event.record({"status": True}, start_time=time.time())

        mock_record_realtime.assert_called_once()
        mock_record_success.assert_called_once()

    @mock.patch.object(Histogram, "observe")
    @mock.patch.object(Counter, "inc")
    def test_that_record_failure_metric_if_error_occurs(
        self, mock_record_failure: mock.MagicMock, mock_record_realtime: mock.MagicMock
    ):
        with self.assertRaises(ValueError):
            self.event.record({"error": ValueError}, start_time=time.time())

        mock_record_realtime.assert_called_once()
        mock_record_failure.assert_called_once()
