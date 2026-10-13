package com.senacor.freighttenders.tender;

import java.util.List;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Spring Data JPA repository for {@link Tender} aggregates. The list queries fetch {@code offers}
 * eagerly so that {@link TenderResponse} can summarise them without one extra query per tender.
 */
public interface TenderRepository extends JpaRepository<Tender, Long> {

  @Override
  @EntityGraph(attributePaths = "offers")
  List<Tender> findAll();

  @EntityGraph(attributePaths = "offers")
  List<Tender> findByStatus(TenderStatus status);
}
