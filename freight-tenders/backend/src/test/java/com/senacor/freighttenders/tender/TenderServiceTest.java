package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class TenderServiceTest {

  @Mock private TenderRepository tenderRepository;

  private static final Clock CLOCK =
      Clock.fixed(Instant.parse("2026-10-13T08:00:00Z"), ZoneId.of("Europe/Berlin"));

  private TenderService tenderService;

  @BeforeEach
  void setUp() {
    tenderService = new TenderService(tenderRepository, CLOCK, TenderFixtures.validator(CLOCK));
  }

  @Test
  void createTenderBuildsOpenTenderAndSavesIt() {
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result = tenderService.createTender(TenderFixtures.request());

    assertThat(result.getOrigin()).isEqualTo(new Address("DE", "20457", "Hamburg"));
    assertThat(result.getDestination()).isEqualTo(new Address("NL", "3011 AA", "Rotterdam"));
    assertThat(result.getStatus()).isEqualTo(TenderStatus.OPEN);

    ArgumentCaptor<Tender> captor = ArgumentCaptor.forClass(Tender.class);
    verify(tenderRepository).save(captor.capture());
    Tender saved = captor.getValue();
    assertThat(saved.getOrigin().city()).isEqualTo("Hamburg");
    assertThat(saved.getDestination().city()).isEqualTo("Rotterdam");
    assertThat(saved.getPickupDate()).isEqualTo(LocalDate.of(2026, 10, 20));
    assertThat(saved.getDeliveryDate()).isEqualTo(LocalDate.of(2026, 10, 22));
    assertThat(saved.getBidDeadline()).isEqualTo(LocalDate.of(2026, 10, 16));
    assertThat(saved.getCommodity()).isEqualTo("Maschinenteile auf Europaletten");
    assertThat(saved.getWeightKg()).isEqualTo(18500);
    assertThat(saved.getLoadingMeters()).isEqualTo(new BigDecimal("13.6"));
    assertThat(saved.getPalletCount()).isEqualTo(33);
    assertThat(saved.getEquipmentType()).isEqualTo(EquipmentType.CURTAIN_SIDER);
    assertThat(saved.isDangerousGoods()).isFalse();
    assertThat(saved.getAdrClass()).isNull();
    assertThat(saved.isTemperatureControlled()).isFalse();
    assertThat(saved.getCurrency()).isEqualTo(Currency.EUR);
    assertThat(saved.getStatus()).isEqualTo(TenderStatus.OPEN);
  }

  @Test
  void closeTenderClosesAndSavesTheLoadedTender() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result = tenderService.closeTender(1L);

    assertThat(result.getStatus()).isEqualTo(TenderStatus.CLOSED);
    verify(tenderRepository).save(tender);
  }

  @Test
  void addRemarkOnOpenTenderIsAddedAndSaved() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result = tenderService.addRemark(1L, "Please expedite");

    assertThat(result.getRemarks()).hasSize(1);
    assertThat(result.getRemarks().get(0).getText()).isEqualTo("Please expedite");
    verify(tenderRepository).save(tender);
  }

  @Test
  void addOfferOnOpenTenderIsAddedAndSaved() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result = addOffer(1L, LocalDate.of(2026, 10, 21));

    assertThat(result.getOffers()).hasSize(1);
    assertThat(result.getOffers().get(0).getSupplierName()).isEqualTo("Acme Logistics");
    verify(tenderRepository).save(tender);
  }

  @Test
  void addRemarkOnClosedTenderIsRejected() {
    Tender tender = TenderFixtures.tender();
    tender.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> tenderService.addRemark(1L, "Too late"))
        .isInstanceOf(TenderClosedException.class);

    assertThat(tender.getRemarks()).isEmpty();
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void addOfferOnClosedTenderIsRejected() {
    Tender tender = TenderFixtures.tender();
    tender.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> addOffer(1L, LocalDate.of(2026, 10, 21)))
        .isInstanceOf(TenderClosedException.class);

    assertThat(tender.getOffers()).isEmpty();
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void listTendersWithNoFilterDelegatesToFindAll() {
    Tender openTender = TenderFixtures.tender();
    Tender closedTender = TenderFixtures.tender("Berlin", "Munich");
    closedTender.close();
    given(tenderRepository.findAll()).willReturn(List.of(openTender, closedTender));

    List<Tender> result = tenderService.listTenders(Optional.empty());

    assertThat(result).containsExactly(openTender, closedTender);
    verify(tenderRepository, never()).findByStatus(any());
  }

  @Test
  void listTendersFilteredByStatusDelegatesToFindByStatus() {
    Tender openTender = TenderFixtures.tender();
    given(tenderRepository.findByStatus(TenderStatus.OPEN)).willReturn(List.of(openTender));

    List<Tender> result = tenderService.listTenders(Optional.of(TenderStatus.OPEN));

    assertThat(result).containsExactly(openTender);
    verify(tenderRepository, never()).findAll();
  }

  @Test
  void addOfferOnTheBidDeadlineDayAndDeliveryOnPickupDayIsAccepted() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));
    Clock deadlineDay =
        Clock.fixed(Instant.parse("2026-10-16T08:00:00Z"), ZoneId.of("Europe/Berlin"));
    TenderService service =
        new TenderService(tenderRepository, deadlineDay, TenderFixtures.validator(deadlineDay));

    Tender result =
        service.addOffer(
            1L,
            "Acme",
            new BigDecimal("1.00"),
            LocalDate.of(2026, 10, 20),
            LocalDate.of(2026, 10, 16),
            " ");

    assertThat(result.getOffers()).hasSize(1);
    assertThat(result.getOffers().get(0).getNote()).isNull();
  }

  @Test
  void addOfferTheDayAfterTheBidDeadlineIsRejectedButRemarkStillAccepted() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));
    Clock dayAfter = Clock.fixed(Instant.parse("2026-10-17T08:00:00Z"), ZoneId.of("Europe/Berlin"));
    TenderService service =
        new TenderService(tenderRepository, dayAfter, TenderFixtures.validator(dayAfter));

    assertThatThrownBy(
            () ->
                service.addOffer(
                    1L,
                    "Acme",
                    new BigDecimal("1.00"),
                    LocalDate.of(2026, 10, 21),
                    LocalDate.of(2026, 10, 30),
                    null))
        .isInstanceOf(BidDeadlinePassedException.class);
    service.addRemark(1L, "Still allowed");

    assertThat(tender.getOffers()).isEmpty();
    assertThat(tender.getRemarks()).hasSize(1);
  }

  @Test
  void addOfferOnClosedTenderWithPassedDeadlineReportsClosedNotDeadline() {
    Tender tender = TenderFixtures.tender();
    tender.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    Clock dayAfter = Clock.fixed(Instant.parse("2026-10-17T08:00:00Z"), ZoneId.of("Europe/Berlin"));
    TenderService service =
        new TenderService(tenderRepository, dayAfter, TenderFixtures.validator(dayAfter));

    assertThatThrownBy(
            () ->
                service.addOffer(
                    1L,
                    "Acme",
                    new BigDecimal("1.00"),
                    LocalDate.of(2026, 10, 21),
                    LocalDate.of(2026, 10, 30),
                    null))
        .isInstanceOf(TenderClosedException.class);
  }

  @Test
  void addOfferWithDeliveryBeforePickupIsRejected() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> addOffer(1L, LocalDate.of(2026, 10, 19)))
        .isInstanceOf(OfferDeliveryBeforePickupException.class);

    assertThat(tender.getOffers()).isEmpty();
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void awardTenderSetsAwardedStatusAndOfferAndSaves() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result = tenderService.awardTender(1L, 10L);

    assertThat(result.getStatus()).isEqualTo(TenderStatus.AWARDED);
    assertThat(result.getAwardedOffer()).isSameAs(tender.getOffers().get(0));
    verify(tenderRepository).save(tender);
  }

  @Test
  void awardTenderOnUnknownTenderIsRejected() {
    given(tenderRepository.findById(1L)).willReturn(Optional.empty());

    assertThatThrownBy(() -> tenderService.awardTender(1L, 10L))
        .isInstanceOf(TenderNotFoundException.class);
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void awardTenderWithUnknownOrForeignOfferIsRejectedAndTenderStaysOpen() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> tenderService.awardTender(1L, 99L))
        .isInstanceOf(OfferNotFoundException.class);

    assertThat(tender.getStatus()).isEqualTo(TenderStatus.OPEN);
    assertThat(tender.getAwardedOffer()).isNull();
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void awardTenderOnClosedOrAwardedTenderIsRejected() {
    Tender closed = tenderWithOffer(LocalDate.of(2026, 10, 30));
    closed.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(closed));
    assertThatThrownBy(() -> tenderService.awardTender(1L, 10L))
        .isInstanceOf(TenderClosedException.class);
    assertThat(closed.getStatus()).isEqualTo(TenderStatus.CLOSED);

    Tender awarded = tenderWithOffer(LocalDate.of(2026, 10, 30));
    awarded.award(awarded.getOffers().get(0));
    given(tenderRepository.findById(2L)).willReturn(Optional.of(awarded));
    assertThatThrownBy(() -> tenderService.awardTender(2L, 10L))
        .isInstanceOf(TenderClosedException.class);
    assertThat(awarded.getStatus()).isEqualTo(TenderStatus.AWARDED);
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void awardTenderWithExpiredOfferIsRejectedButValidUntilTodaySucceeds() {
    Tender expired = tenderWithOffer(LocalDate.of(2026, 10, 12));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(expired));

    assertThatThrownBy(() -> tenderService.awardTender(1L, 10L))
        .isInstanceOf(OfferExpiredException.class);
    assertThat(expired.getStatus()).isEqualTo(TenderStatus.OPEN);
    verify(tenderRepository, never()).save(any());

    Tender today = tenderWithOffer(LocalDate.of(2026, 10, 13));
    given(tenderRepository.findById(2L)).willReturn(Optional.of(today));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    assertThat(tenderService.awardTender(2L, 10L).getStatus()).isEqualTo(TenderStatus.AWARDED);
  }

  @Test
  void awardTenderWorksAfterTheBidDeadline() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));
    Clock dayAfter = Clock.fixed(Instant.parse("2026-10-17T08:00:00Z"), ZoneId.of("Europe/Berlin"));

    Tender result =
        new TenderService(tenderRepository, dayAfter, TenderFixtures.validator(dayAfter))
            .awardTender(1L, 10L);

    assertThat(result.getStatus()).isEqualTo(TenderStatus.AWARDED);
  }

  @Test
  void addRemarkAddOfferAndCloseOnAwardedTenderAreRejected() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    tender.award(tender.getOffers().get(0));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> tenderService.addRemark(1L, "Late"))
        .isInstanceOf(TenderClosedException.class);
    assertThatThrownBy(() -> addOffer(1L, LocalDate.of(2026, 10, 21)))
        .isInstanceOf(TenderClosedException.class);
    assertThatThrownBy(() -> tenderService.closeTender(1L))
        .isInstanceOf(TenderClosedException.class);

    assertThat(tender.getStatus()).isEqualTo(TenderStatus.AWARDED);
    assertThat(tender.getRemarks()).isEmpty();
    assertThat(tender.getOffers()).hasSize(1);
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void closeTenderOnAlreadyClosedTenderStaysClosed() {
    Tender tender = TenderFixtures.tender();
    tender.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    assertThat(tenderService.closeTender(1L).getStatus()).isEqualTo(TenderStatus.CLOSED);
  }

  @Test
  void updateTenderReplacesDataFieldsAndKeepsStatusAndRemarks() {
    Tender tender = TenderFixtures.tender();
    tender.addRemark(new Remark("Keep me"));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result =
        tenderService.updateTender(
            1L,
            requestWith(
                LocalDate.of(2026, 10, 21),
                LocalDate.of(2026, 10, 23),
                LocalDate.of(2026, 10, 17),
                "Neue Ware",
                new BigDecimal("12.0")));

    assertThat(result.getCommodity()).isEqualTo("Neue Ware");
    assertThat(result.getPickupDate()).isEqualTo(LocalDate.of(2026, 10, 21));
    assertThat(result.getLoadingMeters()).isEqualByComparingTo("12.0");
    assertThat(result.getStatus()).isEqualTo(TenderStatus.OPEN);
    assertThat(result.getRemarks()).hasSize(1);
  }

  @Test
  void updateTenderOnUnknownIdThrowsNotFound() {
    given(tenderRepository.findById(9L)).willReturn(Optional.empty());

    assertThatThrownBy(() -> tenderService.updateTender(9L, TenderFixtures.request()))
        .isInstanceOf(TenderNotFoundException.class);
  }

  @Test
  void updateTenderWithInvalidBodyOnClosedTenderThrowsInvalidNotClosed() {
    Tender tender = TenderFixtures.tender();
    tender.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    requestWith(
                        LocalDate.of(2026, 10, 20),
                        LocalDate.of(2026, 10, 19),
                        LocalDate.of(2026, 10, 16),
                        "Ware",
                        new BigDecimal("13.6"))))
        .isInstanceOf(InvalidTenderException.class);
  }

  @Test
  void updateTenderOnClosedAndAwardedTendersThrowsClosed() {
    Tender closed = TenderFixtures.tender();
    closed.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(closed));

    assertThatThrownBy(() -> tenderService.updateTender(1L, TenderFixtures.request()))
        .isInstanceOf(TenderClosedException.class);
    verify(tenderRepository, never()).save(any(Tender.class));
  }

  @Test
  void updateTenderAcceptsStoredPastBidDeadlineButRejectsAnotherPastDate() {
    Tender tender = tenderWithBidDeadline(LocalDate.of(2026, 10, 10));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result =
        tenderService.updateTender(
            1L,
            requestWith(
                LocalDate.of(2026, 10, 20),
                LocalDate.of(2026, 10, 22),
                LocalDate.of(2026, 10, 10),
                "Ware",
                new BigDecimal("13.6")));
    assertThat(result.getBidDeadline()).isEqualTo(LocalDate.of(2026, 10, 10));

    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    requestWith(
                        LocalDate.of(2026, 10, 20),
                        LocalDate.of(2026, 10, 22),
                        LocalDate.of(2026, 10, 11),
                        "Ware",
                        new BigDecimal("13.6"))))
        .isInstanceOfSatisfying(
            InvalidTenderException.class,
            exception ->
                assertThat(exception.getViolations())
                    .extracting(TenderExceptionHandler.Violation::field)
                    .containsExactly("bidDeadline"));
  }

  @Test
  void updateTenderWithOffersRejectsChangedLockedFieldsNamingThem() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(
            () ->
                tenderService.updateTender(
                    1L,
                    requestWith(
                        LocalDate.of(2026, 10, 21),
                        LocalDate.of(2026, 10, 22),
                        LocalDate.of(2026, 10, 16),
                        "Andere Ware",
                        new BigDecimal("13.6"))))
        .isInstanceOf(TenderLockedFieldsException.class)
        .hasMessageContaining("pickupDate")
        .hasMessageContaining("commodity");
    assertThat(tender.getCommodity()).isEqualTo("Maschinenteile auf Europaletten");
    verify(tenderRepository, never()).save(any(Tender.class));
  }

  @Test
  void updateTenderWithOffersAllowsDeliveryDateAndBidDeadlineChanges() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result =
        tenderService.updateTender(
            1L,
            requestWith(
                LocalDate.of(2026, 10, 20),
                LocalDate.of(2026, 10, 25),
                LocalDate.of(2026, 10, 18),
                "Maschinenteile auf Europaletten",
                new BigDecimal("13.6")));

    assertThat(result.getDeliveryDate()).isEqualTo(LocalDate.of(2026, 10, 25));
    assertThat(result.getBidDeadline()).isEqualTo(LocalDate.of(2026, 10, 18));
  }

  private static CreateTenderRequest requestWith(
      LocalDate pickup,
      LocalDate delivery,
      LocalDate deadline,
      String commodity,
      BigDecimal loadingMeters) {
    CreateTenderRequest base = TenderFixtures.request();
    return new CreateTenderRequest(
        base.origin(),
        base.destination(),
        pickup,
        delivery,
        deadline,
        commodity,
        base.weightKg(),
        loadingMeters,
        base.palletCount(),
        base.equipmentType(),
        base.dangerousGoods(),
        base.adrClass(),
        base.temperatureControlled(),
        base.temperatureMinC(),
        base.temperatureMaxC(),
        base.currency());
  }

  private static Tender tenderWithBidDeadline(LocalDate bidDeadline) {
    Tender tender = TenderFixtures.tender();
    tender.update(
        tender.getOrigin(),
        tender.getDestination(),
        tender.getPickupDate(),
        tender.getDeliveryDate(),
        bidDeadline,
        tender.getCommodity(),
        tender.getWeightKg(),
        tender.getLoadingMeters(),
        tender.getPalletCount(),
        tender.getEquipmentType(),
        tender.isDangerousGoods(),
        tender.getAdrClass(),
        tender.isTemperatureControlled(),
        tender.getTemperatureMinC(),
        tender.getTemperatureMaxC(),
        tender.getCurrency());
    return tender;
  }

  private static Tender tenderWithOffer(LocalDate validUntil) {
    Tender tender = TenderFixtures.tender();
    Offer offer =
        new Offer("Acme", new BigDecimal("100.00"), LocalDate.of(2026, 10, 21), validUntil, null);
    ReflectionTestUtils.setField(offer, "id", 10L);
    tender.addOffer(offer);
    return tender;
  }

  private Tender addOffer(Long id, LocalDate deliveryDate) {
    return tenderService.addOffer(
        id,
        "Acme Logistics",
        new BigDecimal("1234.56"),
        deliveryDate,
        LocalDate.of(2026, 10, 30),
        null);
  }
}
