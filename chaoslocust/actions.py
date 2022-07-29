from chaoslib.types import Configuration
from .driver import LocustDriver

__all__ = [
    "start_locust",
    "stop_locust"
]

def start_locust(user_count:int = 0, spawn_rate: float = 1, host: str = "", configuration: Configuration = None):
    locust_configuration = configuration.get("locust")
    driver = LocustDriver(host=locust_configuration.get("host"))
    is_test_started = driver.start_locust(user_count, spawn_rate, host)
    return is_test_started

def stop_locust(configuration: Configuration = None):
    locust_configuration = configuration.get("locust")
    driver = LocustDriver(host=locust_configuration.get("host"))
    is_test_stopped = driver.stop_locust()
    return is_test_stopped