import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { TenderApiService } from './tender-api';

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

  it('calls POST /api/tenders with origin and destination', () => {
    service.create('Hamburg', 'Berlin').subscribe();

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ origin: 'Hamburg', destination: 'Berlin' });
    req.flush({ id: 1, origin: 'Hamburg', destination: 'Berlin', status: 'OPEN' });
  });

  it('calls GET /api/tenders/:id', () => {
    service.detail(42).subscribe();

    const req = httpMock.expectOne('/api/tenders/42');
    expect(req.request.method).toBe('GET');
    req.flush({
      id: 42,
      origin: 'Hamburg',
      destination: 'Berlin',
      status: 'OPEN',
      remarks: [],
      offers: [],
    });
  });

  it('calls POST /api/tenders/:id/remarks with the text', () => {
    service.addRemark(42, 'Bitte schnell liefern').subscribe();

    const req = httpMock.expectOne('/api/tenders/42/remarks');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ text: 'Bitte schnell liefern' });
    req.flush({ id: 1, text: 'Bitte schnell liefern' });
  });

  it('calls POST /api/tenders/:id/offers with supplierName and amount', () => {
    service.addOffer(42, 'Spedition Muster', 1234.56).subscribe();

    const req = httpMock.expectOne('/api/tenders/42/offers');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ supplierName: 'Spedition Muster', amount: 1234.56 });
    req.flush({ id: 1, supplierName: 'Spedition Muster', amount: 1234.56 });
  });
});
