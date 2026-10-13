package com.senacor.freighttenders.tender;

/** Thrown when an {@link Offer} is awarded after its {@code validUntil} date has passed. */
public class OfferExpiredException extends RuntimeException {

  public OfferExpiredException(Long offerId) {
    super("Offer " + offerId + " has expired and can no longer be awarded");
  }
}
