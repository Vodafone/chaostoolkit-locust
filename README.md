# Locust extension for the Chaos Toolkit

Locust is a python based open source performance testing tool:
https://locust.io/
Chaostoolkit-locust module provides actions to start/stop Locust open source performance testing tool.
It also provides proves to check it status and to get the locust test run statistics.

## Install

The extension is not yet pushed to PyPi. If you would like to use the extension please
checkout the source code and compile it locally.


### Install python dependencies
First navigate to the project root and run the following command:
```bash
python3 -m pip install -r requirements.txt
```

If you use pipenv and virtual python environment please use the following command:
```bash
pipenv install -r requirements.txt
```

### Install python dev dependencies
```bash
python3 -m pip install -r requirements-dev.txt
```

```bash
pipenv install -r requirements-dev.txt
```

### Build extension locally

```bash
python3 setup.py bdist_wheel;
python3 -m pip install dist/chaostoolkit_locust-0.0.1-py3-none-any.whl
```

## Usage

To use the probe and check Locust.io status, please insert the following into an experiment file:
```json
{
  "steady-state-hypothesis": {
    "title": "Locust server must be running",
    "probes": [
      {
        "type": "probe",
        "name": "is_locust_running",
        "tolerance": true,
        "provider": {
          "type": "python",
          "module": "chaoslocust.probes",
          "func": "is_locust_running"
        }
      }
    ]
  }
}
```
If you want to start Locust.io, please use the following action in an experiment file:
```json
{
  "method": [
    {
      "type": "action",
      "name": "start_locust_test",
      "provider": {
        "type": "python",
        "module": "chaoslocust.actions",
        "func": "start_locust",
        "arguments": {
          "user_count": 10,
          "spawn_rate": 1,
          "host": "localhost"
        }
      }
    }
  ]
}
```
If you want to stop Locust.io, please use the following action in an experiment file:
```json
{
  "method": [
    {
      "type": "action",
      "name": "stop_locust_test",
      "provider": {
        "type": "python",
        "module": "chaoslocust.actions",
        "func": "stop_locust"
      }
    }
  ]
}
```
If you want to probe a Locust.io execution time statistics value, please use the following action in an experiment file:
```json
{
  "method": [
    {
      "type": "probe",
      "name": "avg_latency_should_be_in_tolerance_range",
      "tolerance": {
        "type": "range",
        "range": [0, 10]
      },
      "provider": {
        "type": "python",
        "module": "chaoslocust.probes",
        "func": "get_current_stats",
        "arguments": {
          "metric_name": "current_response_time_percentile_50"
        }
      }
    }
  ]
}
```
## Test

To run the extension unit tests:

```bash
pytest ./tests
```


## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/