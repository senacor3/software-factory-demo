import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import {
  COUNTRY_LABELS,
  CURRENCIES,
  CreateTenderRequest,
  EQUIPMENT_LABELS,
  EquipmentType,
  TenderApiService,
} from './tender-api';
import { tenderDetail, tenderSummary } from './tender-test-data';

describe('TenderApiService', () => {
  let service: TenderApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(TenderApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('calls GET /api/tenders', () => {
    service.list().subscribe();

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.method).toBe('GET');
    req.flush([]);
  });

  it('calls POST /api/tenders/{id}/close and emits the returned summary', () => {
    let result: unknown;
    service.close(5).subscribe((summary) => (result = summary));

    const req = httpMock.expectOne('/api/tenders/5/close');
    expect(req.request.method).toBe('POST');
    const summary = tenderSummary({ id: 5, status: 'CLOSED' });
    req.flush(summary);

    expect(result).toEqual(summary);
  });

  it('calls POST /api/tenders/{id}/offers/{offerId}/award and emits the returned detail', () => {
    let result: unknown;
    service.awardTender(5, 7).subscribe((detail) => (result = detail));

    const req = httpMock.expectOne('/api/tenders/5/offers/7/award');
    expect(req.request.method).toBe('POST');
    const detail = tenderDetail({ id: 5, status: 'AWARDED', awardedOfferId: 7 });
    req.flush(detail);

    expect(result).toEqual(detail);
  });

  it('calls POST /api/tenders with the full typed request object', () => {
    const request: CreateTenderRequest = {
      origin: { country: 'DE', postalCode: '20457', city: 'Hamburg' },
      destination: { country: 'NL', postalCode: '3011 AA', city: 'Rotterdam' },
      pickupDate: '2026-10-20',
      deliveryDate: '2026-10-22',
      bidDeadline: '2026-10-16',
      commodity: 'Maschinenteile auf Europaletten',
      weightKg: 18500,
      loadingMeters: 13.6,
      palletCount: 33,
      equipmentType: 'CURTAIN_SIDER',
      dangerousGoods: false,
      temperatureControlled: false,
      currency: 'EUR',
    };

    service.create(request).subscribe();

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(request);
    req.flush(tenderSummary());
  });

  it('calls GET /api/tenders/:id', () => {
    service.detail(42).subscribe();

    const req = httpMock.expectOne('/api/tenders/42');
    expect(req.request.method).toBe('GET');
    req.flush(tenderDetail({ id: 42 }));
  });

  it('labels every equipment type in German', () => {
    const types: EquipmentType[] = ['CURTAIN_SIDER', 'BOX', 'REEFER', 'FLATBED', 'MEGA_TRAILER'];

    expect(Object.keys(EQUIPMENT_LABELS).sort()).toEqual([...types].sort());
    expect(EQUIPMENT_LABELS.CURTAIN_SIDER).toBe('Planenauflieger');
    expect(EQUIPMENT_LABELS.REEFER).toBe('Kühlauflieger');
  });

  it('offers the seven currencies and the thirteen countries of the create form', () => {
    expect(CURRENCIES).toEqual(['EUR', 'CHF', 'GBP', 'PLN', 'CZK', 'DKK', 'SEK']);
    expect(Object.keys(COUNTRY_LABELS)).toEqual([
      'DE',
      'AT',
      'CH',
      'NL',
      'BE',
      'LU',
      'FR',
      'IT',
      'ES',
      'PL',
      'CZ',
      'DK',
      'SE',
    ]);
    expect(COUNTRY_LABELS['DE']).toBe('Deutschland');
  });

  it('calls POST /api/tenders/:id/remarks with the text', () => {
    service.addRemark(42, 'Bitte schnell liefern').subscribe();

    const req = httpMock.expectOne('/api/tenders/42/remarks');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ text: 'Bitte schnell liefern' });
    req.flush({ id: 1, text: 'Bitte schnell liefern' });
  });

  it('calls POST /api/tenders/:id/offers with all offer fields', () => {
    const request = {
      supplierName: 'Spedition Muster',
      amount: 1234.56,
      deliveryDate: '2099-10-21',
      validUntil: '2099-10-30',
      note: 'Inkl. Maut',
    };
    service.addOffer(42, request).subscribe();

    const req = httpMock.expectOne('/api/tenders/42/offers');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(request);
    req.flush({ id: 1, ...request });
  });
});
