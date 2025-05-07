# OpenWeatherMap API Test Suite

## Overview
This project contains automated tests for the **OpenWeatherMap Free Plan** endpoints:

- **Current Weather Data** (`/data/2.5/weather`)  
- **5-day / 3-hour Forecast** (`/data/2.5/forecast`)

Tests are written in **Python** using `pytest`, `requests` and `jsonschema` to verify status codes, JSON schemas, required fields and basic performance.

## Project Structure
```
.
├── conftest.py
├── Dockerfile
├── requirements.txt
├── run_tests.sh        # local test runner
├── run_docker.sh       # build & run in Docker
└── tests
    ├── schemas
    │   ├── current_weather_schema.json
    │   └── forecast_schema.json
    ├── test_current_weather.py
    └── test_forecast.py
```

## Prerequisites
- **Python 3.8+**  
- **bash** (for the scripts)  
- **Docker** (if using the container)

## Local Execution
Run the included script to create a virtual environment, install dependencies and execute all tests:

```bash
chmod +x run_tests.sh
./run_tests.sh
```

## Docker Execution
Build a Docker image and run the tests inside a container:

```bash
chmod +x run_docker.sh
./run_docker.sh
```

This will use a `python:3.12-slim` container, install requirements and run `pytest -q`.

