package com.senacor.freighttenders.tender;

/** Thrown when a tender id does not match any existing {@link Tender}. */
public class TenderNotFoundException extends RuntimeException {

  public TenderNotFoundException(Long tenderId) {
    super("No tender found with id " + tenderId);
  }
}
