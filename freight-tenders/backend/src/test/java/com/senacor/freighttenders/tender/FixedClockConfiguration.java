package com.senacor.freighttenders.tender;

import java.time.Clock;
import java.time.Instant;
import java.time.ZoneId;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;

/**
 * Pins "today" to 2026-10-13 (Europe/Berlin) for web-slice tests, so the tender date rules do not
 * depend on the day the tests run. Test slices do not pick up {@link ClockConfiguration}.
 */
@TestConfiguration
class FixedClockConfiguration {

  @Bean
  Clock clock() {
    return Clock.fixed(Instant.parse("2026-10-13T08:00:00Z"), ZoneId.of("Europe/Berlin"));
  }
}
