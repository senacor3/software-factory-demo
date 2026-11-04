package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * The cross-field and "today"-relative rules of a {@link CreateTenderRequest}, shared by {@link
 * CreateTenderRequestValidator} (create) and {@link TenderService#updateTender} (edit). Null values
 * are left to the field-level constraints.
 */
final class CreateTenderRules {

  private CreateTenderRules() {}

  /**
   * Checks every rule. When {@code stored} is non-null (an edit), the "today or later" rules for
   * pickupDate and bidDeadline only apply to a date that differs from the stored value.
   */
  static List<Violation> check(CreateTenderRequest request, LocalDate today, Tender stored) {
    List<Violation> violations = new ArrayList<>();
    LocalDate pickup = request.pickupDate();
    LocalDate delivery = request.deliveryDate();
    LocalDate deadline = request.bidDeadline();

    if (pickup != null
        && pickup.isBefore(today)
        && (stored == null || !Objects.equals(pickup, stored.getPickupDate()))) {
      violations.add(new Violation("pickupDate", "must not be in the past"));
    }
    if (pickup != null && delivery != null && delivery.isBefore(pickup)) {
      violations.add(new Violation("deliveryDate", "must not be before pickupDate"));
    }
    if (deadline != null
        && deadline.isBefore(today)
        && (stored == null || !Objects.equals(deadline, stored.getBidDeadline()))) {
      violations.add(new Violation("bidDeadline", "must not be in the past"));
    }
    if (pickup != null && deadline != null && deadline.isAfter(pickup)) {
      violations.add(new Violation("bidDeadline", "must not be after pickupDate"));
    }

    if (Boolean.TRUE.equals(request.dangerousGoods()) && request.adrClass() == null) {
      violations.add(new Violation("adrClass", "is required when dangerousGoods is true"));
    }
    if (Boolean.FALSE.equals(request.dangerousGoods()) && request.adrClass() != null) {
      violations.add(new Violation("adrClass", "must be absent unless dangerousGoods is true"));
    }

    if (Boolean.TRUE.equals(request.temperatureControlled())) {
      if (request.equipmentType() != null && request.equipmentType() != EquipmentType.REEFER) {
        violations.add(new Violation("equipmentType", "must be REEFER when temperatureControlled"));
      }
      if (request.temperatureMinC() == null) {
        violations.add(new Violation("temperatureMinC", "is required when temperatureControlled"));
      }
      if (request.temperatureMaxC() == null) {
        violations.add(new Violation("temperatureMaxC", "is required when temperatureControlled"));
      }
      if (request.temperatureMinC() != null
          && request.temperatureMaxC() != null
          && request.temperatureMinC() > request.temperatureMaxC()) {
        violations.add(new Violation("temperatureMinC", "must not be above temperatureMaxC"));
        violations.add(new Violation("temperatureMaxC", "must not be below temperatureMinC"));
      }
    }
    if (Boolean.FALSE.equals(request.temperatureControlled())) {
      if (request.temperatureMinC() != null) {
        violations.add(
            new Violation("temperatureMinC", "must be absent unless temperatureControlled"));
      }
      if (request.temperatureMaxC() != null) {
        violations.add(
            new Violation("temperatureMaxC", "must be absent unless temperatureControlled"));
      }
    }
    return violations;
  }
}
