package com.senacor.freighttenders.tender;

import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.servlet.http.HttpServletRequest;
import java.time.Instant;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
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
  public ResponseEntity<ErrorResponse> handleTenderClosed(
      TenderClosedException exception, HttpServletRequest request) {
    return ResponseEntity.status(HttpStatus.CONFLICT)
        .body(ErrorResponse.of(HttpStatus.CONFLICT, exception.getMessage(), request));
  }

  @ExceptionHandler(OfferExpiredException.class)
  public ResponseEntity<ErrorResponse> handleOfferExpired(
      OfferExpiredException exception, HttpServletRequest request) {
    return ResponseEntity.status(HttpStatus.CONFLICT)
        .body(ErrorResponse.of(HttpStatus.CONFLICT, exception.getMessage(), request));
  }

  @ExceptionHandler(OfferNotFoundException.class)
  public ResponseEntity<ErrorResponse> handleOfferNotFound(
      OfferNotFoundException exception, HttpServletRequest request) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(ErrorResponse.of(HttpStatus.NOT_FOUND, exception.getMessage(), request));
  }

  @ExceptionHandler(BidDeadlinePassedException.class)
  public ResponseEntity<ErrorResponse> handleBidDeadlinePassed(
      BidDeadlinePassedException exception, HttpServletRequest request) {
    return ResponseEntity.status(HttpStatus.CONFLICT)
        .body(ErrorResponse.of(HttpStatus.CONFLICT, exception.getMessage(), request));
  }

  @ExceptionHandler(OfferDeliveryBeforePickupException.class)
  public ResponseEntity<ErrorResponse> handleOfferDeliveryBeforePickup(
      OfferDeliveryBeforePickupException exception, HttpServletRequest request) {
    return badRequest(
        "Request validation failed",
        List.of(new Violation("deliveryDate", "must not be before the tender's pickupDate")),
        request);
  }

  @ExceptionHandler(TenderNotFoundException.class)
  public ResponseEntity<ErrorResponse> handleTenderNotFound(
      TenderNotFoundException exception, HttpServletRequest request) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(ErrorResponse.of(HttpStatus.NOT_FOUND, exception.getMessage(), request));
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<ErrorResponse> handleInvalidRequest(
      MethodArgumentNotValidException exception, HttpServletRequest request) {
    // Global (object-level) errors are kept too, named by the validated object, so a constraint
    // without a field name is never silently dropped.
    List<Violation> violations =
        exception.getBindingResult().getAllErrors().stream()
            .map(
                error ->
                    new Violation(
                        error instanceof FieldError fieldError
                            ? fieldError.getField()
                            : error.getObjectName(),
                        error.getDefaultMessage()))
            .toList();
    return badRequest("Request validation failed", violations, request);
  }

  @ExceptionHandler(HttpMessageNotReadableException.class)
  public ResponseEntity<ErrorResponse> handleUnreadableRequest(
      HttpMessageNotReadableException exception, HttpServletRequest request) {
    return badRequest("Request body is malformed or invalid", List.of(), request);
  }

  private static ResponseEntity<ErrorResponse> badRequest(
      String message, List<Violation> violations, HttpServletRequest request) {
    return ResponseEntity.status(HttpStatus.BAD_REQUEST)
        .body(
            new ErrorResponse(
                HttpStatus.BAD_REQUEST.getReasonPhrase(),
                message,
                request.getRequestURI(),
                Instant.now(),
                violations));
  }

  /**
   * Error body returned for mapped tender exceptions (AGENTS.md's documented error shape).
   * Violations are only present on 400s.
   */
  public record ErrorResponse(
      String error,
      String message,
      String path,
      Instant timestamp,
      @JsonInclude(JsonInclude.Include.NON_NULL) List<Violation> violations) {

    // Defensive copy (null stays null, since violations is only present on 400s) so neither the
    // constructor nor the accessor exposes a caller-mutable list (SpotBugs EI_EXPOSE_REP/REP2).
    public ErrorResponse {
      violations = violations == null ? null : List.copyOf(violations);
    }

    static ErrorResponse of(HttpStatus status, String message, HttpServletRequest request) {
      return new ErrorResponse(
          status.getReasonPhrase(), message, request.getRequestURI(), Instant.now(), null);
    }
  }

  /** A single failed field constraint. */
  public record Violation(String field, String message) {}
}
