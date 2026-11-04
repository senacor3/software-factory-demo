package com.senacor.freighttenders.tender;

import java.util.List;

/** Thrown when an edit changes a locked field of a tender that already has offers. */
public class TenderFieldsLockedException extends RuntimeException {

  public TenderFieldsLockedException(Long tenderId, List<String> fields) {
    super(
        "Tender "
            + tenderId
            + " has offers; only deliveryDate and bidDeadline can be changed, but these differ: "
            + String.join(", ", fields));
  }
}
