package com.senacor.freighttenders.tender;

/**
 * Response body for the tender API -- a DTO rather than the {@link Tender} entity itself, since
 * {@link Remark}/{@link Offer} hold a back-reference to their parent and serializing the entity
 * graph directly would recurse infinitely over JSON.
 */
public record TenderResponse(Long id, String origin, String destination, TenderStatus status) {

  public static TenderResponse from(Tender tender) {
    return new TenderResponse(
        tender.getId(), tender.getOrigin(), tender.getDestination(), tender.getStatus());
  }
}
