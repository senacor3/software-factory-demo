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
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
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
  void awardTenderReturns200WithAwardedOfferId() throws Exception {
    Tender tender = TenderFixtures.tender();
    Offer offer = TenderFixtures.offer("Acme", new BigDecimal("100.00"));
    ReflectionTestUtils.setField(offer, "id", 10L);
    tender.addOffer(offer);
    tender.award(offer);
    given(tenderService.awardTender(1L, 10L)).willReturn(tender);

    mockMvc
        .perform(post("/api/tenders/{id}/offers/{offerId}/award", 1L, 10L))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.status").value("AWARDED"))
        .andExpect(jsonPath("$.awardedOfferId").value(10));
  }

  @Test
  void awardTenderMapsNotFoundAndConflictToErrorShape() throws Exception {
    given(tenderService.awardTender(99L, 10L)).willThrow(new TenderNotFoundException(99L));
    given(tenderService.awardTender(1L, 99L)).willThrow(new OfferNotFoundException(1L, 99L));
    given(tenderService.awardTender(2L, 10L)).willThrow(new TenderClosedException(2L));
    given(tenderService.awardTender(3L, 10L)).willThrow(new OfferExpiredException(10L));

    mockMvc
        .perform(post("/api/tenders/{id}/offers/{offerId}/award", 99L, 10L))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.error").value("Not Found"))
        .andExpect(jsonPath("$.violations").doesNotExist());
    mockMvc
        .perform(post("/api/tenders/{id}/offers/{offerId}/award", 1L, 99L))
        .andExpect(status().isNotFound())
        .andExpect(jsonPath("$.path").value("/api/tenders/1/offers/99/award"));
    mockMvc
        .perform(post("/api/tenders/{id}/offers/{offerId}/award", 2L, 10L))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.error").value("Conflict"));
    mockMvc
        .perform(post("/api/tenders/{id}/offers/{offerId}/award", 3L, 10L))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.message").exists());
  }

  @Test
  void listTendersFilteredByAwardedCarriesAwardedSupplierAndAmount() throws Exception {
    Tender awarded = TenderFixtures.tender();
    Offer offer = TenderFixtures.offer("Acme", new BigDecimal("100.00"));
    awarded.addOffer(offer);
    awarded.award(offer);
    Tender open = TenderFixtures.tender("Berlin", "Munich");
    given(tenderService.listTenders(Optional.of(TenderStatus.AWARDED)))
        .willReturn(List.of(awarded));
    given(tenderService.listTenders(Optional.empty())).willReturn(List.of(awarded, open));

    mockMvc
        .perform(get("/api/tenders").param("status", "AWARDED"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].status").value("AWARDED"))
        .andExpect(jsonPath("$[0].awardedSupplierName").value("Acme"))
        .andExpect(jsonPath("$[0].awardedAmount").value(100.00));
    mockMvc
        .perform(get("/api/tenders"))
        .andExpect(jsonPath("$[1].awardedSupplierName").doesNotExist())
        .andExpect(jsonPath("$[1].awardedAmount").doesNotExist());
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
  void listTendersReturnsOfferCountAndLowestOfferAmountPerTender() throws Exception {
    Tender withOffers = TenderFixtures.tender();
    ReflectionTestUtils.setField(withOffers, "id", 1L);
    withOffers.addOffer(TenderFixtures.offer("Acme Logistics", new BigDecimal("1450.00")));
    withOffers.addOffer(TenderFixtures.offer("Spedition Muster", new BigDecimal("1200.50")));
    withOffers.addOffer(TenderFixtures.offer("Nord Transport", new BigDecimal("1300.00")));
    Tender withoutOffers = TenderFixtures.tender("Berlin", "Munich");
    ReflectionTestUtils.setField(withoutOffers, "id", 2L);
    given(tenderService.listTenders(Optional.empty()))
        .willReturn(List.of(withOffers, withoutOffers));

    mockMvc
        .perform(get("/api/tenders"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$[0].offerCount").value(3))
        .andExpect(jsonPath("$[0].lowestOfferAmount").value(1200.50))
        .andExpect(jsonPath("$[1].offerCount").value(0))
        .andExpect(jsonPath("$[1].lowestOfferAmount").value(org.hamcrest.Matchers.nullValue()));
  }

  @Test
  void createAndCloseResponsesCarryOfferCountAndLowestOfferAmount() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    given(tenderService.createTender(any(CreateTenderRequest.class))).willReturn(tender);
    Tender closed = TenderFixtures.tender();
    ReflectionTestUtils.setField(closed, "id", 2L);
    closed.addOffer(TenderFixtures.offer("Acme Logistics", new BigDecimal("990.00")));
    closed.close();
    given(tenderService.closeTender(2L)).willReturn(closed);

    mockMvc
        .perform(
            post("/api/tenders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_REQUEST_JSON))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.offerCount").value(0))
        .andExpect(jsonPath("$.lowestOfferAmount").value(org.hamcrest.Matchers.nullValue()));

    mockMvc
        .perform(post("/api/tenders/2/close"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.offerCount").value(1))
        .andExpect(jsonPath("$.lowestOfferAmount").value(990.00));
  }

  @Test
  void getTenderReturns200WithNestedRemarksAndOffers() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    Remark remark = new Remark("Please expedite");
    ReflectionTestUtils.setField(remark, "id", 10L);
    tender.addRemark(remark);
    Offer offer = TenderFixtures.offer("Acme Logistics", new BigDecimal("1234.56"));
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
    Offer offer = TenderFixtures.offer("Acme Logistics", new BigDecimal("1234.56"));
    ReflectionTestUtils.setField(offer, "id", 20L);
    tender.addOffer(offer);
    given(
            tenderService.addOffer(
                eq(1L), eq("Acme Logistics"), eq(new BigDecimal("1234.56")), any(), any(), any()))
        .willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"supplierName\":\"Acme Logistics\",\"amount\":1234.56,\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-30\"}"))
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
    given(
            tenderService.addOffer(
                eq(1L), eq("Acme Logistics"), eq(new BigDecimal("1234.56")), any(), any(), any()))
        .willThrow(new TenderClosedException(1L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"supplierName\":\"Acme Logistics\",\"amount\":1234.56,\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-30\"}"))
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
    given(
            tenderService.addOffer(
                eq(99L), eq("Acme Logistics"), eq(new BigDecimal("1234.56")), any(), any(), any()))
        .willThrow(new TenderNotFoundException(99L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 99L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"supplierName\":\"Acme Logistics\",\"amount\":1234.56,\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-30\"}"))
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
                .content(
                    "{\"supplierName\":\"  \",\"amount\":10.00,\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-30\"}"))
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
                  .content(
                      "{\"supplierName\":\"Acme Logistics\""
                          + amountJson
                          + ",\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-30\"}"))
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
        .andExpect(jsonPath("$.violations.length()").value(4))
        .andExpect(
            jsonPath("$.violations[*].field")
                .value(containsInAnyOrder("supplierName", "amount", "deliveryDate", "validUntil")));

    verifyNoInteractions(tenderService);
  }

  @Test
  void addOfferWithMinimumAmountReturns201() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    Offer offer = TenderFixtures.offer("Acme Logistics", new BigDecimal("0.01"));
    ReflectionTestUtils.setField(offer, "id", 20L);
    tender.addOffer(offer);
    given(
            tenderService.addOffer(
                eq(1L), eq("Acme Logistics"), eq(new BigDecimal("0.01")), any(), any(), any()))
        .willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"supplierName\":\"Acme Logistics\",\"amount\":0.01,\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-30\"}"))
        .andExpect(status().isCreated());
  }

  @Test
  void invalidRemarkOrOfferOnClosedTenderReturns400NotConflict() throws Exception {
    given(tenderService.addRemark(eq(1L), eq(""))).willThrow(new TenderClosedException(1L));
    given(tenderService.addOffer(eq(1L), eq(""), eq(BigDecimal.ZERO), any(), any(), any()))
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

  @Test
  void addOfferReturnsAllFiveOfferFieldsAndNormalisesBlankNoteToNull() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    Offer offer = TenderFixtures.offer("Acme Logistics", new BigDecimal("1234.56"));
    ReflectionTestUtils.setField(offer, "id", 20L);
    tender.addOffer(offer);
    given(tenderService.addOffer(eq(1L), eq("Acme Logistics"), any(), any(), any(), any()))
        .willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_OFFER_JSON))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.deliveryDate").value("2026-10-21"))
        .andExpect(jsonPath("$.validUntil").value("2026-10-30"))
        .andExpect(jsonPath("$.note").value(org.hamcrest.Matchers.nullValue()));
  }

  @Test
  void addOfferAcceptsValidUntilEqualToTodayAndBoundaryLengths() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    tender.addOffer(TenderFixtures.offer("Acme Logistics", new BigDecimal("1.00")));
    given(tenderService.addOffer(eq(1L), any(), any(), any(), any(), any())).willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(
                    "{\"supplierName\":\""
                        + "s".repeat(100)
                        + "\",\"amount\":1,\"deliveryDate\":\"2026-10-20\","
                        + "\"validUntil\":\"2026-10-13\",\"note\":\""
                        + "n".repeat(500)
                        + "\"}"))
        .andExpect(status().isCreated());
  }

  @Test
  void addOfferWithInvalidTermsReturns400WithViolationForThatField() throws Exception {
    String[][] cases = {
      {"validUntil", "\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-12\""},
      {"validUntil", "\"deliveryDate\":\"2026-10-21\""},
      {"deliveryDate", "\"validUntil\":\"2026-10-30\""},
      {
        "note",
        "\"deliveryDate\":\"2026-10-21\",\"validUntil\":\"2026-10-30\",\"note\":\""
            + "n".repeat(501)
            + "\""
      },
      {
        "supplierName",
        "\"supplierName\":\""
            + "s".repeat(101)
            + "\",\"deliveryDate\":\"2026-10-21\","
            + "\"validUntil\":\"2026-10-30\""
      },
    };
    for (String[] c : cases) {
      String supplier = c[1].contains("\"supplierName\"") ? "" : "\"supplierName\":\"Acme\",";
      mockMvc
          .perform(
              post("/api/tenders/{id}/offers", 1L)
                  .contentType(MediaType.APPLICATION_JSON)
                  .content("{" + supplier + "\"amount\":10," + c[1] + "}"))
          .andExpect(status().isBadRequest())
          .andExpect(jsonPath("$.violations.length()").value(1))
          .andExpect(jsonPath("$.violations[0].field").value(c[0]));
    }

    verifyNoInteractions(tenderService);
  }

  @Test
  void addOfferAfterBidDeadlineReturns409() throws Exception {
    given(tenderService.addOffer(eq(1L), any(), any(), any(), any(), any()))
        .willThrow(new BidDeadlinePassedException(1L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_OFFER_JSON))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.error").value("Conflict"))
        .andExpect(jsonPath("$.path").value("/api/tenders/1/offers"));
  }

  @Test
  void addOfferWithDeliveryBeforePickupReturns400WithDeliveryDateViolation() throws Exception {
    given(tenderService.addOffer(eq(1L), any(), any(), any(), any(), any()))
        .willThrow(new OfferDeliveryBeforePickupException(1L));

    mockMvc
        .perform(
            post("/api/tenders/{id}/offers", 1L)
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_OFFER_JSON))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.violations.length()").value(1))
        .andExpect(jsonPath("$.violations[0].field").value("deliveryDate"));
  }

  @Test
  void updateTenderReturns200WithTheUpdatedTender() throws Exception {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    given(tenderService.updateTender(eq(1L), any(CreateTenderRequest.class))).willReturn(tender);

    mockMvc
        .perform(
            put("/api/tenders/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_REQUEST_JSON))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.commodity").value("Maschinenteile auf Europaletten"))
        .andExpect(jsonPath("$.status").value("OPEN"));

    ArgumentCaptor<CreateTenderRequest> captor = ArgumentCaptor.forClass(CreateTenderRequest.class);
    verify(tenderService).updateTender(eq(1L), captor.capture());
    assertThat(captor.getValue().pickupDate().toString()).isEqualTo("2026-10-20");
  }

  @Test
  void updateTenderOnUnknownIdReturns404() throws Exception {
    given(tenderService.updateTender(eq(9L), any(CreateTenderRequest.class)))
        .willThrow(new TenderNotFoundException(9L));

    mockMvc
        .perform(
            put("/api/tenders/9")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_REQUEST_JSON))
        .andExpect(status().isNotFound());
  }

  @Test
  void updateTenderOnClosedTenderReturns409() throws Exception {
    given(tenderService.updateTender(eq(1L), any(CreateTenderRequest.class)))
        .willThrow(new TenderClosedException(1L));

    mockMvc
        .perform(
            put("/api/tenders/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_REQUEST_JSON))
        .andExpect(status().isConflict());
  }

  @Test
  void updateTenderChangingLockedFieldsReturns409NamingThem() throws Exception {
    given(tenderService.updateTender(eq(1L), any(CreateTenderRequest.class)))
        .willThrow(new TenderLockedFieldsException(1L, List.of("currency", "commodity")));

    mockMvc
        .perform(
            put("/api/tenders/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_REQUEST_JSON))
        .andExpect(status().isConflict())
        .andExpect(jsonPath("$.message").value(org.hamcrest.Matchers.containsString("currency")))
        .andExpect(jsonPath("$.path").value("/api/tenders/1"));
  }

  @Test
  void updateTenderWithViolationsReturns400InTheStandardShape() throws Exception {
    given(tenderService.updateTender(eq(1L), any(CreateTenderRequest.class)))
        .willThrow(
            new TenderRequestInvalidException(
                List.of(
                    new TenderExceptionHandler.Violation(
                        "bidDeadline", "must not be in the past"))));

    mockMvc
        .perform(
            put("/api/tenders/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content(TenderFixtures.VALID_REQUEST_JSON))
        .andExpect(status().isBadRequest())
        .andExpect(jsonPath("$.error").value("Bad Request"))
        .andExpect(jsonPath("$.violations[0].field").value("bidDeadline"))
        .andExpect(jsonPath("$.path").value("/api/tenders/1"));
  }
}
