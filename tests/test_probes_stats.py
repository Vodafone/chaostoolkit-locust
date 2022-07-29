import json
import unittest

import pytest
import requests_mock

from chaoslocust.probes import get_current_stats

BASE_URL = "http://localhost:8089"
LOCUST_CONFIGURATION = {
    "locust": {
        "host": BASE_URL
    }
}


class TestLocustProbeStats(unittest.TestCase):

    def test_get_stats(self):
        metric_name = "current_response_time_percentile_50"
        locust_response = json.dumps({
            metric_name: 100
        })
        with requests_mock.Mocker() as mock_request:
            mock_request.get(f"{BASE_URL}/stats/requests", text=locust_response)

            resolved = get_current_stats(metric_name=metric_name, configuration=LOCUST_CONFIGURATION)
            assert resolved == 100

    def test_get_stats_locust_unavailable(self):
        metric_name = "current_response_time_percentile_50"
        with requests_mock.Mocker() as mock_request:
            mock_request.get(f"{BASE_URL}/stats/requests", status_code=500)

            with pytest.raises(RuntimeError):
                get_current_stats(metric_name=metric_name, configuration=LOCUST_CONFIGURATION)

    def test_get_stats_metric_not_found(self):
        unknown_metric_name = "unknown_metric"
        with requests_mock.Mocker() as mock_request:
            mock_request.get(f"{BASE_URL}/stats/requests", text=json.dumps({"key": "value"}))

            with pytest.raises(ValueError):
                get_current_stats(metric_name=unknown_metric_name, configuration=LOCUST_CONFIGURATION)

    def test_get_stats_metric_current_fail_aggregation(self):
        locust_response = json.dumps({
            "stats": [
                {"current_fail_per_sec": 0.8},
                {"current_fail_per_sec": 1.2}
            ]})
        with requests_mock.Mocker() as mock_request:
            mock_request.get(f"{BASE_URL}/stats/requests", text=locust_response)

            resolved = get_current_stats(metric_name="current_fail_per_sec", configuration=LOCUST_CONFIGURATION)
            assert resolved == 2.0
