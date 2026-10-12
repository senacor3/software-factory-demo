package com.senacor.freighttenders.tender;

import java.math.BigDecimal;

/** Response body for an {@link Offer}, nested under {@link TenderDetailResponse}. */
public record OfferResponse(Long id, String supplierName, BigDecimal amount) {

  public static OfferResponse from(Offer offer) {
    return new OfferResponse(offer.getId(), offer.getSupplierName(), offer.getAmount());
  }
}
