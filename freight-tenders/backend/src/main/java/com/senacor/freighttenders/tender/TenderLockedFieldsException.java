package com.senacor.freighttenders.tender;

import java.util.List;

/**
 * Thrown when an update changes a field that can no longer change because the tender already has
 * offers.
 */
public class TenderLockedFieldsException extends RuntimeException {

  public TenderLockedFieldsException(Long tenderId, List<String> fields) {
    super(
        "Tender "
            + tenderId
            + " has offers; these fields can no longer be changed: "
            + String.join(", ", fields));
  }
}
