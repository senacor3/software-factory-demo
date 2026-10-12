package com.senacor.freighttenders.tender;

/** Request body for {@code POST /api/tenders}. */
public record CreateTenderRequest(String origin, String destination) {}
