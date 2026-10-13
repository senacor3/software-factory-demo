package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(TenderController.class)
@Import(FixedClockConfiguration.class)
class TenderControllerTest {

  @Autowired private MockMvc mockMvc;

  @MockitoBean private TenderService tenderService;

  @Test
  void createTenderReturns201WithOpenTenderAndEveryField() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    given(tenderService.createTender(any(CreateTenderRequest.class))).willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_REQUEST_JSON))
        .andExpect(status().isCreated())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.origin.country").value("DE"))
        .andExpect(jsonPath("$.origin.postalCode").value("20457"))
        .andExpect(jsonPath("$.origin.city").value("Hamburg"))
        .andExpect(jsonPath("$.destination.country").value("NL"))
        .andExpect(jsonPath("$.destination.postalCode").value("3011 AA"))
        .andExpect(jsonPath("$.destination.city").value("Rotterdam"))
        .andExpect(jsonPath("$.pickupDate").value("2026-10-20"))
        .andExpect(jsonPath("$.deliveryDate").value("2026-10-22"))
        .andExpect(jsonPath("$.bidDeadline").value("2026-10-16"))
        .andExpect(jsonPath("$.commodity").value("Maschinenteile auf Europaletten"))
        .andExpect(jsonPath("$.weightKg").value(18500))
        .andExpect(jsonPath("$.loadingMeters").value(13.6))
        .andExpect(jsonPath("$.palletCount").value(33))
        .andExpect(jsonPath("$.equipmentType").value("CURTAIN_SIDER"))
        .andExpect(jsonPath("$.dangerousGoods").value(false))
        .andExpect(jsonPath("$.temperatureControlled").value(false))
        .andExpect(jsonPath("$.currency").value("EUR"))
        .andExpect(jsonPath("$.status").value("OPEN"));

    ArgumentCaptor<CreateTenderRequest> captor = ArgumentCaptor.forClass(CreateTenderRequest.class);
    verify(tenderService).createTender(captor.capture());
    assertThat(captor.getValue()).isEqualTo(TenderFixtures.request());
  }

  @Test
  void notFoundResponseOmitsViolations() throws Exception {
    given(tenderService.getTender(99L)).willThrow(new TenderNotFoundException(99L));

    mockMvc
        .perform(get("/api/tenders/{id}", 99L))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.violations").doesNotExist());
  }

  @Test
  void conflictResponseOmitsViolations() throws Exception {
    given(tenderService.addRemark(eq(1L), eq("Too late"))).willThrow(new TenderClosedException(1L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/remarks", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"text\":\"Too late\"}"))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.violations").doesNotExist());
  }

  @Test
  void closeTenderReturns200WithClosedTender() throws Exception {
    Tender tender = TenderFixtures.tender();
    tender.close();
    given(tenderService.closeTender(1L)).willReturn(tender);

    mockMvc
        .perform(post("/api/tenders/{id}/close", 1L))
        .andExpect(status().isOk())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.status").value("CLOSED"))
        .andExpect(jsonPath("$.origin.city").value("Hamburg"));
  }

  @Test
  void listTendersFilteredByStatusReturnsOnlyOpenTenders() throws Exception {
    Tender openTender = TenderFixtures.tender();
    ReflectionTestUtils.setField(openTender, "id", 1L);
    given(tenderService.listTenders(Optional.of(TenderStatus.OPEN)))
        .willReturn(List.of(openTender));

    mockMvc
        .perform(get("/api/tenders").param("status", "OPEN"))
        .andExpect(status().isOk())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.length()").value(1))
        .andExpect(jsonPath("$[0].id").value(1))
        .andExpect(jsonPath("$[0].status").value("OPEN"));
  }

  @Test
  void listTendersWithNoFilterReturnsOpenAndClosedTendersWithEveryField() throws Exception {
    Tender openTender = TenderFixtures.tender();
    ReflectionTestUtils.setField(openTender, "id", 1L);
    Tender closedTender = TenderFixtures.tender("Berlin", "Munich");
    ReflectionTestUtils.setField(closedTender, "id", 2L);
    closedTender.close();
    given(tenderService.listTenders(Optional.empty()))
        .willReturn(List.of(openTender, closedTender));

    mockMvc
        .perform(get("/api/tenders"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.length()").value(2))
        .andExpect(jsonPath("$[0].status").value("OPEN"))
        .andExpect(jsonPath("$[0].origin.city").value("Hamburg"))
        .andExpect(jsonPath("$[0].destination.city").value("Rotterdam"))
        .andExpect(jsonPath("$[0].pickupDate").value("2026-10-20"))
        .andExpect(jsonPath("$[0].weightKg").value(18500))
        .andExpect(jsonPath("$[0].currency").value("EUR"))
        .andExpect(jsonPath("$[1].status").value("CLOSED"))
        .andExpect(jsonPath("$[1].origin.city").value("Berlin"));
  }

  @Test
  void getTenderReturns200WithNestedRemarksAndOffers() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    Remark remark = new Remark("Please expedite");
    ReflectionTestUtils.setField(remark, "id", 10L);
    tender.addRemark(remark);
    Offer offer = new Offer("Acme Logistics", new BigDecimal("1234.56"));
    ReflectionTestUtils.setField(offer, "id", 20L);
    tender.addOffer(offer);
    given(tenderService.getTender(1L)).willReturn(tender);

    mockMvc
        .perform(get("/api/tenders/{id}", 1L))
        .andExpect(status().isOk())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.origin.city").value("Hamburg"))
        .andExpect(jsonPath("$.destination.city").value("Rotterdam"))
        .andExpect(jsonPath("$.pickupDate").value("2026-10-20"))
        .andExpect(jsonPath("$.deliveryDate").value("2026-10-22"))
        .andExpect(jsonPath("$.bidDeadline").value("2026-10-16"))
        .andExpect(jsonPath("$.equipmentType").value("CURTAIN_SIDER"))
        .andExpect(jsonPath("$.currency").value("EUR"))
        .andExpect(jsonPath("$.remarks[0].text").value("Please expedite"))
        .andExpect(jsonPath("$.offers[0].supplierName").value("Acme Logistics"));
  }

  @Test
  void addRemarkOnOpenTenderReturns201WithCreatedRemark() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    Remark remark = new Remark("Please expedite");
    ReflectionTestUtils.setField(remark, "id", 10L);
    tender.addRemark(remark);
    given(tenderService.addRemark(eq(1L), eq("Please expedite"))).willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders/{id}/remarks", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"text\":\"Please expedite\"}"))
        .andExpect(status().isCreated())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id").value(10))
        .andExpect(jsonPath("$.text").value("Please expedite"));
  }

  @Test
  void addOfferOnOpenTenderReturns201WithCreatedOffer() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    Offer offer = new Offer("Acme Logistics", new BigDecimal("1234.56"));
    ReflectionTestUtils.setField(offer, "id", 20L);
    tender.addOffer(offer);
    given(tenderService.addOffer(eq(1L), eq("Acme Logistics"), eq(new BigDecimal("1234.56"))))
        .willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"supplierName\":\"Acme Logistics\",\"amount\":1234.56}"))
        .andExpect(status().isCreated())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id").value(20))
        .andExpect(jsonPath("$.supplierName").value("Acme Logistics"));
  }

  @Test
  void addRemarkOnClosedTenderReturns409NamingTheClosedTender() throws Exception {
    given(tenderService.addRemark(eq(1L), eq("Too late"))).willThrow(new TenderClosedException(1L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/remarks", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"text\":\"Too late\"}"))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.error").value("Conflict"))
        .andExpect(jsonPath("$.message").value("Tender 1 is closed and can no longer be modified"))
        .andExpect(jsonPath("$.path").value("/api/tenders/1/remarks"))
        .andExpect(jsonPath("$.timestamp").exists());
  }

  @Test
  void addOfferOnClosedTenderReturns409NamingTheClosedTender() throws Exception {
    given(tenderService.addOffer(eq(1L), eq("Acme Logistics"), eq(new BigDecimal("1234.56"))))
        .willThrow(new TenderClosedException(1L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"supplierName\":\"Acme Logistics\",\"amount\":1234.56}"))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.error").value("Conflict"))
        .andExpect(jsonPath("$.message").value("Tender 1 is closed and can no longer be modified"))
        .andExpect(jsonPath("$.path").value("/api/tenders/1/offers"))
        .andExpect(jsonPath("$.timestamp").exists());
  }

  @Test
  void getTenderForUnknownIdReturns404NamingTheMissingId() throws Exception {
    given(tenderService.getTender(99L)).willThrow(new TenderNotFoundException(99L));

    mockMvc
        .perform(get("/api/tenders/{id}", 99L))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Not Found"))
        .andExpect(jsonPath("$.message").value("No tender found with id 99"))
        .andExpect(jsonPath("$.path").value("/api/tenders/99"))
        .andExpect(jsonPath("$.timestamp").exists());
  }

  @Test
  void addRemarkForUnknownIdReturns404NamingTheMissingId() throws Exception {
    given(tenderService.addRemark(eq(99L), eq("Please expedite")))
        .willThrow(new TenderNotFoundException(99L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/remarks", 99L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"text\":\"Please expedite\"}"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Not Found"))
        .andExpect(jsonPath("$.message").value("No tender found with id 99"))
        .andExpect(jsonPath("$.path").value("/api/tenders/99/remarks"))
        .andExpect(jsonPath("$.timestamp").exists());
  }

  @Test
  void addOfferForUnknownIdReturns404NamingTheMissingId() throws Exception {
    given(tenderService.addOffer(eq(99L), eq("Acme Logistics"), eq(new BigDecimal("1234.56"))))
        .willThrow(new TenderNotFoundException(99L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 99L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"supplierName\":\"Acme Logistics\",\"amount\":1234.56}"))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Not Found"))
        .andExpect(jsonPath("$.message").value("No tender found with id 99"))
        .andExpect(jsonPath("$.path").value("/api/tenders/99/offers"))
        .andExpect(jsonPath("$.timestamp").exists());
  }

  @Test
  void addRemarkWithBlankWhitespaceOrMissingTextReturns400WithViolation() throws Exception {
    for (String body : List.of("{\"text\":\"\"}", "{\"text\":\"   \"}", "{}")) {
      mockMvc
          .perform(
              post("/api/tenders/{id}/remarks", 1L)
                  .contentType(MediaType.APPLICATION_JSON)
                  .content(body))
          .andExpect(status().isBadRequest())
          .andExpect(jsonPath("$.error").value("Bad Request"))
          .andExpect(jsonPath("$.message").exists())
          .andExpect(jsonPath("$.path").value("/api/tenders/1/remarks"))
          .andExpect(jsonPath("$.timestamp").exists())
          .andExpect(jsonPath("$.violations.length()").value(1))
          .andExpect(jsonPath("$.violations[0].field").value("text"));
    }

    verifyNoInteractions(tenderService);
  }

  @Test
  void addOfferWithBlankSupplierNameReturns400WithViolation() throws Exception {
    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"supplierName\":\"  \",\"amount\":10.00}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.violations.length()").value(1))
        .andExpect(jsonPath("$.violations[0].field").value("supplierName"));

    verifyNoInteractions(tenderService);
  }

  @Test
  void addOfferWithMissingZeroOrNegativeAmountReturns400WithViolation() throws Exception {
    for (String amountJson : List.of("", ",\"amount\":0", ",\"amount\":-5", ",\"amount\":0.00")) {
      mockMvc
          .perform(
              post("/api/tenders/{id}/offers", 1L)
                  .contentType(MediaType.APPLICATION_JSON)
                  .content("{\"supplierName\":\"Acme Logistics\"" + amountJson + "}"))
          .andExpect(status().isBadRequest())
          .andExpect(jsonPath("$.violations.length()").value(1))
          .andExpect(jsonPath("$.violations[0].field").value("amount"));
    }

    verifyNoInteractions(tenderService);
  }

  @Test
  void addOfferWithEmptyBodyReturns400WithViolationForEachField() throws Exception {
    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.violations.length()").value(2))
        .andExpect(
            jsonPath("$.violations[*].field").value(containsInAnyOrder("supplierName", "amount")));

    verifyNoInteractions(tenderService);
  }

  @Test
  void addOfferWithMinimumAmountReturns201() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    Offer offer = new Offer("Acme Logistics", new BigDecimal("0.01"));
    ReflectionTestUtils.setField(offer, "id", 20L);
    tender.addOffer(offer);
    given(tenderService.addOffer(eq(1L), eq("Acme Logistics"), eq(new BigDecimal("0.01"))))
        .willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"supplierName\":\"Acme Logistics\",\"amount\":0.01}"))
        .andExpect(status().isCreated());
  }

  @Test
  void invalidRemarkOrOfferOnClosedTenderReturns400NotConflict() throws Exception {
    given(tenderService.addRemark(eq(1L), eq(""))).willThrow(new TenderClosedException(1L));
    given(tenderService.addOffer(eq(1L), eq(""), eq(BigDecimal.ZERO)))
        .willThrow(new TenderClosedException(1L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/remarks", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"text\":\"\"}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.violations").exists());
    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"supplierName\":\"\",\"amount\":0}"))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.violations").exists());

    verifyNoInteractions(tenderService);
  }
}
