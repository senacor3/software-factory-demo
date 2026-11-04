package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import java.util.List;

/** Thrown when a tender update request breaks one or more validation rules. */
public class InvalidTenderException extends RuntimeException {

  private final transient List<Violation> violations;

  public InvalidTenderException(List<Violation> violations) {
    super("Request validation failed");
    this.violations = List.copyOf(violations);
  }

  public List<Violation> getViolations() {
    return violations;
  }
}
