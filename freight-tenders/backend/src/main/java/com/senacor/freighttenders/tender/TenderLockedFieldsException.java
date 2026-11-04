package com.senacor.freighttenders.tender;

import java.util.List;

/**
 * Thrown when an update changes a field that is locked because the tender already has offers --
 * only the delivery date and the bid deadline stay editable then.
 */
public class TenderLockedFieldsException extends RuntimeException {

  public TenderLockedFieldsException(Long tenderId, List<String> fields) {
    super(
        "Tender "
            + tenderId
            + " already has offers; these fields can no longer be changed: "
            + String.join(", ", fields));
  }
}
