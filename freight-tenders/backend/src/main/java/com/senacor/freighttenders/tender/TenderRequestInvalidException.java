package com.senacor.freighttenders.tender;

import java.util.List;

/** Thrown when a tender update request breaks a validation rule; carries every violation. */
public class TenderRequestInvalidException extends RuntimeException {

  private static final long serialVersionUID = 1L;

  private final transient List<TenderExceptionHandler.Violation> violations;

  public TenderRequestInvalidException(List<TenderExceptionHandler.Violation> violations) {
    super("Request validation failed");
    this.violations = List.copyOf(violations);
  }

  public List<TenderExceptionHandler.Violation> getViolations() {
    return violations;
  }
}
