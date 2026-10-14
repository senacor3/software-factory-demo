package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import java.time.Clock;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * Enforces the rules of a {@link CreateTenderRequest} that involve more than one field or today's
 * date. "Today" comes from the injected {@link Clock} (Spring's constraint validator factory
 * autowires the constructor), and every violation is attached to the field to fix, so the exception
 * handler reports it like any other field error. Null values are left to the field-level
 * constraints.
 */
public class CreateTenderRequestValidator
    implements ConstraintValidator<ValidCreateTenderRequest, CreateTenderRequest> {

  private final Clock clock;

  public CreateTenderRequestValidator(Clock clock) {
    this.clock = clock;
  }

  @Override
  public boolean isValid(CreateTenderRequest request, ConstraintValidatorContext context) {
    if (request == null) {
      return true;
    }
    context.disableDefaultConstraintViolation();
    List<Violation> violations = new ArrayList<>();
    violations.addAll(TenderRules.pastDateViolations(request, LocalDate.now(clock), true, true));
    violations.addAll(TenderRules.crossFieldViolations(request));
    for (Violation violation : violations) {
      context
          .buildConstraintViolationWithTemplate(violation.message())
          .addPropertyNode(violation.field())
          .addConstraintViolation();
    }
    return violations.isEmpty();
  }
}
