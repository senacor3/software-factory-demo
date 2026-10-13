package com.senacor.freighttenders.tender;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Full detail response body for {@code GET /api/tenders/{id}} -- the tender's own fields plus its
 * remarks and offers nested as DTOs, never the entities themselves (see {@link TenderResponse}).
 */
public record TenderDetailResponse(
    Long id,
    AddressResponse origin,
    AddressResponse destination,
    LocalDate pickupDate,
    LocalDate deliveryDate,
    LocalDate bidDeadline,
    String commodity,
    Integer weightKg,
    BigDecimal loadingMeters,
    Integer palletCount,
    EquipmentType equipmentType,
    boolean dangerousGoods,
    String adrClass,
    boolean temperatureControlled,
    Integer temperatureMinC,
    Integer temperatureMaxC,
    Currency currency,
    TenderStatus status,
    Long awardedOfferId,
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
        AddressResponse.from(tender.getOrigin()),
        AddressResponse.from(tender.getDestination()),
        tender.getPickupDate(),
        tender.getDeliveryDate(),
        tender.getBidDeadline(),
        tender.getCommodity(),
        tender.getWeightKg(),
        tender.getLoadingMeters(),
        tender.getPalletCount(),
        tender.getEquipmentType(),
        tender.isDangerousGoods(),
        tender.getAdrClass(),
        tender.isTemperatureControlled(),
        tender.getTemperatureMinC(),
        tender.getTemperatureMaxC(),
        tender.getCurrency(),
        tender.getStatus(),
        tender.getAwardedOffer() == null ? null : tender.getAwardedOffer().getId(),
        tender.getRemarks().stream().map(RemarkResponse::from).toList(),
        tender.getOffers().stream().map(OfferResponse::from).toList());
  }
}
