package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import java.util.List;

/** Thrown when an edit request breaks a validation rule; carries the violated fields. */
public class TenderValidationException extends RuntimeException {

  private final transient List<Violation> violations;

  public TenderValidationException(List<Violation> violations) {
    super("Request validation failed");
    this.violations = List.copyOf(violations);
  }

  public List<Violation> getViolations() {
    return violations;
  }
}
