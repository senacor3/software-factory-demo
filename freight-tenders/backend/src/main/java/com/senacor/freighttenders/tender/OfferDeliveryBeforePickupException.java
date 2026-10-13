package com.senacor.freighttenders.tender;

/** Thrown when an offer's delivery date lies before the pickup date of its {@link Tender}. */
public class OfferDeliveryBeforePickupException extends RuntimeException {

  public OfferDeliveryBeforePickupException(Long tenderId) {
    super("The offer's deliveryDate must not be before the pickupDate of tender " + tenderId);
  }
}
