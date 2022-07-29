import json
import requests

from logzero import logger


class LocustDriver():
    def __init__(self, host: str = None):
        self.host = host
        self.swarm_url_path = "/swarm"
        self.stop_url_path = "/stop"
        self.requests_stats_url_path = "/stats/requests"
        self.timeout = 5
        self.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    def is_status_code_correct(self, response):
        return response and response.status_code == 200

    def start_locust(self, user_count: int, spawn_rate: float, host: str):
        url = self.host + self.swarm_url_path
        data = f"user_count={user_count}&spawn_rate={spawn_rate}&host={host}"
        try:
            response = requests.post(url=url, data=data, headers=self.headers, timeout=self.timeout)
            return self.is_status_code_correct(response)
        except Exception:
            return False

    def stop_locust(self):
        url = self.host + self.stop_url_path
        try:
            response = requests.get(url=url, timeout=self.timeout)
            return self.is_status_code_correct(response)
        except Exception:
            return False

    def locust_health_check(self):
        url = self.host
        try:
            response = requests.get(url=url, timeout=self.timeout)
            return self.is_status_code_correct(response)
        except Exception:
            return False

    def request_stats(self):
        url = self.host + self.requests_stats_url_path
        try:
            response = requests.get(url=url, timeout=self.timeout)
            if self.is_status_code_correct(response):
                return json.loads(response.content)
            elif response:
                raise RuntimeError(
                    f"Error occurred while retrieving locust stats: status_code[{response.status_code}], body:\n{response.content}"
                )
            else:
                raise RuntimeError("Request returned a null response")
        except Exception as e:
            logger.error(e)
        return None
