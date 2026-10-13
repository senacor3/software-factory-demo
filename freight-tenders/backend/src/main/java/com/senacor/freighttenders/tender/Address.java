package com.senacor.freighttenders.tender;

import jakarta.persistence.Embeddable;

/** A postal address of a shipment's pickup or delivery location, embedded in {@link Tender}. */
@Embeddable
public record Address(String country, String postalCode, String city) {}
