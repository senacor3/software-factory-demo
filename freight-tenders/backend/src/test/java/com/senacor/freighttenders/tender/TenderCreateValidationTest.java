package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.hamcrest.Matchers.hasItem;
import static org.junit.jupiter.params.provider.Arguments.arguments;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

/**
 * The validation rules of {@code POST /api/tenders}. "Today" is fixed to 2026-10-13 by {@link
 * FixedClockConfiguration}, so the date rules do not depend on the day the tests run. Request
 * bodies are the valid example with some fragments replaced; fragments use single quotes for
 * readability.
 */
@WebMvcTest(TenderController.class)
@Import(FixedClockConfiguration.class)
class TenderCreateValidationTest {

  private static final String DANGEROUS_GOODS = "'dangerousGoods':false";
  private static final String NOT_TEMPERATURE_CONTROLLED = "'temperatureControlled':false";
  private static final String CURTAIN_SIDER =
      "'equipmentType':'CURTAIN_SIDER'," + DANGEROUS_GOODS + "," + NOT_TEMPERATURE_CONTROLLED;
  private static final String REEFER =
      "'equipmentType':'REEFER'," + DANGEROUS_GOODS + ",'temperatureControlled':true";

  @Autowired private MockMvc mockMvc;

  @MockitoBean private TenderService tenderService;

