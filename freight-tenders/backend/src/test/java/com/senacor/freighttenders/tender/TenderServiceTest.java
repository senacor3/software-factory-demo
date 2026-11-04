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

  private static final jakarta.validation.Validator VALIDATOR =
      jakarta.validation.Validation.buildDefaultValidatorFactory().getValidator();

  private TenderService tenderService;

  @BeforeEach
  void setUp() {
    tenderService = new TenderService(tenderRepository, CLOCK, VALIDATOR);
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
    TenderService service = new TenderService(tenderRepository, deadlineDay, VALIDATOR);

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
    TenderService service = new TenderService(tenderRepository, dayAfter, VALIDATOR);

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
    TenderService service = new TenderService(tenderRepository, dayAfter, VALIDATOR);

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

    Tender result = new TenderService(tenderRepository, dayAfter, VALIDATOR).awardTender(1L, 10L);

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
  void updateTenderReplacesDataAndKeepsIdStatusAndRemarks() {
    Tender tender = TenderFixtures.tender();
    ReflectionTestUtils.setField(tender, "id", 1L);
    tender.addRemark(new Remark("keep me"));
    givenStoredAndSave(tender);

    Tender result =
        tenderService.updateTender(
            1L,
            new CreateTenderRequest(
                new CreateTenderRequest.AddressRequest("DE", "10115", "Berlin"),
                new CreateTenderRequest.AddressRequest("NL", "3011 AA", "Rotterdam"),
                LocalDate.of(2026, 10, 21),
                LocalDate.of(2026, 10, 23),
                LocalDate.of(2026, 10, 17),
                "Neue Ware",
                1000,
                new BigDecimal("5.5"),
                null,
                EquipmentType.REEFER,
                true,
                "3",
                true,
                -5,
                5,
                Currency.EUR));

    assertThat(result.getId()).isEqualTo(1L);
    assertThat(result.getStatus()).isEqualTo(TenderStatus.OPEN);
    assertThat(result.getRemarks()).hasSize(1);
    assertThat(result.getOrigin().city()).isEqualTo("Berlin");
    assertThat(result.getPickupDate()).isEqualTo(LocalDate.of(2026, 10, 21));
    assertThat(result.getCommodity()).isEqualTo("Neue Ware");
    assertThat(result.getPalletCount()).isNull();
    assertThat(result.isDangerousGoods()).isTrue();
    assertThat(result.getAdrClass()).isEqualTo("3");
    assertThat(result.getTemperatureMinC()).isEqualTo(-5);
    verify(tenderRepository).save(tender);
  }

  @Test
  void updateTenderWithUnchangedDataSucceeds() {
    Tender tender = TenderFixtures.tender();
    givenStoredAndSave(tender);

    assertThat(tenderService.updateTender(1L, TenderFixtures.request()).getCommodity())
        .isEqualTo("Maschinenteile auf Europaletten");
  }

  @Test
  void updateTenderOnUnknownIdThrowsNotFoundEvenForInvalidBody() {
    given(tenderRepository.findById(99L)).willReturn(Optional.empty());
    CreateTenderRequest invalid = requestWithCommodity("");

    assertThatThrownBy(() -> tenderService.updateTender(99L, invalid))
        .isInstanceOf(TenderNotFoundException.class);
  }

  @Test
  void updateTenderWithBlankCommodityIsRejectedAndLeavesTenderUnchanged() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThat(violationFields(requestWithCommodity(" "))).contains("commodity");
    assertThat(tender.getCommodity()).isEqualTo("Maschinenteile auf Europaletten");
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void updateTenderRejectsEachCrossFieldRule() {
    Tender tender = TenderFixtures.tender();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    LocalDate pickup = LocalDate.of(2026, 10, 20);
    LocalDate deliver = LocalDate.of(2026, 10, 22);
    LocalDate deadline = LocalDate.of(2026, 10, 16);

    LocalDate early = LocalDate.of(2026, 10, 19);
    LocalDate late = LocalDate.of(2026, 10, 21);

    assertThat(rejected(pickup, early, deadline, false, null, false, null, null))
        .contains("deliveryDate");
    assertThat(rejected(pickup, deliver, late, false, null, false, null, null))
        .contains("bidDeadline");
    assertThat(rejected(pickup, deliver, deadline, true, null, false, null, null))
        .contains("adrClass");
    assertThat(rejected(pickup, deliver, deadline, false, "3", false, null, null))
        .contains("adrClass");
    assertThat(rejected(pickup, deliver, deadline, false, null, true, null, null))
        .contains("equipmentType", "temperatureMinC", "temperatureMaxC");
    assertThat(rejected(pickup, deliver, deadline, false, null, true, 9, 1))
        .contains("temperatureMinC", "temperatureMaxC");
    assertThat(rejected(pickup, deliver, deadline, false, null, false, 1, 2))
        .contains("temperatureMinC", "temperatureMaxC");
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void updateTenderAcceptsPastDatesEqualToStoredValuesButNotChangedOnes() {
    Tender tender =
        new Tender(
            new Address("DE", "20457", "Hamburg"),
            new Address("NL", "3011 AA", "Rotterdam"),
            LocalDate.of(2026, 10, 10),
            LocalDate.of(2026, 10, 12),
            LocalDate.of(2026, 10, 5),
            "Maschinenteile auf Europaletten",
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
    givenStoredAndSave(tender);

    CreateTenderRequest same =
        requestWith(
            LocalDate.of(2026, 10, 10),
            LocalDate.of(2026, 10, 12),
            LocalDate.of(2026, 10, 5),
            false,
            null,
            false,
            null,
            null);
    assertThat(tenderService.updateTender(1L, same)).isSameAs(tender);

    assertThat(
            violationFields(
                requestWith(
                    LocalDate.of(2026, 10, 11),
                    LocalDate.of(2026, 10, 12),
                    LocalDate.of(2026, 10, 5),
                    false,
                    null,
                    false,
                    null,
                    null)))
        .containsExactly("pickupDate");
    assertThat(
            violationFields(
                requestWith(
                    LocalDate.of(2026, 10, 10),
                    LocalDate.of(2026, 10, 12),
                    LocalDate.of(2026, 10, 6),
                    false,
                    null,
                    false,
                    null,
                    null)))
        .containsExactly("bidDeadline");
  }

  @Test
  void updateTenderOnClosedOrAwardedTenderIsRejectedWithConflict() {
    Tender closed = TenderFixtures.tender();
    closed.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(closed));

    assertThatThrownBy(() -> tenderService.updateTender(1L, TenderFixtures.request()))
        .isInstanceOf(TenderClosedException.class);

    Tender awarded = tenderWithOffer(LocalDate.of(2026, 10, 30));
    awarded.award(awarded.getOffers().get(0));
    given(tenderRepository.findById(2L)).willReturn(Optional.of(awarded));
    assertThatThrownBy(() -> tenderService.updateTender(2L, TenderFixtures.request()))
        .isInstanceOf(TenderClosedException.class);
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void updateTenderWithInvalidBodyOnClosedTenderReturnsValidationNotConflict() {
    Tender closed = TenderFixtures.tender();
    closed.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(closed));

    assertThatThrownBy(() -> tenderService.updateTender(1L, requestWithCommodity("")))
        .isInstanceOf(TenderValidationException.class);
  }

  @Test
  void updateTenderWithOffersAllowsChangingOnlyDeliveryDateAndBidDeadline() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    givenStoredAndSave(tender);

    Tender result =
        tenderService.updateTender(
            1L,
            requestWith(
                LocalDate.of(2026, 10, 20),
                LocalDate.of(2026, 10, 25),
                LocalDate.of(2026, 10, 18),
                false,
                null,
                false,
                null,
                null));

    assertThat(result.getDeliveryDate()).isEqualTo(LocalDate.of(2026, 10, 25));
    assertThat(result.getBidDeadline()).isEqualTo(LocalDate.of(2026, 10, 18));
  }

  @Test
  void updateTenderWithOffersRejectsChangedLockedFieldsNamingThem() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 30));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> tenderService.updateTender(1L, requestWithCommodity("Andere Ware")))
        .isInstanceOf(TenderFieldsLockedException.class)
        .hasMessageContaining("commodity");

    CreateTenderRequest base = TenderFixtures.request();
    CreateTenderRequest otherCurrency =
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
            base.dangerousGoods(),
            base.adrClass(),
            base.temperatureControlled(),
            base.temperatureMinC(),
            base.temperatureMaxC(),
            Currency.values()[(base.currency().ordinal() + 1) % Currency.values().length]);
    assertThatThrownBy(() -> tenderService.updateTender(1L, otherCurrency))
        .isInstanceOf(TenderFieldsLockedException.class)
        .hasMessageContaining("currency");

    CreateTenderRequest otherOrigin =
        new CreateTenderRequest(
            new CreateTenderRequest.AddressRequest("DE", "20457", "Bremen"),
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
            base.currency());
    assertThatThrownBy(() -> tenderService.updateTender(1L, otherOrigin))
        .isInstanceOf(TenderFieldsLockedException.class)
        .hasMessageContaining("origin");
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void updateTenderWithOffersTreatsEqualValuesAsUnchanged() {
    Tender tender =
        new Tender(
            new Address("DE", "20457", "Hamburg"),
            new Address("NL", "3011 AA", "Rotterdam"),
            LocalDate.of(2026, 10, 20),
            LocalDate.of(2026, 10, 22),
            LocalDate.of(2026, 10, 16),
            "Maschinenteile auf Europaletten",
            18500,
            new BigDecimal("13.60"),
            null,
            EquipmentType.CURTAIN_SIDER,
            false,
            null,
            false,
            null,
            null,
            Currency.EUR);
    tender.addOffer(TenderFixtures.offer("Acme", new BigDecimal("100.00")));
    givenStoredAndSave(tender);
    CreateTenderRequest base = TenderFixtures.request();

    // loadingMeters 13.6 vs stored 13.60, palletCount absent vs stored null
    Tender result =
        tenderService.updateTender(
            1L,
            new CreateTenderRequest(
                base.origin(),
                base.destination(),
                base.pickupDate(),
                base.deliveryDate(),
                base.bidDeadline(),
                base.commodity(),
                base.weightKg(),
                new BigDecimal("13.6"),
                null,
                base.equipmentType(),
                base.dangerousGoods(),
                null,
                base.temperatureControlled(),
                null,
                null,
                base.currency()));

    assertThat(result).isSameAs(tender);
  }

  @Test
  void updateTenderWithOnlyExpiredOffersIsStillLocked() {
    Tender tender = tenderWithOffer(LocalDate.of(2026, 10, 1));
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> tenderService.updateTender(1L, requestWithCommodity("Andere Ware")))
        .isInstanceOf(TenderFieldsLockedException.class);
  }

  @Test
  void extendingAPassedBidDeadlineMakesAddOfferWorkAgain() {
    Tender tender =
        new Tender(
            new Address("DE", "20457", "Hamburg"),
            new Address("NL", "3011 AA", "Rotterdam"),
            LocalDate.of(2026, 10, 20),
            LocalDate.of(2026, 10, 22),
            LocalDate.of(2026, 10, 10),
            "Maschinenteile auf Europaletten",
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
    givenStoredAndSave(tender);

    assertThatThrownBy(() -> addOffer(1L, LocalDate.of(2026, 10, 21)))
        .isInstanceOf(BidDeadlinePassedException.class);

    tenderService.updateTender(
        1L,
        requestWith(
            LocalDate.of(2026, 10, 20),
            LocalDate.of(2026, 10, 22),
            LocalDate.of(2026, 10, 13),
            false,
            null,
            false,
            null,
            null));

    assertThat(addOffer(1L, LocalDate.of(2026, 10, 21)).getOffers()).hasSize(1);
  }

  private void givenStoredAndSave(Tender tender) {
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));
  }

  private List<String> rejected(
      LocalDate pickup,
      LocalDate delivery,
      LocalDate deadline,
      boolean dangerousGoods,
      String adrClass,
      boolean temperatureControlled,
      Integer minC,
      Integer maxC) {
    return violationFields(
        requestWith(
            pickup,
            delivery,
            deadline,
            dangerousGoods,
            adrClass,
            temperatureControlled,
            minC,
            maxC));
  }

  private List<String> violationFields(CreateTenderRequest request) {
    try {
      tenderService.updateTender(1L, request);
    } catch (TenderValidationException exception) {
      return exception.getViolations().stream()
          .map(TenderExceptionHandler.Violation::field)
          .toList();
    }
    return List.of();
  }

  private static CreateTenderRequest requestWithCommodity(String commodity) {
    CreateTenderRequest base = TenderFixtures.request();
    return new CreateTenderRequest(
        base.origin(),
        base.destination(),
        base.pickupDate(),
        base.deliveryDate(),
        base.bidDeadline(),
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

  private static CreateTenderRequest requestWith(
      LocalDate pickup,
      LocalDate delivery,
      LocalDate deadline,
      boolean dangerousGoods,
      String adrClass,
      boolean temperatureControlled,
      Integer minC,
      Integer maxC) {
    CreateTenderRequest base = TenderFixtures.request();
    return new CreateTenderRequest(
        base.origin(),
        base.destination(),
        pickup,
        delivery,
        deadline,
        base.commodity(),
        base.weightKg(),
        base.loadingMeters(),
        base.palletCount(),
        base.equipmentType(),
        dangerousGoods,
        adrClass,
        temperatureControlled,
        minC,
        maxC,
        base.currency());
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
