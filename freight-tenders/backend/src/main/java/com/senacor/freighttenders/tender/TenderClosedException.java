package com.senacor.freighttenders.tender;

/**
 * Thrown when a remark or offer is added to a {@link Tender} that has already been closed -- the
 * epic's one non-trivial rule, enforced by {@link TenderService}.
 */
public class TenderClosedException extends RuntimeException {

  public TenderClosedException(Long tenderId) {
    super("Tender " + tenderId + " is closed and can no longer be modified");
  }

  public TenderClosedException(Long tenderId, TenderStatus status) {
    super(
        status == TenderStatus.AWARDED
            ? "Tender " + tenderId + " is awarded and can no longer be modified"
            : "Tender " + tenderId + " is closed and can no longer be modified");
  }
}
