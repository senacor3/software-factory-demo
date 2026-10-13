package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.ActiveProfiles;

@DataJpaTest
@ActiveProfiles("demo")
@Import({TenderService.class, DemoDataSeeder.class, FixedClockConfiguration.class})
class DemoDataSeederTest {

  private static final LocalDate TODAY = LocalDate.of(2026, 10, 13);

  @Autowired private DemoDataSeeder seeder;

  @Autowired private TenderRepository tenderRepository;

  @Autowired private TenderService tenderService;

  @BeforeEach
  void seed() {
    seeder.run(null);
  }

  private List<Tender> byId() {
    return tenderRepository.findAll().stream().sorted(Comparator.comparing(Tender::getId)).toList();
  }

  @Test
  void seedsEightTendersWithTheExpectedStatuses() {
    List<Tender> tenders = byId();

    assertThat(tenders).hasSize(8);
    assertThat(tenders.stream().filter(t -> t.getStatus() == TenderStatus.OPEN)).hasSize(6);
    assertThat(tenders.stream().filter(t -> t.getStatus() == TenderStatus.AWARDED)).hasSize(1);
    assertThat(tenders.stream().filter(t -> t.getStatus() == TenderStatus.CLOSED)).hasSize(1);
  }

  @Test
  void bidDeadlinesAreRelativeToToday() {
    List<Tender> tenders = byId();

    assertThat(tenders.subList(0, 6))
        .extracting(Tender::getBidDeadline)
        .containsExactly(
            TODAY.plusDays(3),
            TODAY.plusDays(5),
            TODAY,
            TODAY.plusDays(7),
            TODAY.minusDays(1),
            TODAY.plusDays(4));
    assertThat(tenders.get(4).getOffers().stream().filter(o -> o.getValidUntil().isBefore(TODAY)))
        .hasSize(1);
  }

  @Test
  void tendersCarryTheirSpecialFields() {
    List<Tender> tenders = byId();

    Tender t1 = tenders.get(0);
    assertThat(
            t1.getOffers().stream().filter(o -> o.getDeliveryDate().isAfter(t1.getDeliveryDate())))
        .hasSize(1);
    assertThat(tenders.get(1).isTemperatureControlled()).isTrue();
    assertThat(tenders.get(1).getEquipmentType()).isEqualTo(EquipmentType.REEFER);
    assertThat(tenders.get(2).isDangerousGoods()).isTrue();
    assertThat(tenders.get(2).getAdrClass()).isEqualTo("3");
    assertThat(tenders.get(3).getPalletCount()).isNull();
    assertThat(tenders.get(5).getCurrency()).isEqualTo(Currency.CHF);
  }

  @Test
  void awardedAndClosedTendersMatchWhatTheServiceProduces() {
    List<Tender> tenders = byId();

    Tender awarded = tenders.get(6);
    assertThat(awarded.getStatus()).isEqualTo(TenderStatus.AWARDED);
    assertThat(awarded.getOffers()).hasSize(2);
    assertThat(awarded.getAwardedOffer().getAmount()).isEqualByComparingTo(new BigDecimal("1100"));

    Tender closed = tenders.get(7);
    assertThat(closed.getStatus()).isEqualTo(TenderStatus.CLOSED);
    assertThat(closed.getAwardedOffer()).isNull();
    assertThat(closed.getOffers()).hasSize(1);
    assertThat(closed.getRemarks()).hasSize(1);
  }

  @Test
  void hasRemarksAndOfferNotes() {
    List<Tender> tenders = byId();

    assertThat(tenders.stream().filter(t -> !t.getRemarks().isEmpty()).count())
        .isGreaterThanOrEqualTo(3);
    assertThat(
            tenders.stream()
                .flatMap(t -> t.getOffers().stream())
                .filter(o -> o.getNote() != null)
                .count())
        .isGreaterThanOrEqualTo(2);
  }

  @Test
  void runningAgainDoesNotSeedTwice() {
    seeder.run(null);

    assertThat(tenderRepository.count()).isEqualTo(8);
  }

  @Test
  void seededTenderWithPassedDeadlineRejectsNewOffers() {
    Long id = byId().get(4).getId();

    assertThatThrownBy(
            () ->
                tenderService.addOffer(
                    id, "Spät GmbH", new BigDecimal("100"), TODAY.plusDays(5), TODAY, null))
        .isInstanceOf(BidDeadlinePassedException.class);
  }
}
