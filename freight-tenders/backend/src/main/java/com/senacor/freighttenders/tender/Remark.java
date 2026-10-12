package com.senacor.freighttenders.tender;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

/** A free-text remark recorded against a {@link Tender}. */
@Entity
public class Remark {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private String text;

  @ManyToOne private Tender tender;

  protected Remark() {
    // required by JPA
  }

  public Remark(String text) {
    this.text = text;
  }

  public Long getId() {
    return id;
  }

  public String getText() {
    return text;
  }

  public Tender getTender() {
    return tender;
  }

  void setTender(Tender tender) {
    this.tender = tender;
  }
}
