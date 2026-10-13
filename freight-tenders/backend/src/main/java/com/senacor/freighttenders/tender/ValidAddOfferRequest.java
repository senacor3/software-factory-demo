package com.senacor.freighttenders.tender;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Clock-dependent rules of an {@link AddOfferRequest}. The violation is reported on the field the
 * user has to fix, see {@link AddOfferRequestValidator}.
 */
@Documented
@Constraint(validatedBy = AddOfferRequestValidator.class)
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidAddOfferRequest {

  String message() default "Invalid offer request";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
