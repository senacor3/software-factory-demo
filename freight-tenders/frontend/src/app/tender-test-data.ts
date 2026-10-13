import { TenderDetail, TenderSummary } from './tender-api';

// Shared by the specs only: a complete tender, with each spec overriding what it cares about.
export function tenderSummary(overrides: Partial<TenderSummary> = {}): TenderSummary {
  return {
    id: 1,
    origin: { country: 'DE', postalCode: '20457', city: 'Hamburg' },
    destination: { country: 'NL', postalCode: '3011 AA', city: 'Rotterdam' },
    pickupDate: '2099-10-20',
    deliveryDate: '2099-10-22',
    bidDeadline: '2099-10-16',
    commodity: 'Maschinenteile auf Europaletten',
    weightKg: 18500,
    loadingMeters: 13.6,
    palletCount: 33,
    equipmentType: 'CURTAIN_SIDER',
    dangerousGoods: false,
    adrClass: null,
    temperatureControlled: false,
    temperatureMinC: null,
    temperatureMaxC: null,
    currency: 'EUR',
    status: 'OPEN',
    offerCount: 0,
    lowestOfferAmount: null,
    ...overrides,
  };
}

export function tenderDetail(overrides: Partial<TenderDetail> = {}): TenderDetail {
  const { offerCount: _count, lowestOfferAmount: _lowest, ...summary } = tenderSummary();
  return { ...summary, remarks: [], offers: [], ...overrides };
}
