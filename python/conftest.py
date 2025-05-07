import os
import pytest
import requests

@pytest.fixture(scope="session")
def api_key():
    key = "4b66cf4f354cd07b407c07800dc8c2f9"
    if not key:
        pytest.skip("No OPENWEATHER_API_KEY definido en variables de entorno")
    return key

@pytest.fixture
def base_url():
    return "https://api.openweathermap.org/data/2.5/weather"

@pytest.fixture
def forecast_url():
    return "https://api.openweathermap.org/data/2.5/forecast"

@pytest.fixture
def request_headers():
    return {
        "Accept": "application/json"
    }
