package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
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
@DataJpaTest
@Import(TenderService.class)
class TenderServicePersistenceTest {

  @Autowired private TenderService tenderService;

  @Autowired private TenderRepository tenderRepository;

  @Test
  void addRemarkAppendsTheNewRemarkAsTheLastElementAfterRealPersistence() {
    Tender tender = new Tender("Hamburg", "Rotterdam");
    tender.addRemark(new Remark("First remark"));
    Long id = tenderRepository.save(tender).getId();

    Tender result = tenderService.addRemark(id, "Second remark");

    assertThat(result.getRemarks()).hasSize(2);
    assertThat(result.getRemarks().get(result.getRemarks().size() - 1).getText())
        .isEqualTo("Second remark");
  }

  @Test
  void addOfferAppendsTheNewOfferAsTheLastElementAfterRealPersistence() {
    Tender tender = new Tender("Hamburg", "Rotterdam");
    tender.addOffer(new Offer("First Supplier", new BigDecimal("100.00")));
    Long id = tenderRepository.save(tender).getId();

    Tender result = tenderService.addOffer(id, "Second Supplier", new BigDecimal("200.00"));

    assertThat(result.getOffers()).hasSize(2);
    assertThat(result.getOffers().get(result.getOffers().size() - 1).getSupplierName())
        .isEqualTo("Second Supplier");
  }
}
