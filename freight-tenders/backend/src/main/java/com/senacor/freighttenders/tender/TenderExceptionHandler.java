package com.senacor.freighttenders.tender;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * Maps the tender domain's exceptions to HTTP status -- re-enforcing entry 3's open/closed rule
 * (and entry 2's existence check) at the HTTP layer, in one place rather than a per-endpoint
 * try/catch.
 */
@RestControllerAdvice
public class TenderExceptionHandler {

  @ExceptionHandler(TenderClosedException.class)
  public ResponseEntity<ErrorResponse> handleTenderClosed(TenderClosedException exception) {
    return ResponseEntity.status(HttpStatus.CONFLICT)
        .body(new ErrorResponse(exception.getMessage()));
  }

  @ExceptionHandler(TenderNotFoundException.class)
  public ResponseEntity<ErrorResponse> handleTenderNotFound(TenderNotFoundException exception) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(new ErrorResponse(exception.getMessage()));
  }

  /** Error body returned for mapped tender exceptions. */
  public record ErrorResponse(String message) {}
}
