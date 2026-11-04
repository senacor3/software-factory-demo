package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validator;
import java.math.BigDecimal;
import java.time.Clock;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
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

  private final Validator validator;

  public TenderService(TenderRepository tenderRepository, Clock clock, Validator validator) {
    this.tenderRepository = tenderRepository;
    this.clock = clock;
    this.validator = validator;
  }

  /**
   * Replaces the data of an open tender. Check order: 404, 400, 409 (not open), 409 (locked fields
   * of a tender with offers). Dates in the past are accepted only when equal to the stored value.
   */
  public Tender updateTender(Long id, CreateTenderRequest request) {
    Tender tender = getTenderOrThrow(id);
    List<Violation> violations = new ArrayList<>();
    for (ConstraintViolation<CreateTenderRequest> violation : validator.validate(request)) {
      // The class-level constraint applies the create-only "today" rules; they are re-run below.
      if (!(violation.getConstraintDescriptor().getAnnotation()
          instanceof ValidCreateTenderRequest)) {
        violations.add(
            new Violation(violation.getPropertyPath().toString(), violation.getMessage()));
      }
    }
    violations.addAll(CreateTenderRules.check(request, LocalDate.now(clock), tender));
    if (!violations.isEmpty()) {
      throw new TenderValidationException(violations);
    }
    rejectIfClosed(tender);
    if (!tender.getOffers().isEmpty()) {
      List<String> locked = differingLockedFields(tender, request);
      if (!locked.isEmpty()) {
        throw new TenderFieldsLockedException(id, locked);
      }
    }
    tender.update(
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
        request.currency());
    return tenderRepository.save(tender);
  }

  private static List<String> differingLockedFields(Tender tender, CreateTenderRequest request) {
    List<String> fields = new ArrayList<>();
    if (!Objects.equals(tender.getOrigin(), request.origin().toAddress())) {
      fields.add("origin");
    }
    if (!Objects.equals(tender.getDestination(), request.destination().toAddress())) {
      fields.add("destination");
    }
    if (!Objects.equals(tender.getPickupDate(), request.pickupDate())) {
      fields.add("pickupDate");
    }
    if (!Objects.equals(tender.getCommodity(), request.commodity())) {
      fields.add("commodity");
    }
    if (!Objects.equals(tender.getWeightKg(), request.weightKg())) {
      fields.add("weightKg");
    }
    if (tender.getLoadingMeters() == null
        ? request.loadingMeters() != null
        : request.loadingMeters() == null
            || tender.getLoadingMeters().compareTo(request.loadingMeters()) != 0) {
      fields.add("loadingMeters");
    }
    if (!Objects.equals(tender.getPalletCount(), request.palletCount())) {
      fields.add("palletCount");
    }
    if (tender.getEquipmentType() != request.equipmentType()) {
      fields.add("equipmentType");
    }
    if (tender.isDangerousGoods() != Boolean.TRUE.equals(request.dangerousGoods())) {
      fields.add("dangerousGoods");
    }
    if (!Objects.equals(tender.getAdrClass(), request.adrClass())) {
      fields.add("adrClass");
    }
    if (tender.isTemperatureControlled() != Boolean.TRUE.equals(request.temperatureControlled())) {
      fields.add("temperatureControlled");
    }
    if (!Objects.equals(tender.getTemperatureMinC(), request.temperatureMinC())) {
      fields.add("temperatureMinC");
    }
    if (!Objects.equals(tender.getTemperatureMaxC(), request.temperatureMaxC())) {
      fields.add("temperatureMaxC");
    }
    if (tender.getCurrency() != request.currency()) {
      fields.add("currency");
    }
    return fields;
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
    if (tender.getStatus() == TenderStatus.AWARDED) {
      throw new TenderClosedException(tender.getId(), tender.getStatus());
    }
    tender.close();
    return tenderRepository.save(tender);
  }

  public Tender awardTender(Long tenderId, Long offerId) {
    Tender tender = getTenderOrThrow(tenderId);
    Offer offer =
        tender.getOffers().stream()
            .filter(candidate -> offerId.equals(candidate.getId()))
            .findFirst()
            .orElseThrow(() -> new OfferNotFoundException(tenderId, offerId));
    rejectIfClosed(tender);
    if (offer.getValidUntil().isBefore(LocalDate.now(clock))) {
      throw new OfferExpiredException(offerId);
    }
    tender.award(offer);
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
    if (tender.getStatus() != TenderStatus.OPEN) {
      throw new TenderClosedException(tender.getId(), tender.getStatus());
    }
  }
}
