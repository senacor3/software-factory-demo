package com.senacor.freighttenders.tender;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

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
}
