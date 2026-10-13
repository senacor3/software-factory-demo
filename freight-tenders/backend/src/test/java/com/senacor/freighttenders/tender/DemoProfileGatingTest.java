package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

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

    @Test
    void listsTheEightSeededTenders() throws Exception {
      mockMvc
          .perform(get("/api/tenders"))
          .andExpect(status().isOk())
          .andExpect(jsonPath("$.length()").value(8));
    }
  }
}
