package com.senacor.freighttenders.tender;

import com.senacor.freighttenders.tender.TenderExceptionHandler.Violation;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
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

  /**
   * Checks the field rules of an update request; the class-level create rules are not in its group.
   */
  private static final Validator VALIDATOR =
      Validation.buildDefaultValidatorFactory().getValidator();

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

  /**
   * Replaces the shipment fields of an open tender. Checks in order: the tender exists, the request
   * is valid (the "today or later" rules only for a date that changes), the tender is open, and --
   * once it has offers -- only deliveryDate and bidDeadline change.
   */
  public Tender updateTender(Long id, CreateTenderRequest request) {
    Tender tender = getTenderOrThrow(id);
    validateUpdate(tender, request);
    rejectIfClosed(tender);
    if (!tender.getOffers().isEmpty()) {
      List<String> locked = changedLockedFields(tender, request);
      if (!locked.isEmpty()) {
        throw new TenderLockedFieldsException(id, locked);
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

  private void validateUpdate(Tender tender, CreateTenderRequest request) {
    List<Violation> violations = new ArrayList<>();
    for (ConstraintViolation<CreateTenderRequest> violation : VALIDATOR.validate(request)) {
      violations.add(new Violation(violation.getPropertyPath().toString(), violation.getMessage()));
    }
    violations.addAll(TenderRules.crossFieldViolations(request));
    violations.addAll(
        TenderRules.pastDateViolations(
            request,
            LocalDate.now(clock),
            !Objects.equals(request.pickupDate(), tender.getPickupDate()),
            !Objects.equals(request.bidDeadline(), tender.getBidDeadline())));
    if (!violations.isEmpty()) {
      throw new TenderRequestInvalidException(violations);
    }
  }

  private static List<String> changedLockedFields(Tender tender, CreateTenderRequest request) {
    List<String> changed = new ArrayList<>();
    addIfChanged(
        changed, "origin.country", tender.getOrigin().country(), request.origin().country());
    addIfChanged(
        changed,
        "origin.postalCode",
        tender.getOrigin().postalCode(),
        request.origin().postalCode());
    addIfChanged(changed, "origin.city", tender.getOrigin().city(), request.origin().city());
    addIfChanged(
        changed,
        "destination.country",
        tender.getDestination().country(),
        request.destination().country());
    addIfChanged(
        changed,
        "destination.postalCode",
        tender.getDestination().postalCode(),
        request.destination().postalCode());
    addIfChanged(
        changed, "destination.city", tender.getDestination().city(), request.destination().city());
    addIfChanged(changed, "pickupDate", tender.getPickupDate(), request.pickupDate());
    addIfChanged(changed, "commodity", tender.getCommodity(), request.commodity());
    addIfChanged(changed, "weightKg", tender.getWeightKg(), request.weightKg());
    if (tender.getLoadingMeters().compareTo(request.loadingMeters()) != 0) {
      changed.add("loadingMeters");
    }
    addIfChanged(changed, "palletCount", tender.getPalletCount(), request.palletCount());
    addIfChanged(changed, "equipmentType", tender.getEquipmentType(), request.equipmentType());
    addIfChanged(changed, "dangerousGoods", tender.isDangerousGoods(), request.dangerousGoods());
    addIfChanged(changed, "adrClass", tender.getAdrClass(), request.adrClass());
    addIfChanged(
        changed,
        "temperatureControlled",
        tender.isTemperatureControlled(),
        request.temperatureControlled());
    addIfChanged(
        changed, "temperatureMinC", tender.getTemperatureMinC(), request.temperatureMinC());
    addIfChanged(
        changed, "temperatureMaxC", tender.getTemperatureMaxC(), request.temperatureMaxC());
    addIfChanged(changed, "currency", tender.getCurrency(), request.currency());
    return changed;
  }

  private static void addIfChanged(
      List<String> changed, String field, Object stored, Object requested) {
    if (!Objects.equals(stored, requested)) {
      changed.add(field);
    }
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
