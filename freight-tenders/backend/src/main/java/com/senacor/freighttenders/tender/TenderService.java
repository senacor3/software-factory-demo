package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validator;
import java.math.BigDecimal;
import java.time.Clock;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Comparator;
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

  /**
   * Replaces the data fields of an open tender. Checks run in this order: unknown id (404), invalid
   * body (400), tender not open (409), locked fields changed on a tender with offers (409).
   */
  public Tender updateTender(Long id, CreateTenderRequest request) {
    Tender tender = getTenderOrThrow(id);
    validateUpdate(tender, request);
    rejectIfClosed(tender);
    if (!tender.getOffers().isEmpty()) {
      List<String> changed = changedLockedFields(tender, request);
      if (!changed.isEmpty()) {
        throw new TenderLockedFieldsException(tender.getId(), changed);
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

  private void validateUpdate(Tender tender, CreateTenderRequest request) {
    List<Violation> violations = new ArrayList<>();
    // The class-level constraint is skipped: it would reject any stored past date, so the same
    // rules are evaluated below with the stored dates exempt.
    for (ConstraintViolation<CreateTenderRequest> violation : validator.validate(request)) {
      if (violation.getConstraintDescriptor().getAnnotation() instanceof ValidCreateTenderRequest) {
        continue;
      }
      violations.add(new Violation(violation.getPropertyPath().toString(), violation.getMessage()));
    }
    violations.sort(Comparator.comparing(Violation::field).thenComparing(Violation::message));
    violations.addAll(
        CreateTenderRequestValidator.check(
            request, LocalDate.now(clock), tender.getPickupDate(), tender.getBidDeadline()));
    if (!violations.isEmpty()) {
      throw new InvalidTenderException(violations);
    }
  }

  private static List<String> changedLockedFields(Tender tender, CreateTenderRequest request) {
    List<String> changed = new ArrayList<>();
    addIfDifferent(changed, "origin", tender.getOrigin(), request.origin().toAddress());
    addIfDifferent(
        changed, "destination", tender.getDestination(), request.destination().toAddress());
    addIfDifferent(changed, "pickupDate", tender.getPickupDate(), request.pickupDate());
    addIfDifferent(changed, "commodity", tender.getCommodity(), request.commodity());
    addIfDifferent(changed, "weightKg", tender.getWeightKg(), request.weightKg());
    if (compareDecimals(tender.getLoadingMeters(), request.loadingMeters()) != 0) {
      changed.add("loadingMeters");
    }
    addIfDifferent(changed, "palletCount", tender.getPalletCount(), request.palletCount());
    addIfDifferent(changed, "equipmentType", tender.getEquipmentType(), request.equipmentType());
    addIfDifferent(changed, "dangerousGoods", tender.isDangerousGoods(), request.dangerousGoods());
    addIfDifferent(changed, "adrClass", tender.getAdrClass(), request.adrClass());
    addIfDifferent(
        changed,
        "temperatureControlled",
        tender.isTemperatureControlled(),
        request.temperatureControlled());
    addIfDifferent(
        changed, "temperatureMinC", tender.getTemperatureMinC(), request.temperatureMinC());
    addIfDifferent(
        changed, "temperatureMaxC", tender.getTemperatureMaxC(), request.temperatureMaxC());
    addIfDifferent(changed, "currency", tender.getCurrency(), request.currency());
    return changed;
  }

  private static void addIfDifferent(
      List<String> changed, String field, Object stored, Object requested) {
    if (!Objects.equals(stored, requested)) {
      changed.add(field);
    }
  }

  private static int compareDecimals(BigDecimal stored, BigDecimal requested) {
    if (stored == null || requested == null) {
      return stored == requested ? 0 : 1;
    }
    return stored.compareTo(requested);
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
