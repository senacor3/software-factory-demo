package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;

import jakarta.persistence.EntityManager;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.context.annotation.Import;

/**
 * Proves, against a real {@link TenderRepository}/Hibernate persistence context rather than the
 * mocked repository used by {@link TenderServiceTest}, that {@code TenderController}'s assumption
 * -- the newly-added remark/offer is always the last element of the {@link Tender} returned by
 * {@link TenderService#addRemark}/{@link TenderService#addOffer} -- actually holds. This relies on
 * {@code spring.jpa.open-in-view=true} keeping the service's {@code findById} and {@code save} in
 * one persistence context, since {@link TenderService} has no {@code @Transactional} of its own.
 */
@DataJpaTest(properties = "spring.jpa.properties.hibernate.generate_statistics=true")
@Import({TenderService.class, FixedClockConfiguration.class})
class TenderServicePersistenceTest {

  @Autowired private EntityManager entityManager;

  @Autowired private TenderService tenderService;

  @Autowired private TenderRepository tenderRepository;

  @Test
  void addRemarkAppendsTheNewRemarkAsTheLastElementAfterRealPersistence() {
    Tender tender = TenderFixtures.tender();
    tender.addRemark(new Remark("First remark"));
    Long id = tenderRepository.save(tender).getId();

    Tender result = tenderService.addRemark(id, "Second remark");

    assertThat(result.getRemarks()).hasSize(2);
    assertThat(result.getRemarks().get(result.getRemarks().size() - 1).getText())
        .isEqualTo("Second remark");
  }

  @Test
  void listingTendersFetchesOffersWithAConstantNumberOfQueries() {
    for (int i = 0; i < 5; i++) {
      Tender tender = TenderFixtures.tender();
      tender.addOffer(TenderFixtures.offer("Supplier " + i, new BigDecimal("100.00")));
      tender.addOffer(TenderFixtures.offer("Other Supplier " + i, new BigDecimal("200.00")));
      tenderRepository.save(tender);
    }
    entityManager.flush();
    entityManager.clear();
    Statistics statistics =
        entityManager.getEntityManagerFactory().unwrap(SessionFactory.class).getStatistics();
    statistics.clear();

    List<Tender> tenders = tenderService.listTenders(Optional.empty());
    int offerCount = tenders.stream().mapToInt(t -> t.getOffers().size()).sum();

    assertThat(tenders).hasSize(5);
    assertThat(offerCount).isEqualTo(10);
    assertThat(statistics.getPrepareStatementCount()).isEqualTo(1);
  }

  @Test
  void addOfferAppendsTheNewOfferAsTheLastElementAfterRealPersistence() {
    Tender tender = TenderFixtures.tender();
    tender.addOffer(TenderFixtures.offer("First Supplier", new BigDecimal("100.00")));
    Long id = tenderRepository.save(tender).getId();

    Tender result =
        tenderService.addOffer(
            id,
            "Second Supplier",
            new BigDecimal("200.00"),
            LocalDate.of(2026, 10, 21),
            LocalDate.of(2026, 10, 30),
            "Note");

    assertThat(result.getOffers()).hasSize(2);
    assertThat(result.getOffers().get(result.getOffers().size() - 1).getSupplierName())
        .isEqualTo("Second Supplier");
  }
}
