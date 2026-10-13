package com.senacor.freighttenders.tender;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.math.BigDecimal;

/** Request body for {@code POST /api/tenders/{id}/offers}. */
public record AddOfferRequest(
    @NotBlank String supplierName, @NotNull @DecimalMin("0.01") BigDecimal amount) {}
