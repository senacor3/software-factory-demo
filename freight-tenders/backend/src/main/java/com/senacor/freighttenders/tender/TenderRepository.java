package com.senacor.freighttenders.tender;

import org.springframework.data.jpa.repository.JpaRepository;

/** Spring Data JPA repository for {@link Tender} aggregates. */
public interface TenderRepository extends JpaRepository<Tender, Long> {}
