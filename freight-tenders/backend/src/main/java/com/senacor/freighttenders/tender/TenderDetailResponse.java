package com.senacor.freighttenders.tender;

import java.util.List;

/**
 * Full detail response body for {@code GET /api/tenders/{id}} -- the tender's own fields plus its
 * remarks and offers nested as DTOs, never the entities themselves (see {@link TenderResponse}).
 */
public record TenderDetailResponse(
    Long id,
    String origin,
    String destination,
    TenderStatus status,
    List<RemarkResponse> remarks,
    List<OfferResponse> offers) {

  // Defensive copy so neither the constructor nor the accessors expose the caller's or this
  // record's own list instance for external mutation (SpotBugs EI_EXPOSE_REP/EI_EXPOSE_REP2).
  public TenderDetailResponse {
    remarks = List.copyOf(remarks);
    offers = List.copyOf(offers);
  }

  public static TenderDetailResponse from(Tender tender) {
    return new TenderDetailResponse(
        tender.getId(),
        tender.getOrigin(),
        tender.getDestination(),
        tender.getStatus(),
        tender.getRemarks().stream().map(RemarkResponse::from).toList(),
        tender.getOffers().stream().map(OfferResponse::from).toList());
  }
}
