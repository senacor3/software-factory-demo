package com.senacor.freighttenders.tender;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.math.BigDecimal;
import java.time.LocalDate;

/** Request body for {@code POST /api/tenders/{id}/offers}. */
@ValidAddOfferRequest
public record AddOfferRequest(
    @NotBlank @Size(max = 100) String supplierName,
    @NotNull @DecimalMin("0.01") BigDecimal amount,
    @NotNull LocalDate deliveryDate,
    @NotNull LocalDate validUntil,
    @Size(max = 500) String note) {}
