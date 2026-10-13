package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.time.LocalDate;
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
    Tender tender = TenderFixtures.tender();
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
    Tender tender = TenderFixtures.tender("Berlin", "Munich");

    Long id = tenderRepository.save(tender).getId();
    entityManager.flush();
    entityManager.clear();

    Tender reloaded = tenderRepository.findById(id).orElseThrow();

    assertThat(reloaded.getStatus()).isEqualTo(TenderStatus.OPEN);
    assertThat(reloaded.getRemarks()).isEmpty();
    assertThat(reloaded.getOffers()).isEmpty();
  }

  @Test
  void embeddedAddressesAndEveryShipmentFieldRoundTrip() {
    Tender tender =
        new Tender(
            new Address("DE", "20457", "Hamburg"),
            new Address("NL", "3011 AA", "Rotterdam"),
            LocalDate.of(2026, 10, 20),
            LocalDate.of(2026, 10, 22),
            LocalDate.of(2026, 10, 16),
            "Tiefkühlware",
            12000,
            new BigDecimal("7.5"),
            null,
            EquipmentType.REEFER,
            true,
            "4.1",
            true,
            -18,
            -10,
            Currency.CHF);

    Long id = tenderRepository.save(tender).getId();
    entityManager.flush();
    entityManager.clear();

    Tender reloaded = tenderRepository.findById(id).orElseThrow();

    assertThat(reloaded.getOrigin()).isEqualTo(new Address("DE", "20457", "Hamburg"));
    assertThat(reloaded.getDestination()).isEqualTo(new Address("NL", "3011 AA", "Rotterdam"));
    assertThat(reloaded.getPickupDate()).isEqualTo(LocalDate.of(2026, 10, 20));
    assertThat(reloaded.getDeliveryDate()).isEqualTo(LocalDate.of(2026, 10, 22));
    assertThat(reloaded.getBidDeadline()).isEqualTo(LocalDate.of(2026, 10, 16));
    assertThat(reloaded.getCommodity()).isEqualTo("Tiefkühlware");
    assertThat(reloaded.getWeightKg()).isEqualTo(12000);
    assertThat(reloaded.getLoadingMeters()).isEqualByComparingTo("7.5");
    assertThat(reloaded.getPalletCount()).isNull();
    assertThat(reloaded.getEquipmentType()).isEqualTo(EquipmentType.REEFER);
    assertThat(reloaded.isDangerousGoods()).isTrue();
    assertThat(reloaded.getAdrClass()).isEqualTo("4.1");
    assertThat(reloaded.isTemperatureControlled()).isTrue();
    assertThat(reloaded.getTemperatureMinC()).isEqualTo(-18);
    assertThat(reloaded.getTemperatureMaxC()).isEqualTo(-10);
    assertThat(reloaded.getCurrency()).isEqualTo(Currency.CHF);
  }
}
