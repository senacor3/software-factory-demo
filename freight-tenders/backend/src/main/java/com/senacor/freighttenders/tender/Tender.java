package com.senacor.freighttenders.tender;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * A freight tender -- a request for supplier offers between an {@code origin} and {@code
 * destination} -- along with the remarks and offers recorded against it.
 *
 * <p>{@link #close()}, {@link #addRemark(Remark)} and {@link #addOffer(Offer)} are plain state
 * mutators that keep the bidirectional association consistent; they deliberately do not enforce the
 * open/closed invariant (e.g. rejecting a remark/offer added to a closed tender). That enforcement
 * belongs to the service layer introduced elsewhere, so gating it here would duplicate -- and risk
 * diverging from -- that layer's design.
 */
@Entity
public class Tender {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;

  private String origin;

  private String destination;

  @Enumerated(EnumType.STRING)
  private TenderStatus status = TenderStatus.OPEN;

  @OneToMany(mappedBy = "tender", cascade = CascadeType.ALL, orphanRemoval = true)
  private List<Remark> remarks = new ArrayList<>();

  @OneToMany(mappedBy = "tender", cascade = CascadeType.ALL, orphanRemoval = true)
  private List<Offer> offers = new ArrayList<>();

  protected Tender() {
    // required by JPA
  }

  public Tender(String origin, String destination) {
    this.origin = origin;
    this.destination = destination;
  }

  public Long getId() {
    return id;
  }

  public String getOrigin() {
    return origin;
  }

  public String getDestination() {
    return destination;
  }

  public TenderStatus getStatus() {
    return status;
  }

  public List<Remark> getRemarks() {
    return Collections.unmodifiableList(remarks);
  }

  public List<Offer> getOffers() {
    return Collections.unmodifiableList(offers);
  }

  public void addRemark(Remark remark) {
    remarks.add(remark);
    remark.setTender(this);
  }

  public void addOffer(Offer offer) {
    offers.add(offer);
    offer.setTender(this);
  }

  public void close() {
    status = TenderStatus.CLOSED;
  }
}
