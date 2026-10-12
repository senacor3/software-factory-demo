package com.senacor.freighttenders.tender;

/** Request body for {@code POST /api/tenders/{id}/remarks}. */
public record AddRemarkRequest(String text) {}
