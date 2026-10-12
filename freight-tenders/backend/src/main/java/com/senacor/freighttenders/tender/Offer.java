package com.senacor.freighttenders.tender;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import java.math.BigDecimal;

/** A supplier's offer submitted against a {@link Tender}. */
@Entity
public class Offer {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private String supplierName;

  private BigDecimal amount;

  @ManyToOne private Tender tender;

  protected Offer() {
    // required by JPA
  }

  public Offer(String supplierName, BigDecimal amount) {
    this.supplierName = supplierName;
    this.amount = amount;
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

  public Tender getTender() {
    return tender;
  }

  void setTender(Tender tender) {
    this.tender = tender;
  }
}
