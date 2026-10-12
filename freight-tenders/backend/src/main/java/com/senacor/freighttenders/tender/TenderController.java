package com.senacor.freighttenders.tender;

import jakarta.validation.Valid;
import java.util.List;
import java.util.Optional;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** REST API for creating, closing, listing and inspecting tenders, and recording remarks/offers. */
@RestController
@RequestMapping("/api/tenders")
public class TenderController {

  private final TenderService tenderService;

  public TenderController(TenderService tenderService) {
    this.tenderService = tenderService;
  }

  @PostMapping("")
  public ResponseEntity<TenderResponse> createTender(
      @Valid @RequestBody CreateTenderRequest request) {
    Tender tender = tenderService.createTender(request.origin(), request.destination());
    return ResponseEntity.status(HttpStatus.CREATED).body(TenderResponse.from(tender));
  }

  @PostMapping("/{id}/close")
  public TenderResponse closeTender(@PathVariable Long id) {
    Tender tender = tenderService.closeTender(id);
    return TenderResponse.from(tender);
  }

  @GetMapping("")
  public List<TenderResponse> listTenders(@RequestParam(required = false) TenderStatus status) {
    return tenderService.listTenders(Optional.ofNullable(status)).stream()
        .map(TenderResponse::from)
        .toList();
  }

  @GetMapping("/{id}")
  public TenderDetailResponse getTender(@PathVariable Long id) {
    Tender tender = tenderService.getTender(id);
    return TenderDetailResponse.from(tender);
  }

  @PostMapping("/{id}/remarks")
  public ResponseEntity<RemarkResponse> addRemark(
      @PathVariable Long id, @RequestBody AddRemarkRequest request) {
    Tender tender = tenderService.addRemark(id, request.text());
    Remark createdRemark = tender.getRemarks().get(tender.getRemarks().size() - 1);
    return ResponseEntity.status(HttpStatus.CREATED).body(RemarkResponse.from(createdRemark));
  }

  @PostMapping("/{id}/offers")
  public ResponseEntity<OfferResponse> addOffer(
      @PathVariable Long id, @RequestBody AddOfferRequest request) {
    Tender tender = tenderService.addOffer(id, request.supplierName(), request.amount());
    Offer createdOffer = tender.getOffers().get(tender.getOffers().size() - 1);
    return ResponseEntity.status(HttpStatus.CREATED).body(OfferResponse.from(createdOffer));
  }
}
