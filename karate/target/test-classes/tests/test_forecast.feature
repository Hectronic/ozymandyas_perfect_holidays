# tests/test_forecast.feature
Feature: 5-day / 3-hour Forecast API tests

  Background:
    * url 'https://api.openweathermap.org/data/2.5/forecast'
    * header Accept = 'application/json'
    * def apiKey = karate.env == 'ci' ? karate.properties['OPENWEATHER_API_KEY'] : '4b66cf4f354cd07b407c07800dc8c2f9'

  Scenario Outline: Valid 5-day/3-hour forecast for coordinates <lat>,<lon>
    Given param lat    = '<lat>'
    And   param lon    = '<lon>'
    And   param appid  = apiKey
    And   param units  = 'metric'
    When  method GET
    Then  status 200

    # assert we got an array and it has at least one entry
    *   assert response.list.length > 0

    # spot‐check the first element
    And   match response.list[0].dt         == '#number'
    And   match response.list[0].main.temp  == '#number'

  Examples:
    | lat     | lon      |
    | 40.4168 | -3.7038  |
    | 51.5074 | -0.1278  |
    | 40.7128 | -74.0060 |

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

  Scenario: Forecast in imperial units returns numeric temp
    Given param lat   = '40.4168'
    And   param lon   = '-3.7038'
    And   param appid = apiKey
    And   param units = 'imperial'
    When  method GET
    Then  status 200
    And   match response.list[0].main.temp == '#number'

  Scenario: Forecast with Spanish lang returns non-empty description
    Given param lat   = '40.4168'
    And   param lon   = '-3.7038'
    And   param appid = apiKey
    And   param units = 'metric'
    And   param lang  = 'es'
    When  method GET
    Then  status 200
    And   match response.list[0].weather[0].description == '#string'
