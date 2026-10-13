package com.senacor.freighttenders.tender;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import java.time.Clock;
import java.time.LocalDate;

/**
 * Enforces the rules of a {@link CreateTenderRequest} that involve more than one field or today's
 * date. "Today" comes from the injected {@link Clock} (Spring's constraint validator factory
 * autowires the constructor), and every violation is attached to the field to fix, so the exception
 * handler reports it like any other field error. Null values are left to the field-level
 * constraints.
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
    boolean valid = true;
    LocalDate today = LocalDate.now(clock);
    LocalDate pickup = request.pickupDate();
    LocalDate delivery = request.deliveryDate();
    LocalDate deadline = request.bidDeadline();

    if (pickup != null && pickup.isBefore(today)) {
      valid = reject(context, "pickupDate", "must not be in the past");
    }
    if (pickup != null && delivery != null && delivery.isBefore(pickup)) {
      valid = reject(context, "deliveryDate", "must not be before pickupDate");
    }
    if (deadline != null && deadline.isBefore(today)) {
      valid = reject(context, "bidDeadline", "must not be in the past");
    }
    if (pickup != null && deadline != null && deadline.isAfter(pickup)) {
      valid = reject(context, "bidDeadline", "must not be after pickupDate");
    }

    if (Boolean.TRUE.equals(request.dangerousGoods()) && request.adrClass() == null) {
      valid = reject(context, "adrClass", "is required when dangerousGoods is true");
    }
    if (Boolean.FALSE.equals(request.dangerousGoods()) && request.adrClass() != null) {
      valid = reject(context, "adrClass", "must be absent unless dangerousGoods is true");
    }

    if (Boolean.TRUE.equals(request.temperatureControlled())) {
      if (request.equipmentType() != null && request.equipmentType() != EquipmentType.REEFER) {
        valid = reject(context, "equipmentType", "must be REEFER when temperatureControlled");
      }
      if (request.temperatureMinC() == null) {
        valid = reject(context, "temperatureMinC", "is required when temperatureControlled");
      }
      if (request.temperatureMaxC() == null) {
        valid = reject(context, "temperatureMaxC", "is required when temperatureControlled");
      }
      if (request.temperatureMinC() != null
          && request.temperatureMaxC() != null
          && request.temperatureMinC() > request.temperatureMaxC()) {
        valid = reject(context, "temperatureMinC", "must not be above temperatureMaxC");
        valid = reject(context, "temperatureMaxC", "must not be below temperatureMinC");
      }
    }
    if (Boolean.FALSE.equals(request.temperatureControlled())) {
      if (request.temperatureMinC() != null) {
        valid = reject(context, "temperatureMinC", "must be absent unless temperatureControlled");
      }
      if (request.temperatureMaxC() != null) {
        valid = reject(context, "temperatureMaxC", "must be absent unless temperatureControlled");
      }
    }
    return valid;
  }

  private static boolean reject(ConstraintValidatorContext context, String field, String message) {
    context
        .buildConstraintViolationWithTemplate(message)
        .addPropertyNode(field)
        .addConstraintViolation();
    return false;
  }
}
