package com.senacor.freighttenders.tender;

import jakarta.validation.Validation;
import jakarta.validation.Validator;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;

/**
 * Provides the Bean Validation {@link Validator} that {@link TenderService} needs, for
 * {@code @DataJpaTest} slices that import the service but do not auto-configure validation.
 */
@TestConfiguration
class ValidatorTestConfiguration {

  @Bean
  Validator validator() {
    return Validation.buildDefaultValidatorFactory().getValidator();
  }
}
