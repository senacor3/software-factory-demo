package com.senacor.freighttenders.tender;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import java.time.Clock;
import java.time.LocalDate;

/**
 * Enforces that an offer's {@code validUntil} is today or later. "Today" comes from the injected
 * {@link Clock}, and the violation is attached to the {@code validUntil} field. Null values are
 * left to the field-level constraints.
 */
public class AddOfferRequestValidator
    implements ConstraintValidator<ValidAddOfferRequest, AddOfferRequest> {

  private final Clock clock;

  public AddOfferRequestValidator(Clock clock) {
    this.clock = clock;
  }

  @Override
  public boolean isValid(AddOfferRequest request, ConstraintValidatorContext context) {
    if (request == null || request.validUntil() == null) {
      return true;
    }
    if (request.validUntil().isBefore(LocalDate.now(clock))) {
      context.disableDefaultConstraintViolation();
      context
          .buildConstraintViolationWithTemplate("must not be in the past")
          .addPropertyNode("validUntil")
          .addConstraintViolation();
      return false;
    }
    return true;
  }
}
