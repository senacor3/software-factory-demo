package com.senacor.freighttenders.tender;

import jakarta.validation.constraints.NotBlank;

/** Request body for {@code POST /api/tenders/{id}/remarks}. */
public record AddRemarkRequest(@NotBlank String text) {}
