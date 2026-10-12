package com.senacor.freighttenders.tender;

/** Response body for a {@link Remark}, nested under {@link TenderDetailResponse}. */
public record RemarkResponse(Long id, String text) {

  public static RemarkResponse from(Remark remark) {
    return new RemarkResponse(remark.getId(), remark.getText());
  }
}
