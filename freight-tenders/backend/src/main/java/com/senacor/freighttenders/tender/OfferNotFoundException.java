package com.senacor.freighttenders.tender;

/** Thrown when an offer id does not match any {@link Offer} of the given {@link Tender}. */
public class OfferNotFoundException extends RuntimeException {

  public OfferNotFoundException(Long tenderId, Long offerId) {
    super("No offer found with id " + offerId + " in tender " + tenderId);
  }
}
