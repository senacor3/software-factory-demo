package com.senacor.freighttenders.tender;

/** Thrown when an offer is added to a {@link Tender} whose bid deadline lies in the past. */
public class BidDeadlinePassedException extends RuntimeException {

  public BidDeadlinePassedException(Long tenderId) {
    super("The bid deadline of tender " + tenderId + " has passed");
  }
}
