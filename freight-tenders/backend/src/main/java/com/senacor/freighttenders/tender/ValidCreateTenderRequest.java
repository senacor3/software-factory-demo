package com.senacor.freighttenders.tender;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Cross-field and clock-dependent rules of a {@link CreateTenderRequest}. Each violation is
 * reported on the field the user has to fix, see {@link CreateTenderRequestValidator}.
 */
@Documented
@Constraint(validatedBy = CreateTenderRequestValidator.class)
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidCreateTenderRequest {

  String message() default "Invalid tender request";

  Class<?>[] groups() default {};

  Class<? extends Payload>[] payload() default {};
}
