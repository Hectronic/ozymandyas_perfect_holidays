import pytest
import requests
import time
import json
from jsonschema import validate, ValidationError

# Test coordinates
COORDS = [
    (40.4168, -3.7038),   # Madrid
    (51.5074, -0.1278),    # London
    (40.7128, -74.0060),   # New York
]

def load_schema(path):
    """Helper function to load a JSON schema from a file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.parametrize("lat,lon", COORDS)
def test_5day_3h_forecast_by_coords(lat, lon, api_key, forecast_url, request_headers):
    """
    Tests the 5-day/3-hour forecast API by coordinates.
    Checks for:
    - HTTP 200 OK status.
    - Response time.
    - Correct JSON content type.
    - JSON schema validation.
    - Presence of essential fields in the forecast data.
    """
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    start_time = time.time()
    response = requests.get(forecast_url, headers=request_headers, params=params, timeout=5)
    elapsed_time = time.time() - start_time

    # Status and performance checks
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert elapsed_time < 2, f"Excessive response time: {elapsed_time:.2f}s"
    assert response.headers["Content-Type"].startswith("application/json"), \
        f"Unexpected Content-Type: {response.headers['Content-Type']}"

    data = response.json()

    # JSON schema validation
    schema = load_schema("tests/schemas/forecast_schema.json") # Ensure this path is correct
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Forecast JSON does not conform to schema: {e.message}")

    # Additional structural checks
    assert "list" in data and isinstance(data["list"], list) and data["list"], \
        "Forecast list is missing, not a list, or empty."
    
    first_forecast = data["list"][0]
    for field in ("dt", "main", "weather"):
        assert field in first_forecast, f"Missing required field in forecast item: {field}"
    assert "temp" in first_forecast["main"], "Missing 'temp' in 'main' part of forecast item."

def test_forecast_missing_params(forecast_url, api_key, request_headers):
    """
    Tests that the forecast API returns a 400 Bad Request if 'lat' or 'lon' parameters are missing.
    """
    # Test case 1: Missing 'lon'
    params_missing_lon = {"lat": 40.0, "appid": api_key}
    response1 = requests.get(
        forecast_url,
        headers=request_headers,
        params=params_missing_lon,
        timeout=5
    )
    assert response1.status_code == 400, \
        f"Expected status 400 when 'lon' is missing, got {response1.status_code}"

    # Test case 2: Missing 'lat'
    params_missing_lat = {"lon": -3.0, "appid": api_key}
    response2 = requests.get(
        forecast_url,
        headers=request_headers,
        params=params_missing_lat,
        timeout=5
    )
    assert response2.status_code == 400, \
        f"Expected status 400 when 'lat' is missing, got {response2.status_code}"

@pytest.mark.parametrize("units,lang", [
    ("imperial", None), # Test with imperial units, default language
    ("metric", "es"),   # Test with metric units, Spanish language
])
def test_forecast_units_and_lang(units, lang, api_key, forecast_url, request_headers):
    """
    Tests the 'units' and 'lang' (internationalization) parameters for the Forecast API.
    """
    # Use the first coordinate for this test
    lat, lon = COORDS[0]
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units}
    if lang:
        params["lang"] = lang

    response = requests.get(forecast_url, headers=request_headers, params=params, timeout=5)
    assert response.status_code == 200, \
        f"Unexpected status code for units={units}, lang={lang}: {response.status_code}"
    
    data = response.json()
    assert "list" in data and data["list"], "Forecast list is missing or empty."
    first_forecast = data["list"][0]

    # Check temperature
    temperature = first_forecast["main"]["temp"]
    assert isinstance(temperature, (int, float)), \
        f"Temperature should be a number, got {type(temperature)} for units={units}"

    # Check weather description 
    description = first_forecast["weather"][0]["description"]
    assert isinstance(description, str) and description, \
        f"Weather description should be a non-empty string, got '{description}' for lang={lang}"
    
