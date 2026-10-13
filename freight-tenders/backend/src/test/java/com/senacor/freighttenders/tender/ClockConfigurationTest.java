package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.ZoneId;
import org.junit.jupiter.api.Test;

class ClockConfigurationTest {

  @Test
  void productionClockIsFixedToTheEuropeBerlinZone() {
    assertThat(new ClockConfiguration().clock().getZone()).isEqualTo(ZoneId.of("Europe/Berlin"));
  }
}
