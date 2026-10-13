package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class TenderServiceTest {

  @Mock private TenderRepository tenderRepository;

  private TenderService tenderService;

  @BeforeEach
  void setUp() {
    tenderService = new TenderService(tenderRepository);
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

    Tender result = tenderService.addOffer(1L, "Acme Logistics", new BigDecimal("1234.56"));

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

    assertThatThrownBy(
            () -> tenderService.addOffer(1L, "Acme Logistics", new BigDecimal("1234.56")))
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
}
