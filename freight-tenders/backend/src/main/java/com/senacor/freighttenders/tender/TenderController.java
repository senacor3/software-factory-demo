package com.senacor.freighttenders.tender;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** REST API for creating and closing tenders. */
@RestController
@RequestMapping("/api/tenders")
public class TenderController {

  private final TenderService tenderService;

  public TenderController(TenderService tenderService) {
    this.tenderService = tenderService;
  }

  @PostMapping("")
  public ResponseEntity<TenderResponse> createTender(@RequestBody CreateTenderRequest request) {
    Tender tender = tenderService.createTender(request.origin(), request.destination());
    return ResponseEntity.status(HttpStatus.CREATED).body(TenderResponse.from(tender));
  }

  @PostMapping("/{id}/close")
  public TenderResponse closeTender(@PathVariable Long id) {
    Tender tender = tenderService.closeTender(id);
    return TenderResponse.from(tender);
  }
}
