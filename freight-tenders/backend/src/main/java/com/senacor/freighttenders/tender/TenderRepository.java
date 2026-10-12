package com.senacor.freighttenders.tender;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

/** Spring Data JPA repository for {@link Tender} aggregates. */
public interface TenderRepository extends JpaRepository<Tender, Long> {

  List<Tender> findByStatus(TenderStatus status);
}