  @ParameterizedTest
  @MethodSource("boundaryCases")
  void createTenderAtTheBoundaryOfARuleReturns201(String[] replacements) throws Exception {
    given(tenderService.createTender(any(CreateTenderRequest.class)))
        .willReturn(TenderFixtures.tender());

    mockMvc
        .perform(
            post("/api/tenders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(body(replacements)))
        .andExpect(status().isCreated());
  }

  static Stream<Arguments> boundaryCases() {
    return Stream.of(
        // pickup and deadline equal to today, delivery equal to pickup
        accepted(
            "'pickupDate':'2026-10-20'",
            "'pickupDate':'2026-10-13'",
            "'deliveryDate':'2026-10-22'",
            "'deliveryDate':'2026-10-13'",
            "'bidDeadline':'2026-10-16'",
            "'bidDeadline':'2026-10-13'"),
        // deadline equal to pickup
        accepted("'bidDeadline':'2026-10-16'", "'bidDeadline':'2026-10-20'"),
        accepted("'weightKg':18500", "'weightKg':1"),
        accepted("'weightKg':18500", "'weightKg':40000"),
        accepted("'loadingMeters':13.6", "'loadingMeters':0.1"),
        accepted("'palletCount':33", "'palletCount':1"),
        accepted("'palletCount':33", "'palletCount':66"),
        accepted(",'palletCount':33", ""),
        accepted(DANGEROUS_GOODS, "'dangerousGoods':true,'adrClass':'4.1'"),
        accepted(CURTAIN_SIDER, REEFER + ",'temperatureMinC':-30,'temperatureMaxC':-30"),
        accepted(CURTAIN_SIDER, REEFER + ",'temperatureMinC':2,'temperatureMaxC':30"));
  }

  @ParameterizedTest
  @MethodSource("rejectedCases")
  void createTenderViolatingARuleReturns400NamingTheFieldAndSkipsService(
      String[] replacements, String field) throws Exception {
    mockMvc
        .perform(
            post("/api/tenders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(body(replacements)))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").value("Bad Request"))
        .andExpect(jsonPath("$.message").exists())
        .andExpect(jsonPath("$.path").value("/api/tenders"))
        .andExpect(jsonPath("$.timestamp").exists())
        .andExpect(jsonPath("$.violations[*].field").value(hasItem(field)))
        .andExpect(jsonPath("$.violations[0].message").exists());

    verifyNoInteractions(tenderService);
  }

  static Stream<Arguments> rejectedCases() {
    String origin = "'origin':{'country':'DE','postalCode':'20457','city':'Hamburg'},";
    String commodity = "'commodity':'Maschinenteile auf Europaletten'";
    String box = "'equipmentType':'BOX','dangerousGoods':false,'temperatureControlled':true";
    box = box + ",'temperatureMinC':2,'temperatureMaxC':8";
    return Stream.of(
        // addresses, named by their nested path
        rejected("origin.country", "'country':'DE'", "'country':'de'"),
        rejected("origin.country", "'country':'DE'", "'country':'DEU'"),
        rejected("origin.country", "'country':'DE'", "'country':null"),
        rejected("destination.country", "'country':'NL'", "'country':'N1'"),
        rejected("origin.postalCode", "'postalCode':'20457'", "'postalCode':'12345678901'"),
        rejected("origin.postalCode", "'postalCode':'20457'", "'postalCode':''"),
        rejected("destination.postalCode", "'postalCode':'3011 AA'", "'postalCode':null"),
        rejected("origin.city", "'city':'Hamburg'", "'city':'" + "x".repeat(101) + "'"),
        rejected("destination.city", "'city':'Rotterdam'", "'city':''"),
        rejected("origin", origin, ""),
        // dates
        rejected("pickupDate", "'pickupDate':'2026-10-20'", "'pickupDate':'2026-10-12'"),
        rejected("pickupDate", "'pickupDate':'2026-10-20'", "'pickupDate':null"),
        rejected("deliveryDate", "'deliveryDate':'2026-10-22'", "'deliveryDate':'2026-10-19'"),
        rejected("bidDeadline", "'bidDeadline':'2026-10-16'", "'bidDeadline':'2026-10-12'"),
        rejected("bidDeadline", "'bidDeadline':'2026-10-16'", "'bidDeadline':'2026-10-21'"),
        // cargo
        rejected("commodity", commodity, "'commodity':'" + "x".repeat(201) + "'"),
        rejected("commodity", commodity, "'commodity':' '"),
        rejected("weightKg", "'weightKg':18500", "'weightKg':0"),
        rejected("weightKg", "'weightKg':18500", "'weightKg':40001"),
        rejected("loadingMeters", "'loadingMeters':13.6", "'loadingMeters':0.0"),
        rejected("loadingMeters", "'loadingMeters':13.6", "'loadingMeters':13.7"),
        rejected("loadingMeters", "'loadingMeters':13.6", "'loadingMeters':1.25"),
        rejected("palletCount", "'palletCount':33", "'palletCount':0"),
        rejected("palletCount", "'palletCount':33", "'palletCount':67"),
        // dangerous goods
        rejected("adrClass", DANGEROUS_GOODS, "'dangerousGoods':true,'adrClass':'10'"),
        rejected("adrClass", DANGEROUS_GOODS, "'dangerousGoods':true"),
        rejected("adrClass", DANGEROUS_GOODS, DANGEROUS_GOODS + ",'adrClass':'3'"),
        rejected("dangerousGoods", DANGEROUS_GOODS + ",", ""),
        // temperature
        rejected("temperatureMinC", CURTAIN_SIDER, REEFER + ",'temperatureMinC':-31"),
        rejected("temperatureMaxC", CURTAIN_SIDER, REEFER + ",'temperatureMaxC':31"),
        rejected("temperatureMinC", CURTAIN_SIDER, REEFER + ",'temperatureMaxC':5"),
        rejected("temperatureMaxC", CURTAIN_SIDER, REEFER + ",'temperatureMinC':5"),
        rejected(
            "temperatureMinC", CURTAIN_SIDER, REEFER + ",'temperatureMinC':6,'temperatureMaxC':5"),
        rejected(
            "temperatureMaxC", CURTAIN_SIDER, REEFER + ",'temperatureMinC':6,'temperatureMaxC':5"),
        rejected(
            "temperatureMinC",
            NOT_TEMPERATURE_CONTROLLED,
            NOT_TEMPERATURE_CONTROLLED + ",'temperatureMinC':5"),
        rejected(
            "temperatureMaxC",
            NOT_TEMPERATURE_CONTROLLED,
            NOT_TEMPERATURE_CONTROLLED + ",'temperatureMaxC':5"),
        // vehicle
        rejected("equipmentType", CURTAIN_SIDER, box),
        rejected("equipmentType", "'equipmentType':'CURTAIN_SIDER',", ""),
        // flags and currency
        rejected("temperatureControlled", "," + NOT_TEMPERATURE_CONTROLLED, ""),
        rejected("currency", ",'currency':'EUR'", ""));
  }

  @Test
  void createTenderWithEmptyBodyReturns400WithViolationForEachRequiredField() throws Exception {
    mockMvc
        .perform(post("/api/tenders").contentType(MediaType.APPLICATION_JSON).content("{}"))
        .andExpect(status().isBadRequest())
        .andExpect(
            jsonPath("$.violations[*].field")
                .value(
                    containsInAnyOrder(
                        "origin",
                        "destination",
                        "pickupDate",
                        "deliveryDate",
                        "bidDeadline",
                        "commodity",
                        "weightKg",
                        "loadingMeters",
                        "equipmentType",
                        "dangerousGoods",
                        "temperatureControlled",
                        "currency")));

    verifyNoInteractions(tenderService);
  }

  @ParameterizedTest
  @MethodSource("unreadableBodies")
  void createTenderWithUnreadableBodyReturns400InTheStandardShape(String requestBody)
      throws Exception {
    mockMvc
        .perform(post("/api/tenders").contentType(MediaType.APPLICATION_JSON).content(requestBody))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").value("Bad Request"))
        .andExpect(jsonPath("$.message").exists())
        .andExpect(jsonPath("$.path").value("/api/tenders"))
        .andExpect(jsonPath("$.timestamp").exists())
        .andExpect(jsonPath("$.violations").isEmpty());

    verifyNoInteractions(tenderService);
  }

  static Stream<String> unreadableBodies() {
    return Stream.of(
        body("'equipmentType':'CURTAIN_SIDER'", "'equipmentType':'SPACESHIP'"),
        body("'currency':'EUR'", "'currency':'XXX'"),
        body("'pickupDate':'2026-10-20'", "'pickupDate':'20.10.2026'"),
        body("'pickupDate':'2026-10-20'", "'pickupDate':'2026-13-45'"),
        body("'weightKg':18500", "'weightKg':'heavy'"),
        "{\"origin\":");
  }

  private static Arguments accepted(String... replacements) {
    return arguments((Object) replacements);
  }

  private static Arguments rejected(String field, String from, String to) {
    return arguments(new String[] {from, to}, field);
  }

  /** The valid request body with each {@code from, to} pair of {@code replacements} applied. */
  private static String body(String... replacements) {
    String result = TenderFixtures.VALID_REQUEST_JSON;
    for (int i = 0; i < replacements.length; i += 2) {
      String from = replacements[i].replace('\'', '"');
      assertThat(result).contains(from);
      result = result.replace(from, replacements[i + 1].replace('\'', '"'));
    }
    return result;
  }
}
