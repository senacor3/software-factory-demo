package com.senacor.freighttenders.tender;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Response body for the tender API -- a DTO rather than the {@link Tender} entity itself, since
 * {@link Remark}/{@link Offer} hold a back-reference to their parent and serializing the entity
 * graph directly would recurse infinitely over JSON.
 */
public record TenderResponse(
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
    TenderStatus status) {

  public static TenderResponse from(Tender tender) {
    return new TenderResponse(
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
        tender.getStatus());
  }
}
