package com.senacor.freighttenders.tender;

import java.math.BigDecimal;
import java.time.LocalDate;

/** Shared test data: a complete, valid tender and the JSON request body that creates it. */
final class TenderFixtures {

  /** A valid request body, the example from the tender story. */
  static final String VALID_REQUEST_JSON =
      "{\"origin\":{\"country\":\"DE\",\"postalCode\":\"20457\",\"city\":\"Hamburg\"},"
          + "\"destination\":{\"country\":\"NL\",\"postalCode\":\"3011 AA\",\"city\":\"Rotterdam\"},"
          + "\"pickupDate\":\"2026-10-20\",\"deliveryDate\":\"2026-10-22\","
          + "\"bidDeadline\":\"2026-10-16\","
          + "\"commodity\":\"Maschinenteile auf Europaletten\",\"weightKg\":18500,"
          + "\"loadingMeters\":13.6,\"palletCount\":33,\"equipmentType\":\"CURTAIN_SIDER\","
          + "\"dangerousGoods\":false,\"temperatureControlled\":false,\"currency\":\"EUR\"}";

  private TenderFixtures() {}

  static Tender tender() {
    return tender("Hamburg", "Rotterdam");
  }

  static Tender tender(String originCity, String destinationCity) {
    return new Tender(
        new Address("DE", "20457", originCity),
        new Address("NL", "3011 AA", destinationCity),
        LocalDate.of(2026, 10, 20),
        LocalDate.of(2026, 10, 22),
        LocalDate.of(2026, 10, 16),
        "Maschinenteile auf Europaletten",
        18500,
        new BigDecimal("13.6"),
        33,
        EquipmentType.CURTAIN_SIDER,
        false,
        null,
        false,
        null,
        null,
        Currency.EUR);
  }

  /** A request equal to {@link #VALID_REQUEST_JSON}, for service-level tests. */
  static CreateTenderRequest request() {
    return new CreateTenderRequest(
        new CreateTenderRequest.AddressRequest("DE", "20457", "Hamburg"),
        new CreateTenderRequest.AddressRequest("NL", "3011 AA", "Rotterdam"),
        LocalDate.of(2026, 10, 20),
        LocalDate.of(2026, 10, 22),
        LocalDate.of(2026, 10, 16),
        "Maschinenteile auf Europaletten",
        18500,
        new BigDecimal("13.6"),
        33,
        EquipmentType.CURTAIN_SIDER,
        false,
        null,
        false,
        null,
        null,
        Currency.EUR);
  }
}
