package com.senacor.freighttenders.tender;

import java.time.Clock;
import java.time.ZoneId;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Provides the {@link Clock} the tender date rules read "today" from. */
@Configuration
public class ClockConfiguration {

  /** The zone "today" is evaluated in, so it does not depend on where the server runs. */
  static final ZoneId TENDER_ZONE = ZoneId.of("Europe/Berlin");

  @Bean
  public Clock clock() {
    return Clock.system(TENDER_ZONE);
  }
}
