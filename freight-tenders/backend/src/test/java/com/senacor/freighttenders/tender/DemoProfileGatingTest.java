package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.http.MediaType.APPLICATION_JSON;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.LocalDate;
import java.time.ZoneId;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.context.ApplicationContext;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

class DemoProfileGatingTest {

  @Nested
  @SpringBootTest(properties = "spring.datasource.url=jdbc:h2:mem:gating-without-demo")
  @AutoConfigureMockMvc
  class WithoutDemoProfile {

    @Autowired private ApplicationContext context;

    @Autowired private MockMvc mockMvc;

    @Test
    void seederBeanIsAbsentAndNoTendersExist() throws Exception {
      assertThat(context.getBeanNamesForType(DemoDataSeeder.class)).isEmpty();

      mockMvc
          .perform(get("/api/tenders"))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.length()").value(0));
    }
  }

  @Nested
  @SpringBootTest(properties = "spring.datasource.url=jdbc:h2:mem:gating-with-demo")
  @AutoConfigureMockMvc
  @ActiveProfiles("demo")
  class WithDemoProfile {

    @Autowired private MockMvc mockMvc;

    @Autowired private TenderRepository tenderRepository;

    @Test
    void listsTheEightSeededTenders() throws Exception {
      mockMvc
          .perform(get("/api/tenders"))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.length()").value(8));
    }

    @Test
    void addingAnOfferToTheSeededTenderWithPassedDeadlineReturns409() throws Exception {
      LocalDate today = LocalDate.now(ZoneId.of("Europe/Berlin"));
      Long id =
          tenderRepository.findAll().stream()
              .filter(t -> t.getBidDeadline().isBefore(today))
              .findFirst()
              .orElseThrow()
              .getId();
      String body =
          """
          {"supplierName":"Spät GmbH","amount":100,"deliveryDate":"%s","validUntil":"%s"}
          """
              .formatted(today.plusDays(10), today.plusDays(5));

      mockMvc
          .perform(post("/api/tenders/{id}/offers", id).contentType(APPLICATION_JSON).content(body))
          .andExpect(status().isConflict());
    }
  }
}
