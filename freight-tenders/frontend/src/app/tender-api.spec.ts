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
});
