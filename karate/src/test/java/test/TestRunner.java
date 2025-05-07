// src/test/java/test/TestRunner.java
package test;

import com.intuit.karate.junit5.Karate;

public class TestRunner {

  @Karate.Test
  public Karate testAll() {
    return Karate.run(
      "classpath:tests/test_current_weather.feature",
      "classpath:tests/test_forecast.feature"
    );
  }

}
