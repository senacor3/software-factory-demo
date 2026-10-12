package com.senacor.freighttenders.tender;

import jakarta.servlet.http.HttpServletRequest;
import java.time.Instant;
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

  /** Error body returned for mapped tender exceptions (AGENTS.md's documented error shape). */
  public record ErrorResponse(String error, String message, String path, Instant timestamp) {

    static ErrorResponse of(HttpStatus status, String message, HttpServletRequest request) {
      return new ErrorResponse(
          status.getReasonPhrase(), message, request.getRequestURI(), Instant.now());
    }
  }
}
