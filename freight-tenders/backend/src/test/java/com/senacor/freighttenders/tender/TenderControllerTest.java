package com.senacor.freighttenders.tender;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(TenderController.class)
class TenderControllerTest {

  @Autowired private MockMvc mockMvc;

  @MockitoBean private TenderService tenderService;

  @Test
  void createTenderReturns201WithOpenTender() throws Exception {
    Tender tender = new Tender("Hamburg", "Rotterdam");
    ReflectionTestUtils.setField(tender, "id", 1L);
    given(tenderService.createTender(eq("Hamburg"), eq("Rotterdam"))).willReturn(tender);

    mockMvc
        .perform(
            post("/api/tenders")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"origin\":\"Hamburg\",\"destination\":\"Rotterdam\"}"))
        .andExpect(status().isCreated())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.id").value(1))
        .andExpect(jsonPath("$.origin").value("Hamburg"))
        .andExpect(jsonPath("$.destination").value("Rotterdam"))
        .andExpect(jsonPath("$.status").value("OPEN"));
  }

  @Test
  void closeTenderReturns200WithClosedTender() throws Exception {
    Tender tender = new Tender("Hamburg", "Rotterdam");
    tender.close();
    given(tenderService.closeTender(1L)).willReturn(tender);

    mockMvc
        .perform(post("/api/tenders/{id}/close", 1L))
        .andExpect(status().isOk())
        .andExpect(content().contentType(MediaType.APPLICATION_JSON))
        .andExpect(jsonPath("$.status").value("CLOSED"));
  }

  @Test
  void listTendersFilteredByStatusReturnsOnlyOpenTenders() throws Exception {
    Tender openTender = new Tender("Hamburg", "Rotterdam");
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
  void listTendersWithNoFilterReturnsOpenAndClosedTenders() throws Exception {
    Tender openTender = new Tender("Hamburg", "Rotterdam");
    ReflectionTestUtils.setField(openTender, "id", 1L);
    Tender closedTender = new Tender("Berlin", "Munich");
    ReflectionTestUtils.setField(closedTender, "id", 2L);
    closedTender.close();
    given(tenderService.listTenders(Optional.empty()))
        .willReturn(List.of(openTender, closedTender));

    mockMvc
        .perform(get("/api/tenders"))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.length()").value(2))
        .andExpect(jsonPath("$[0].status").value("OPEN"))
        .andExpect(jsonPath("$[1].status").value("CLOSED"));
  }

  @Test
  void getTenderReturns200WithNestedRemarksAndOffers() throws Exception {
    Tender tender = new Tender("Hamburg", "Rotterdam");
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
        .andExpect(jsonPath("$.origin").value("Hamburg"))
        .andExpect(jsonPath("$.destination").value("Rotterdam"))
        .andExpect(jsonPath("$.remarks[0].text").value("Please expedite"))
        .andExpect(jsonPath("$.offers[0].supplierName").value("Acme Logistics"));
  }

  @Test
  void addRemarkOnOpenTenderReturns201WithCreatedRemark() throws Exception {
    Tender tender = new Tender("Hamburg", "Rotterdam");
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
    Tender tender = new Tender("Hamburg", "Rotterdam");
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
}
