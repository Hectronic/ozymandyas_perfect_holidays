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
def test_current_weather_by_coords(lat, lon, api_key, base_url, request_headers):
    """
    Tests the Current Weather API by coordinates.
    Checks for:
    - HTTP 200 OK status.
    - Response time.
    - Correct JSON content type.
    - JSON schema validation.
    - Presence of essential fields (coord, weather, main, name, cod) and their types.
    """
    params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}
    start_time = time.time()
    response = requests.get(base_url, headers=request_headers, params=params, timeout=5)
    elapsed_time = time.time() - start_time

    # Status and performance checks
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert elapsed_time < 2, f"Excessive response time: {elapsed_time:.2f}s"
    assert response.headers["Content-Type"].startswith("application/json"), \
        f"Unexpected Content-Type: {response.headers['Content-Type']}"

    data = response.json()

    # JSON schema validation
    schema = load_schema("tests/schemas/current_weather_schema.json")
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Current Weather JSON does not conform to schema: {e.message}")

    # Additional mandatory fields checks
    for field in ("coord", "weather", "main", "name", "cod"):
        assert field in data, f"Missing mandatory field: {field}"
    
    assert "coord" in data and isinstance(data["coord"].get("lat"), float), \
        "Field 'coord.lat' is missing or not a float."
    assert "coord" in data and isinstance(data["coord"].get("lon"), float), \
        "Field 'coord.lon' is missing or not a float."
    assert "main" in data and isinstance(data["main"].get("temp"), (int, float)), \
        "Field 'main.temp' is missing or not a number (int/float)."

def test_current_weather_invalid_key(base_url, request_headers):
    """
    Tests that the Current Weather API returns a 401 Unauthorized status
    when the API key is missing or invalid (implicitly tested by not providing one).
    """
    # Parameters without 'appid' (API key)
    params_without_key = {"lat": 40.0, "lon": -3.0} # Using Madrid's coordinates as an example
    
    response = requests.get(base_url, headers=request_headers, params=params_without_key, timeout=5)
    
    assert response.status_code == 401, \
        f"Expected status 401 Unauthorized when API key is missing, but got {response.status_code}."