package com.senacor.freighttenders.tender;

import java.math.BigDecimal;
import java.time.Clock;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;

/**
 * Owns the tender lifecycle and the open/closed invariant: {@link #addRemark} and {@link #addOffer}
 * reject a closed tender with a {@link TenderClosedException} rather than letting {@link Tender}'s
 * plain mutators silently accept it (see {@link Tender}'s own class doc).
 */
@Service
public class TenderService {

  private final TenderRepository tenderRepository;

  private final Clock clock;

  public TenderService(TenderRepository tenderRepository, Clock clock) {
    this.tenderRepository = tenderRepository;
    this.clock = clock;
  }

  public Tender createTender(CreateTenderRequest request) {
    return tenderRepository.save(
        new Tender(
            request.origin().toAddress(),
            request.destination().toAddress(),
            request.pickupDate(),
            request.deliveryDate(),
            request.bidDeadline(),
            request.commodity(),
            request.weightKg(),
            request.loadingMeters(),
            request.palletCount(),
            request.equipmentType(),
            request.dangerousGoods(),
            request.adrClass(),
            request.temperatureControlled(),
            request.temperatureMinC(),
            request.temperatureMaxC(),
            request.currency()));
  }

  public Tender closeTender(Long id) {
    Tender tender = getTenderOrThrow(id);
    tender.close();
    return tenderRepository.save(tender);
  }

  public Tender addRemark(Long id, String text) {
    Tender tender = getTenderOrThrow(id);
    rejectIfClosed(tender);
    tender.addRemark(new Remark(text));
    return tenderRepository.save(tender);
  }

  public Tender addOffer(
      Long id,
      String supplierName,
      BigDecimal amount,
      LocalDate deliveryDate,
      LocalDate validUntil,
      String note) {
    Tender tender = getTenderOrThrow(id);
    rejectIfClosed(tender);
    if (tender.getBidDeadline().isBefore(LocalDate.now(clock))) {
      throw new BidDeadlinePassedException(tender.getId());
    }
    if (deliveryDate.isBefore(tender.getPickupDate())) {
      throw new OfferDeliveryBeforePickupException(tender.getId());
    }
    tender.addOffer(new Offer(supplierName, amount, deliveryDate, validUntil, note));
    return tenderRepository.save(tender);
  }

  public Tender getTender(Long id) {
    return getTenderOrThrow(id);
  }

  public List<Tender> listTenders(Optional<TenderStatus> status) {
    return status.map(tenderRepository::findByStatus).orElseGet(tenderRepository::findAll);
  }

  private Tender getTenderOrThrow(Long id) {
    return tenderRepository.findById(id).orElseThrow(() -> new TenderNotFoundException(id));
  }

  private void rejectIfClosed(Tender tender) {
    if (tender.getStatus() == TenderStatus.CLOSED) {
      throw new TenderClosedException(tender.getId());
    }
  }
}
