package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.boot.jpa.test.autoconfigure.TestEntityManager;

@DataJpaTest
class TenderRepositoryTest {

  @Autowired private TenderRepository tenderRepository;

  @Autowired private TestEntityManager entityManager;

  @Test
  void fullLifecycleRoundTripsThroughClose() {
    Tender tender = new Tender("Hamburg", "Rotterdam");
    tender.addRemark(new Remark("Please expedite"));
    tender.addOffer(new Offer("Acme Logistics", new BigDecimal("1234.56")));
    tender.close();

    Long id = tenderRepository.save(tender).getId();
    entityManager.flush();
    entityManager.clear();

    Tender reloaded = tenderRepository.findById(id).orElseThrow();

    assertThat(reloaded.getStatus()).isEqualTo(TenderStatus.CLOSED);
    assertThat(reloaded.getRemarks()).hasSize(1);
    assertThat(reloaded.getRemarks().get(0).getText()).isEqualTo("Please expedite");
    assertThat(reloaded.getRemarks().get(0).getTender().getId()).isEqualTo(reloaded.getId());
    assertThat(reloaded.getOffers()).hasSize(1);
    assertThat(reloaded.getOffers().get(0).getSupplierName()).isEqualTo("Acme Logistics");
    assertThat(reloaded.getOffers().get(0).getAmount()).isEqualTo(new BigDecimal("1234.56"));
    assertThat(reloaded.getOffers().get(0).getTender().getId()).isEqualTo(reloaded.getId());
  }

  @Test
  void newTenderWithNoRemarksOrOffersReloadsOpenAndEmpty() {
    Tender tender = new Tender("Berlin", "Munich");

    Long id = tenderRepository.save(tender).getId();
    entityManager.flush();
    entityManager.clear();

    Tender reloaded = tenderRepository.findById(id).orElseThrow();

    assertThat(reloaded.getStatus()).isEqualTo(TenderStatus.OPEN);
    assertThat(reloaded.getRemarks()).isEmpty();
    assertThat(reloaded.getOffers()).isEmpty();
  }
}
