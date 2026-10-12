import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { TenderDetail as TenderDetailModel } from '../tender-api';
import { TenderDetail } from './tender-detail';

const OPEN_TENDER: TenderDetailModel = {
  id: 1,
  origin: 'Hamburg',
  destination: 'Berlin',
  status: 'OPEN',
  remarks: [{ id: 10, text: 'Bestehende Bemerkung' }],
  offers: [{ id: 20, supplierName: 'Spedition Muster', amount: 500 }],
};

const CLOSED_TENDER: TenderDetailModel = {
  ...OPEN_TENDER,
  status: 'CLOSED',
};

describe('TenderDetail', () => {
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'tenders/:id', component: TenderDetail }]),
      ],
    }).compileComponents();

    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('shows a German loading message before the response arrives', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');

    const element = harness.routeNativeElement as HTMLElement;
    expect(element.querySelector('[data-testid="loading"]')?.textContent).toContain(
      'wird geladen',
    );

    httpMock.expectOne('/api/tenders/1').flush(OPEN_TENDER);
  });

  it('shows remarks/offers for an open tender with enabled add-forms, and appends a new remark/offer without reloading', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');
    httpMock.expectOne('/api/tenders/1').flush(OPEN_TENDER);
    harness.detectChanges();

    const element = harness.routeNativeElement as HTMLElement;
    expect(element.querySelector('[data-testid="status"]')?.textContent).toContain('Offen');
    expect(element.querySelector('[data-testid="remarks"]')?.textContent).toContain(
      'Bestehende Bemerkung',
    );
    expect(element.querySelector('[data-testid="offers"]')?.textContent).toContain(
      'Spedition Muster',
    );

    const remarkInputBeforeFill = element.querySelector<HTMLInputElement>(
      '[data-testid="remark-input"]',
    );
    const offerSupplierInputBeforeFill = element.querySelector<HTMLInputElement>(
      '[data-testid="offer-supplier-input"]',
    );
    expect(remarkInputBeforeFill?.disabled).toBe(false);
    expect(offerSupplierInputBeforeFill?.disabled).toBe(false);
    expect(element.querySelector('[data-testid="closed-explanation"]')).toBeFalsy();

    const remarkInput = element.querySelector<HTMLInputElement>('[data-testid="remark-input"]')!;
    remarkInput.value = 'Neue Bemerkung';
    remarkInput.dispatchEvent(new Event('input'));
    harness.detectChanges();

    element.querySelector('[data-testid="remark-input"]')!.closest('form')!.dispatchEvent(
      new Event('submit'),
    );

    const remarkReq = httpMock.expectOne('/api/tenders/1/remarks');
    expect(remarkReq.request.body).toEqual({ text: 'Neue Bemerkung' });
    remarkReq.flush({ id: 11, text: 'Neue Bemerkung' });
    harness.detectChanges();

    expect(element.querySelector('[data-testid="remarks"]')?.textContent).toContain(
      'Neue Bemerkung',
    );
    httpMock.expectNone('/api/tenders/1');

    const supplierInput = element.querySelector<HTMLInputElement>(
      '[data-testid="offer-supplier-input"]',
    )!;
    const amountInput = element.querySelector<HTMLInputElement>(
      '[data-testid="offer-amount-input"]',
    )!;
    supplierInput.value = 'Neuer Anbieter';
    supplierInput.dispatchEvent(new Event('input'));
    amountInput.value = '750';
    amountInput.dispatchEvent(new Event('input'));
    harness.detectChanges();

    element.querySelector('[data-testid="offer-supplier-input"]')!.closest('form')!.dispatchEvent(
      new Event('submit'),
    );

    const offerReq = httpMock.expectOne('/api/tenders/1/offers');
    expect(offerReq.request.body).toEqual({ supplierName: 'Neuer Anbieter', amount: 750 });
    offerReq.flush({ id: 21, supplierName: 'Neuer Anbieter', amount: 750 });
    harness.detectChanges();

    expect(element.querySelector('[data-testid="offers"]')?.textContent).toContain(
      'Neuer Anbieter',
    );
  });

  it('disables the add-forms and shows a German explanation for a closed tender', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');
    httpMock.expectOne('/api/tenders/1').flush(CLOSED_TENDER);
    harness.detectChanges();

    const element = harness.routeNativeElement as HTMLElement;
    expect(element.querySelector('[data-testid="status"]')?.textContent).toContain(
      'Geschlossen',
    );
    expect(element.querySelector('[data-testid="closed-explanation"]')?.textContent).toContain(
      'geschlossen',
    );

    const remarkSubmit = element.querySelector<HTMLButtonElement>('[data-testid="remark-submit"]');
    const offerSubmit = element.querySelector<HTMLButtonElement>('[data-testid="offer-submit"]');
    const remarkInput = element.querySelector<HTMLInputElement>('[data-testid="remark-input"]');
    const offerSupplierInput = element.querySelector<HTMLInputElement>(
      '[data-testid="offer-supplier-input"]',
    );
    expect(remarkSubmit?.disabled).toBe(true);
    expect(offerSubmit?.disabled).toBe(true);
    expect(remarkInput?.disabled).toBe(true);
    expect(offerSupplierInput?.disabled).toBe(true);
  });

  it('shows a German not-found/error message when the tender cannot be loaded', async () => {
    const harness = await RouterTestingHarness.create('/tenders/999');
    httpMock.expectOne('/api/tenders/999').flush('Not found', {
      status: 404,
      statusText: 'Not Found',
    });
    harness.detectChanges();

    const element = harness.routeNativeElement as HTMLElement;
    expect(element.querySelector('[data-testid="load-error"]')?.textContent).toContain(
      'nicht gefunden',
    );
  });
});
