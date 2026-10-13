package com.senacor.freighttenders.tender;

import java.math.BigDecimal;
import java.time.LocalDate;

/** Response body for an {@link Offer}, nested under {@link TenderDetailResponse}. */
public record OfferResponse(
    Long id,
    String supplierName,
    BigDecimal amount,
    LocalDate deliveryDate,
    LocalDate validUntil,
    String note) {

  public static OfferResponse from(Offer offer) {
    return new OfferResponse(
        offer.getId(),
        offer.getSupplierName(),
        offer.getAmount(),
        offer.getDeliveryDate(),
        offer.getValidUntil(),
        offer.getNote());
  }
}
