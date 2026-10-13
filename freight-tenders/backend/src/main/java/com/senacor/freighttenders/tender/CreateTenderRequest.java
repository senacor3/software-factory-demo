package com.senacor.freighttenders.tender;

import jakarta.validation.Valid;
import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Request body for {@code POST /api/tenders}: a spot tender for one European road shipment.
 *
 * <p>Field rules are declared here; the cross-field and "today"-relative rules live in {@link
 * CreateTenderRequestValidator}. The explicit {@code getXxx()} methods for the fields that
 * validator reports on let Spring's binding result read the rejected value of a class-level
 * violation on a record, which has no JavaBean getters of its own.
 */
@ValidCreateTenderRequest
public record CreateTenderRequest(
    @NotNull @Valid AddressRequest origin,
    @NotNull @Valid AddressRequest destination,
    @NotNull LocalDate pickupDate,
    @NotNull LocalDate deliveryDate,
    @NotNull LocalDate bidDeadline,
    @NotBlank @Size(max = 200) String commodity,
    @NotNull @Min(1) @Max(40000) Integer weightKg,
    @NotNull @DecimalMin("0.1") @DecimalMax("13.6") @Digits(integer = 2, fraction = 1)
        BigDecimal loadingMeters,
    @Min(1) @Max(66) Integer palletCount,
    @NotNull EquipmentType equipmentType,
    @NotNull Boolean dangerousGoods,
    @Pattern(regexp = "1|2|3|4\\.1|4\\.2|4\\.3|5\\.1|5\\.2|6\\.1|6\\.2|7|8|9") String adrClass,
    @NotNull Boolean temperatureControlled,
    @Min(-30) @Max(30) Integer temperatureMinC,
    @Min(-30) @Max(30) Integer temperatureMaxC,
    @NotNull Currency currency) {

  /** An origin or destination address. */
  public record AddressRequest(
      @NotNull @Pattern(regexp = "[A-Z]{2}") String country,
      @NotBlank @Size(max = 10) String postalCode,
      @NotBlank @Size(max = 100) String city) {

    Address toAddress() {
      return new Address(country, postalCode, city);
    }
  }

  public LocalDate getPickupDate() {
    return pickupDate;
  }

  public LocalDate getDeliveryDate() {
    return deliveryDate;
  }

  public LocalDate getBidDeadline() {
    return bidDeadline;
  }

  public EquipmentType getEquipmentType() {
    return equipmentType;
  }

  public String getAdrClass() {
    return adrClass;
  }

  public Integer getTemperatureMinC() {
    return temperatureMinC;
  }

  public Integer getTemperatureMaxC() {
    return temperatureMaxC;
  }
}
