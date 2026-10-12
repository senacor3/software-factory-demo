package com.senacor.freighttenders.health;

import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Plain health endpoint for the scaffold's trivial end-to-end path -- deliberately not Spring Boot
 * Actuator's {@code /actuator/health}, which would bring broader disk/db checks that don't apply
 * yet to this tracer bullet.
 */
@RestController
public class HealthController {

  @GetMapping("/api/health")
  public Map<String, String> health() {
    return Map.of("status", "UP");
  }
}
