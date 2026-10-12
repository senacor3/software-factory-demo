package com.senacor.freighttenders.tender;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;

import java.math.BigDecimal;
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

    Tender result = tenderService.createTender("Hamburg", "Rotterdam");

    assertThat(result.getOrigin()).isEqualTo("Hamburg");
    assertThat(result.getDestination()).isEqualTo("Rotterdam");
    assertThat(result.getStatus()).isEqualTo(TenderStatus.OPEN);

    ArgumentCaptor<Tender> captor = ArgumentCaptor.forClass(Tender.class);
    verify(tenderRepository).save(captor.capture());
    assertThat(captor.getValue().getOrigin()).isEqualTo("Hamburg");
    assertThat(captor.getValue().getDestination()).isEqualTo("Rotterdam");
    assertThat(captor.getValue().getStatus()).isEqualTo(TenderStatus.OPEN);
  }

  @Test
  void closeTenderClosesAndSavesTheLoadedTender() {
    Tender tender = new Tender("Hamburg", "Rotterdam");
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));
    given(tenderRepository.save(any(Tender.class)))
        .willAnswer(invocation -> invocation.getArgument(0));

    Tender result = tenderService.closeTender(1L);

    assertThat(result.getStatus()).isEqualTo(TenderStatus.CLOSED);
    verify(tenderRepository).save(tender);
  }

  @Test
  void addRemarkOnOpenTenderIsAddedAndSaved() {
    Tender tender = new Tender("Hamburg", "Rotterdam");
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
    Tender tender = new Tender("Hamburg", "Rotterdam");
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
    Tender tender = new Tender("Hamburg", "Rotterdam");
    tender.close();
    given(tenderRepository.findById(1L)).willReturn(Optional.of(tender));

    assertThatThrownBy(() -> tenderService.addRemark(1L, "Too late"))
        .isInstanceOf(TenderClosedException.class);

    assertThat(tender.getRemarks()).isEmpty();
    verify(tenderRepository, never()).save(any());
  }

  @Test
  void addOfferOnClosedTenderIsRejected() {
    Tender tender = new Tender("Hamburg", "Rotterdam");
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
    Tender openTender = new Tender("Hamburg", "Rotterdam");
    Tender closedTender = new Tender("Berlin", "Munich");
    closedTender.close();
    given(tenderRepository.findAll()).willReturn(List.of(openTender, closedTender));

    List<Tender> result = tenderService.listTenders(Optional.empty());

    assertThat(result).containsExactly(openTender, closedTender);
    verify(tenderRepository, never()).findByStatus(any());
  }

  @Test
  void listTendersFilteredByStatusDelegatesToFindByStatus() {
    Tender openTender = new Tender("Hamburg", "Rotterdam");
    given(tenderRepository.findByStatus(TenderStatus.OPEN)).willReturn(List.of(openTender));

    List<Tender> result = tenderService.listTenders(Optional.of(TenderStatus.OPEN));

    assertThat(result).containsExactly(openTender);
    verify(tenderRepository, never()).findAll();
  }
}
