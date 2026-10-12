package com.senacor.freighttenders.tender;

import java.math.BigDecimal;

/** Request body for {@code POST /api/tenders/{id}/offers}. */
public record AddOfferRequest(String supplierName, BigDecimal amount) {}
