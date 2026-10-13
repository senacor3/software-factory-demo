package com.senacor.freighttenders.tender;

import jakarta.persistence.AttributeOverride;
import jakarta.persistence.AttributeOverrides;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import java.math.BigDecimal;
import java.time.LocalDate;
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

  @Embedded
  @AttributeOverrides({
    @AttributeOverride(name = "country", column = @Column(name = "origin_country")),
    @AttributeOverride(name = "postalCode", column = @Column(name = "origin_postal_code")),
    @AttributeOverride(name = "city", column = @Column(name = "origin_city"))
  })
  private Address origin;

  @Embedded
  @AttributeOverrides({
    @AttributeOverride(name = "country", column = @Column(name = "destination_country")),
    @AttributeOverride(name = "postalCode", column = @Column(name = "destination_postal_code")),
    @AttributeOverride(name = "city", column = @Column(name = "destination_city"))
  })
  private Address destination;

  private LocalDate pickupDate;

  private LocalDate deliveryDate;

  private LocalDate bidDeadline;

  private String commodity;

  private Integer weightKg;

  @Column(precision = 3, scale = 1)
  private BigDecimal loadingMeters;

  private Integer palletCount;

  @Enumerated(EnumType.STRING)
  private EquipmentType equipmentType;

  private boolean dangerousGoods;

  private String adrClass;

  private boolean temperatureControlled;

  private Integer temperatureMinC;

  private Integer temperatureMaxC;

  @Enumerated(EnumType.STRING)
  private Currency currency;

  @Enumerated(EnumType.STRING)
  private TenderStatus status = TenderStatus.OPEN;

  @ManyToOne private Offer awardedOffer;

  @OneToMany(mappedBy = "tender", cascade = CascadeType.ALL, orphanRemoval = true)
  private List<Remark> remarks = new ArrayList<>();

  @OneToMany(mappedBy = "tender", cascade = CascadeType.ALL, orphanRemoval = true)
  private List<Offer> offers = new ArrayList<>();

  protected Tender() {
    // required by JPA
  }

  public Tender(
      Address origin,
      Address destination,
      LocalDate pickupDate,
      LocalDate deliveryDate,
      LocalDate bidDeadline,
      String commodity,
      Integer weightKg,
      BigDecimal loadingMeters,
      Integer palletCount,
      EquipmentType equipmentType,
      boolean dangerousGoods,
      String adrClass,
      boolean temperatureControlled,
      Integer temperatureMinC,
      Integer temperatureMaxC,
      Currency currency) {
    this.origin = origin;
    this.destination = destination;
    this.pickupDate = pickupDate;
    this.deliveryDate = deliveryDate;
    this.bidDeadline = bidDeadline;
    this.commodity = commodity;
    this.weightKg = weightKg;
    this.loadingMeters = loadingMeters;
    this.palletCount = palletCount;
    this.equipmentType = equipmentType;
    this.dangerousGoods = dangerousGoods;
    this.adrClass = adrClass;
    this.temperatureControlled = temperatureControlled;
    this.temperatureMinC = temperatureMinC;
    this.temperatureMaxC = temperatureMaxC;
    this.currency = currency;
  }

  public Long getId() {
    return id;
  }

  public Address getOrigin() {
    return origin;
  }

  public Address getDestination() {
    return destination;
  }

  public LocalDate getPickupDate() {
    return pickupDate;
  }

  public LocalDate getDeliveryDate() {
    return deliveryDate;
  }

  public LocalDate getBidDeadline() {
    return bidDeadline;
  }

  public String getCommodity() {
    return commodity;
  }

  public Integer getWeightKg() {
    return weightKg;
  }

  public BigDecimal getLoadingMeters() {
    return loadingMeters;
  }

  public Integer getPalletCount() {
    return palletCount;
  }

  public EquipmentType getEquipmentType() {
    return equipmentType;
  }

  public boolean isDangerousGoods() {
    return dangerousGoods;
  }

  public String getAdrClass() {
    return adrClass;
  }

  public boolean isTemperatureControlled() {
    return temperatureControlled;
  }

  public Integer getTemperatureMinC() {
    return temperatureMinC;
  }

  public Integer getTemperatureMaxC() {
    return temperatureMaxC;
  }

  public Currency getCurrency() {
    return currency;
  }

  public TenderStatus getStatus() {
    return status;
  }

  public Offer getAwardedOffer() {
    return awardedOffer;
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

  public void award(Offer offer) {
    awardedOffer = offer;
    status = TenderStatus.AWARDED;
  }
}
