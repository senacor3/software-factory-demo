package com.senacor.freighttenders.tender;

import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.servlet.http.HttpServletRequest;
import java.time.Instant;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
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

  @ExceptionHandler(TenderNotFoundException.class)
  public ResponseEntity<ErrorResponse> handleTenderNotFound(
      TenderNotFoundException exception, HttpServletRequest request) {
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(ErrorResponse.of(HttpStatus.NOT_FOUND, exception.getMessage(), request));
  }

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<ErrorResponse> handleInvalidRequest(
      MethodArgumentNotValidException exception, HttpServletRequest request) {
    List<Violation> violations =
        exception.getBindingResult().getFieldErrors().stream()
            .map(fieldError -> new Violation(fieldError.getField(), fieldError.getDefaultMessage()))
            .toList();
    return ResponseEntity.status(HttpStatus.BAD_REQUEST)
        .body(
            new ErrorResponse(
                HttpStatus.BAD_REQUEST.getReasonPhrase(),
                "Request validation failed",
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

    static ErrorResponse of(HttpStatus status, String message, HttpServletRequest request) {
      return new ErrorResponse(
          status.getReasonPhrase(), message, request.getRequestURI(), Instant.now(), null);
    }
  }

  /** A single failed field constraint. */
  public record Violation(String field, String message) {}
}
