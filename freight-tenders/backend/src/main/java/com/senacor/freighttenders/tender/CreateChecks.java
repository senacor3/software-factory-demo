package com.senacor.freighttenders.tender;

import jakarta.validation.groups.Default;

/**
 * Validation group of {@code POST /api/tenders}: the default field rules plus the cross-field and
 * "today"-relative rules of {@link ValidCreateTenderRequest}. {@code PUT /api/tenders/{id}}
 * validates the default group only and applies those rules itself, see {@link TenderService}.
 */
public interface CreateChecks extends Default {}
