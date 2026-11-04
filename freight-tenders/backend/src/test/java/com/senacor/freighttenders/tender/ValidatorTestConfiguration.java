package com.senacor.freighttenders.tender;

import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.validation.beanvalidation.LocalValidatorFactoryBean;

/**
 * Supplies the bean validator that {@code @DataJpaTest} slices omit but {@link TenderService}
 * needs.
 */
@TestConfiguration(proxyBeanMethods = false)
class ValidatorTestConfiguration {

  @Bean
  LocalValidatorFactoryBean testValidator() {
    return new LocalValidatorFactoryBean();
  }
}
