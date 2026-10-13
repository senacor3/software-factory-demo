package com.senacor.freighttenders.tender;

/** An origin or destination address as returned by the tender API. */
public record AddressResponse(String country, String postalCode, String city) {

  public static AddressResponse from(Address address) {
    return new AddressResponse(address.country(), address.postalCode(), address.city());
  }
}
