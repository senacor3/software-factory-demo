package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import java.time.Clock;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * Enforces the rules of a {@link CreateTenderRequest} that involve more than one field or today's
 * date. "Today" comes from the injected {@link Clock} (Spring's constraint validator factory
 * autowires the constructor), and every violation is attached to the field to fix, so the exception
 * handler reports it like any other field error. Null values are left to the field-level
 * constraints.
 *
 * <p>The rules themselves live in {@link #check}, which {@link TenderService#updateTender} reuses:
 * an update may repeat a stored date that has since slipped into the past, so it passes the stored
 * dates as the ones exempt from the "today or later" rules.
 */
public class CreateTenderRequestValidator
    implements ConstraintValidator<ValidCreateTenderRequest, CreateTenderRequest> {

  private final Clock clock;

  public CreateTenderRequestValidator(Clock clock) {
    this.clock = clock;
  }

  @Override
  public boolean isValid(CreateTenderRequest request, ConstraintValidatorContext context) {
    if (request == null) {
      return true;
    }
    context.disableDefaultConstraintViolation();
    List<Violation> violations = check(request, LocalDate.now(clock), null, null);
    for (Violation violation : violations) {
      context
          .buildConstraintViolationWithTemplate(violation.message())
          .addPropertyNode(violation.field())
          .addConstraintViolation();
    }
    return violations.isEmpty();
  }

  /**
   * Evaluates the cross-field and "today"-relative rules.
   *
   * @param today the current date
   * @param unchangedPickupDate a pickup date that is accepted even if in the past (the stored one
   *     on update), or {@code null} if past dates are never accepted
   * @param unchangedBidDeadline the same for the bid deadline
   */
  static List<Violation> check(
      CreateTenderRequest request,
      LocalDate today,
      LocalDate unchangedPickupDate,
      LocalDate unchangedBidDeadline) {
    List<Violation> violations = new ArrayList<>();
    LocalDate pickup = request.pickupDate();
    LocalDate delivery = request.deliveryDate();
    LocalDate deadline = request.bidDeadline();

    if (pickup != null && pickup.isBefore(today) && !pickup.equals(unchangedPickupDate)) {
      violations.add(new Violation("pickupDate", "must not be in the past"));
    }
    if (pickup != null && delivery != null && delivery.isBefore(pickup)) {
      violations.add(new Violation("deliveryDate", "must not be before pickupDate"));
    }
    if (deadline != null && deadline.isBefore(today) && !deadline.equals(unchangedBidDeadline)) {
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
        violations.add(
            new Violation("equipmentType", "must be REEFER when temperatureControlled"));
      }
      if (request.temperatureMinC() == null) {
        violations.add(
            new Violation("temperatureMinC", "is required when temperatureControlled"));
      }
      if (request.temperatureMaxC() == null) {
        violations.add(
            new Violation("temperatureMaxC", "is required when temperatureControlled"));
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
