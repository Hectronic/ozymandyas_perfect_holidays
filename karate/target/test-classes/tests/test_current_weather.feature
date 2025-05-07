# tests/test_current_weather.feature
Feature: Current Weather API tests

  Background:
    * url 'https://api.openweathermap.org/data/2.5/weather'
    * header Accept = 'application/json'
    * def apiKey = karate.env == 'ci' ? karate.properties['OPENWEATHER_API_KEY'] : '4b66cf4f354cd07b407c07800dc8c2f9'

  Scenario Outline: Valid current weather for coordinates <lat>,<lon>
    Given param lat    = '<lat>'
    And   param lon    = '<lon>'
    And   param appid  = apiKey
    And   param units  = 'metric'
    When  method GET
    Then  status 200

    # allow extra fields but verify key properties
    And   match response contains { coord: { lat: '#number', lon: '#number' }, name: '#string', cod: '#number' }
    And   match response.main contains { temp: '#number', pressure: '#number', humidity: '#number' }
    And   match response.weather[0] contains { id: '#number', main: '#string', description: '#string' }

  Examples:
    | lat     | lon      |
    | 40.4168 | -3.7038  |
    | 51.5074 | -0.1278  |
    | 40.7128 | -74.0060 |

  Scenario: Missing API key returns 401
    Given param lat   = '40.4168'
    And   param lon   = '-3.7038'
    When  method GET
    Then  status 401

  Scenario: Missing latitude returns 400
    Given param lon   = '-3.7038'
    And   param appid = apiKey
    When  method GET
    Then  status 400

  Scenario: Missing longitude returns 400
    Given param lat   = '40.4168'
    And   param appid = apiKey
    When  method GET
    Then  status 400
