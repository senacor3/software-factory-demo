package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * The rules of a {@link CreateTenderRequest} that involve more than one field or today's date,
 * shared by create ({@link CreateTenderRequestValidator}) and update ({@link TenderService}). Null
 * values are left to the field-level constraints.
 */
final class TenderRules {

  private TenderRules() {}

  /** Rules relating the fields of the request to each other, independent of today's date. */
  static List<Violation> crossFieldViolations(CreateTenderRequest request) {
    List<Violation> violations = new ArrayList<>();
    LocalDate pickup = request.pickupDate();
    LocalDate delivery = request.deliveryDate();
    LocalDate deadline = request.bidDeadline();

    if (pickup != null && delivery != null && delivery.isBefore(pickup)) {
      violations.add(new Violation("deliveryDate", "must not be before pickupDate"));
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

  /**
   * The "today or later" rules. {@code checkPickup} and {@code checkDeadline} select which of the
   * two dates are checked, so an update can skip a date it leaves unchanged.
   */
  static List<Violation> pastDateViolations(
      CreateTenderRequest request, LocalDate today, boolean checkPickup, boolean checkDeadline) {
    List<Violation> violations = new ArrayList<>();
    LocalDate pickup = request.pickupDate();
    LocalDate deadline = request.bidDeadline();
    if (checkPickup && pickup != null && pickup.isBefore(today)) {
      violations.add(new Violation("pickupDate", "must not be in the past"));
    }
    if (checkDeadline && deadline != null && deadline.isBefore(today)) {
      violations.add(new Violation("bidDeadline", "must not be in the past"));
    }
    return violations;
  }
}
