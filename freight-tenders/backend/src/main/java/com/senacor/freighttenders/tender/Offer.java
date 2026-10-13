package com.senacor.freighttenders.tender;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import java.math.BigDecimal;
import java.time.LocalDate;

/** A supplier's offer submitted against a {@link Tender}. */
@Entity
public class Offer {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private String supplierName;

  private BigDecimal amount;

  private LocalDate deliveryDate;

  private LocalDate validUntil;

  private String note;

  @ManyToOne private Tender tender;

  protected Offer() {
    // required by JPA
  }

  public Offer(
      String supplierName,
      BigDecimal amount,
      LocalDate deliveryDate,
      LocalDate validUntil,
      String note) {
    this.supplierName = supplierName;
    this.amount = amount;
    this.deliveryDate = deliveryDate;
    this.validUntil = validUntil;
    this.note = note == null || note.isBlank() ? null : note;
  }

  public Long getId() {
    return id;
  }

  public String getSupplierName() {
    return supplierName;
  }

  public BigDecimal getAmount() {
    return amount;
  }

  public LocalDate getDeliveryDate() {
    return deliveryDate;
  }

  public LocalDate getValidUntil() {
    return validUntil;
  }

  public String getNote() {
    return note;
  }

  public Tender getTender() {
    return tender;
  }

  void setTender(Tender tender) {
    this.tender = tender;
  }
}
