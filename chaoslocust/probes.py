from typing import TypedDict, List

from chaoslib.types import Configuration

from .driver import LocustDriver

__all__ = ["is_locust_running", "get_current_stats"]


class LocustApiStats(TypedDict):
    current_fail_per_sec: float


class LocustStats(TypedDict):
    current_response_time_percentile_50: float
    current_response_time_percentile_95: float
    current_fail_per_sec: float
    fail_ratio: float
    state: str
    total_rps: float
    user_count: float
    stats: List[LocustApiStats]


def is_locust_running(configuration: Configuration = None):
    locust_configuration = configuration.get("locust")
    driver = LocustDriver(host=locust_configuration.get("host"))
    is_locust_running = driver.locust_health_check()
    return is_locust_running


def __aggregate_api_stats(stats: LocustStats):
    if "stats" in stats:
        stats["current_fail_per_sec"] = sum([s.get("current_fail_per_sec") for s in stats.get("stats")])


def get_current_stats(metric_name: str, configuration: Configuration = None) -> float:
    """
    Available metric_name values:
    - current_response_time_percentile_50
    - current_response_time_percentile_95
    - current_fail_per_sec
    - fail_ratio
    - total_rps
    - user_count
    - state                 " current test state [ready,running,stopped]

    :param metric_name: The name of the test metric
    :param configuration: the LocustDriver configuration
    :return: the metric value
    """
    locust_configuration = configuration.get("locust")
    driver = LocustDriver(host=locust_configuration.get("host"))
    stats = driver.request_stats()
    if not stats:
        raise RuntimeError(f"Unable to read stats from locust server {locust_configuration.get('host')}")

    __aggregate_api_stats(stats)

    if metric_name in stats:
        return stats.get(metric_name)
    else:
        raise ValueError(f"Unable to find metric key with name {metric_name}")
