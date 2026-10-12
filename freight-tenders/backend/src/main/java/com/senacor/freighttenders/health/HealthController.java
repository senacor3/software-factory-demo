package com.senacor.freighttenders.health;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Plain liveness endpoint -- deliberately not Spring Boot Actuator's {@code /actuator/health},
 * which would bring broader disk/db checks this app does not need.
 */
@RestController
public class HealthController {

  @GetMapping("/api/health")
  public Map<String, String> health() {
    return Map.of("status", "UP");
  }
}
