package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

import com.senacor.freighttenders.tender.CreateTenderRequest.AddressRequest;
import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

/** The rules of {@link TenderService#updateTender}; "today" is 2026-10-13. */
@ExtendWith(MockitoExtension.class)
class TenderServiceUpdateTest {

  private static final Clock CLOCK =
      Clock.fixed(Instant.parse("2026-10-13T08:00:00Z"), ZoneId.of("Europe/Berlin"));

  @Mock private TenderRepository tenderRepository;

  private TenderService tenderService;

  @BeforeEach
  void setUp() {
    tenderService = new TenderService(tenderRepository, CLOCK);
  }

  private void stored(Tender tender) {
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
  }

  private void savingReturnsItsArgument() {
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));
  }

  private static CreateTenderRequest request(
      LocalDate pickup, LocalDate delivery, LocalDate deadline, String commodity) {
    CreateTenderRequest base = TenderFixtures.request();
    return new CreateTenderRequest(
        base.origin(),
        base.destination(),
        pickup,
        delivery,
        deadline,
        commodity,
        base.weightKg(),
        base.loadingMeters(),
        base.palletCount(),
        base.equipmentType(),
        base.dangerousGoods(),
        base.adrClass(),
        base.temperatureControlled(),
        base.temperatureMinC(),
        base.temperatureMaxC(),
        base.currency());
  }

  private static CreateTenderRequest withCurrency(Currency currency) {
    CreateTenderRequest base = TenderFixtures.request();
    return new CreateTenderRequest(
        base.origin(),
        base.destination(),
        base.pickupDate(),
        base.deliveryDate(),
        base.bidDeadline(),
        base.commodity(),
        base.weightKg(),
        base.loadingMeters(),
        base.palletCount(),
        base.equipmentType(),
        base.dangerousGoods(),
        base.adrClass(),
        base.temperatureControlled(),
        base.temperatureMinC(),
        base.temperatureMaxC(),
        currency);
  }

  private static Tender tenderWithOffer() {
    Tender tender = TenderFixtures.tender();
    tender.addOffer(TenderFixtures.offer("Acme Logistics", new BigDecimal("100.00")));
    return tender;
  }

  @Test
  void updateTenderReplacesTheShipmentFieldsAndKeepsStatusAndRemarks() {
    Tender tender = TenderFixtures.tender();
    tender.addRemark(new Remark("Bitte schnell"));
    stored(tender);
    savingReturnsItsArgument();

    Tender result =
        tenderService.updateTender(
            1L,
            request(
                LocalDate.of(2026, 10, 21),
                LocalDate.of(2026, 10, 23),
                LocalDate.of(2026, 10, 17),
                "Gefrorene Ware"));

    assertThat(result.getCommodity()).isEqualTo("Gefrorene Ware");
    assertThat(result.getPickupDate()).isEqualTo(LocalDate.of(2026, 10, 21));
    assertThat(result.getStatus()).isEqualTo(TenderStatus.OPEN);
    assertThat(result.getRemarks()).hasSize(1);
  }

  @Test
  void updateTenderOnUnknownIdThrowsNotFoundBeforeValidating() {
    given(tenderRepository.findById(1L)).willReturn(Optional.empty());

    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    new CreateTenderRequest(
                        null, null, null, null, null, null, null, null, null, null, null, null,
                        null, null, null, null)))
        .isInstanceOf(TenderNotFoundException.class);
  }

  @Test
  void updateTenderWithInvalidBodyOnClosedTenderThrowsInvalidRatherThanClosed() {
    Tender tender = TenderFixtures.tender();
    tender.close();
    stored(tender);

    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    request(
                        LocalDate.of(2026, 10, 20),
                        LocalDate.of(2026, 10, 19),
                        LocalDate.of(2026, 10, 16),
                        "x")))
        .isInstanceOf(TenderRequestInvalidException.class)
        .satisfies(
            exception ->
                assertThat(((TenderRequestInvalidException) exception).getViolations())
                    .extracting(TenderExceptionHandler.Violation::field)
                    .containsExactly("deliveryDate"));
  }

  @Test
  void updateTenderReportsFieldRuleViolationsUnderTheirFieldNames() {
    stored(TenderFixtures.tender());

    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    new CreateTenderRequest(
                        new AddressRequest("de", "20457", "Hamburg"),
                        TenderFixtures.request().destination(),
                        LocalDate.of(2026, 10, 20),
                        LocalDate.of(2026, 10, 22),
                        LocalDate.of(2026, 10, 16),
                        " ",
                        18500,
                        new BigDecimal("13.6"),
                        33,
                        EquipmentType.CURTAIN_SIDER,
                        false,
                        null,
                        false,
                        null,
                        null,
                        Currency.EUR)))
        .isInstanceOf(TenderRequestInvalidException.class)
        .satisfies(
            exception ->
                assertThat(((TenderRequestInvalidException) exception).getViolations())
                    .extracting(TenderExceptionHandler.Violation::field)
                    .containsExactlyInAnyOrder("origin.country", "commodity"));
    verify(tenderRepository, never()).save(any(Tender.class));
  }

  @Test
  void updateTenderOnClosedOrAwardedTenderThrowsClosed() {
    Tender tender = TenderFixtures.tender();
    tender.close();
    stored(tender);

    assertThatThrownBy(() -> tenderService.updateTender(1L, TenderFixtures.request()))
        .isInstanceOf(TenderClosedException.class);
    verify(tenderRepository, never()).save(any(Tender.class));
  }

  @Test
  void updateTenderRepeatingAPastDateAcceptsItButAnotherPastDateIsRejected() {
    Tender tender =
        new Tender(
            new Address("DE", "20457", "Hamburg"),
            new Address("NL", "3011 AA", "Rotterdam"),
            LocalDate.of(2026, 10, 12),
            LocalDate.of(2026, 10, 14),
            LocalDate.of(2026, 10, 10),
            "Maschinenteile",
            18500,
            new BigDecimal("13.6"),
            33,
            EquipmentType.CURTAIN_SIDER,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    stored(tender);
    savingReturnsItsArgument();

    Tender result =
        tenderService.updateTender(
            1L,
            request(
                LocalDate.of(2026, 10, 12),
                LocalDate.of(2026, 10, 15),
                LocalDate.of(2026, 10, 10),
                "Maschinenteile"));
    assertThat(result.getDeliveryDate()).isEqualTo(LocalDate.of(2026, 10, 15));

    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    request(
                        LocalDate.of(2026, 10, 12),
                        LocalDate.of(2026, 10, 15),
                        LocalDate.of(2026, 10, 9),
                        "Maschinenteile")))
        .isInstanceOf(TenderRequestInvalidException.class)
        .satisfies(
            exception ->
                assertThat(((TenderRequestInvalidException) exception).getViolations())
                    .extracting(TenderExceptionHandler.Violation::field)
                    .containsExactly("bidDeadline"));
    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    request(
                        LocalDate.of(2026, 10, 11),
                        LocalDate.of(2026, 10, 15),
                        LocalDate.of(2026, 10, 10),
                        "Maschinenteile")))
        .isInstanceOf(TenderRequestInvalidException.class)
        .satisfies(
            exception ->
                assertThat(((TenderRequestInvalidException) exception).getViolations())
                    .extracting(TenderExceptionHandler.Violation::field)
                    .contains("pickupDate"));
  }

  @Test
  void updateTenderWithOffersAllowsChangingOnlyDeliveryDateAndBidDeadline() {
    stored(tenderWithOffer());
    savingReturnsItsArgument();

    Tender result =
        tenderService.updateTender(
            1L,
            request(
                LocalDate.of(2026, 10, 20),
                LocalDate.of(2026, 10, 25),
                LocalDate.of(2026, 10, 18),
                "Maschinenteile auf Europaletten"));

    assertThat(result.getDeliveryDate()).isEqualTo(LocalDate.of(2026, 10, 25));
    assertThat(result.getBidDeadline()).isEqualTo(LocalDate.of(2026, 10, 18));
  }

  @Test
  void updateTenderWithOffersRejectsChangedLockedFieldsNamingThem() {
    Tender tender = tenderWithOffer();
    stored(tender);

    assertThatThrownBy(() -> tenderService.updateTender(1L, withCurrency(Currency.CHF)))
        .isInstanceOf(TenderLockedFieldsException.class)
        .hasMessageContaining("currency");
    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    request(
                        LocalDate.of(2026, 10, 20),
                        LocalDate.of(2026, 10, 22),
                        LocalDate.of(2026, 10, 16),
                        "Anderes")))
        .isInstanceOf(TenderLockedFieldsException.class)
        .hasMessageContaining("commodity");
    assertThat(tender.getCurrency()).isEqualTo(Currency.EUR);
    verify(tenderRepository, never()).save(any(Tender.class));
  }

  @Test
  void updateTenderWithOffersComparesLoadingMetersByValueAndAbsentOptionalsAsNull() {
    Tender tender = tenderWithOffer();
    ReflectionTestUtils.setField(tender, "loadingMeters", new BigDecimal("13.60"));
    stored(tender);
    savingReturnsItsArgument();
    CreateTenderRequest base = TenderFixtures.request();
    CreateTenderRequest sameValues =
        new CreateTenderRequest(
            base.origin(),
            base.destination(),
            base.pickupDate(),
            base.deliveryDate(),
            base.bidDeadline(),
            base.commodity(),
            base.weightKg(),
            base.loadingMeters(),
            base.palletCount(),
            base.equipmentType(),
            false,
            null,
            false,
            null,
            null,
            base.currency());

    assertThat(tenderService.updateTender(1L, sameValues).getLoadingMeters())
        .isEqualByComparingTo("13.6");
  }

  @Test
  void updateTenderWithNoChangeSucceeds() {
    stored(TenderFixtures.tender());
    savingReturnsItsArgument();

    assertThat(tenderService.updateTender(1L, TenderFixtures.request()).getStatus())
        .isEqualTo(TenderStatus.OPEN);
  }

  @Test
  void extendingAPassedBidDeadlineMakesAddOfferSucceedAgain() {
    Tender tender =
        new Tender(
            new Address("DE", "20457", "Hamburg"),
            new Address("NL", "3011 AA", "Rotterdam"),
            LocalDate.of(2026, 10, 20),
            LocalDate.of(2026, 10, 22),
            LocalDate.of(2026, 10, 10),
            "Maschinenteile",
            18500,
            new BigDecimal("13.6"),
            33,
            EquipmentType.CURTAIN_SIDER,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    stored(tender);
    savingReturnsItsArgument();
    LocalDate delivery = LocalDate.of(2026, 10, 21);
    LocalDate validUntil = LocalDate.of(2026, 10, 30);

    assertThatThrownBy(
            () ->
                tenderService.addOffer(
                    1L, "Acme", new BigDecimal("10"), delivery, validUntil, null))
        .isInstanceOf(BidDeadlinePassedException.class);

    tenderService.updateTender(
        1L,
        request(
            LocalDate.of(2026, 10, 20),
            LocalDate.of(2026, 10, 22),
            LocalDate.of(2026, 10, 13),
            "Maschinenteile"));

    assertThat(
            tenderService
                .addOffer(1L, "Acme", new BigDecimal("10"), delivery, validUntil, null)
                .getOffers())
        .hasSize(1);
  }
}
