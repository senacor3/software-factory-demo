package com.senacor.freighttenders.tender;

import jakarta.validation.constraints.NotBlank;

/** Request body for {@code POST /api/tenders}. */
public record CreateTenderRequest(@NotBlank String origin, @NotBlank String destination) {}
