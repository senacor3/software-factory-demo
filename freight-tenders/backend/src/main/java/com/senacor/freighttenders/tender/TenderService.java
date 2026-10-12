package com.senacor.freighttenders.tender;

import java.math.BigDecimal;
import org.springframework.stereotype.Service;

/**
 * Owns the tender lifecycle and the open/closed invariant: {@link #addRemark} and {@link #addOffer}
 * reject a closed tender with a {@link TenderClosedException} rather than letting {@link Tender}'s
 * plain mutators silently accept it (see {@link Tender}'s own class doc).
 */
@Service
public class TenderService {

  private final TenderRepository tenderRepository;

  public TenderService(TenderRepository tenderRepository) {
    this.tenderRepository = tenderRepository;
  }

  public Tender createTender(String origin, String destination) {
    return tenderRepository.save(new Tender(origin, destination));
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

  public Tender addOffer(Long id, String supplierName, BigDecimal amount) {
    Tender tender = getTenderOrThrow(id);
    rejectIfClosed(tender);
    tender.addOffer(new Offer(supplierName, amount));
    return tenderRepository.save(tender);
  }

  private Tender getTenderOrThrow(Long id) {
    return tenderRepository
        .findById(id)
        .orElseThrow(() -> new IllegalArgumentException("No tender found with id " + id));
  }

  private void rejectIfClosed(Tender tender) {
    if (tender.getStatus() == TenderStatus.CLOSED) {
      throw new TenderClosedException(tender.getId());
    }
  }
}
