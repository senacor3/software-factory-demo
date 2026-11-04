import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { TenderDetail } from '../tender-api';
import { offerSummary, tenderDetail, tenderSummary } from '../tender-test-data';
import { routes } from '../app.routes';

describe('TenderEdit', () => {
  let httpMock: HttpTestingController;
  let harness: RouterTestingHarness;
  let root: HTMLElement;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter(routes)],
    });
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  async function open(url: string, tender?: TenderDetail, status = 200): Promise<void> {
    harness = await RouterTestingHarness.create();
    const navigation = harness.navigateByUrl(url);
    await Promise.resolve();
    if (tender !== undefined || status !== 200) {
      const request = httpMock.expectOne('/api/tenders/1');
      if (status === 200) {
        request.flush(tender);
      } else {
        request.flush({}, { status, statusText: 'Error' });
      }
    }
    await navigation;
    harness.detectChanges();
    root = harness.routeNativeElement as HTMLElement;
  }

  function element<T extends HTMLElement>(testId: string): T | null {
    return root.querySelector<T>(`[data-testid="${testId}"]`);
  }

  function setValue(testId: string, value: string): void {
    const control = element<HTMLInputElement | HTMLSelectElement>(testId)!;
    control.value = value;
    control.dispatchEvent(new Event(control instanceof HTMLSelectElement ? 'change' : 'input'));
    harness.detectChanges();
  }

  const submitButton = () => element<HTMLButtonElement>('submit')!;

  function submit(): void {
    root.querySelector('form')!.dispatchEvent(new Event('submit'));
    harness.detectChanges();
  }

  it('shows a German loading message before the response arrives', async () => {
    harness = await RouterTestingHarness.create();
    const navigation = harness.navigateByUrl('/tenders/1/edit');
    await Promise.resolve();
    harness.detectChanges();
    root = harness.routeNativeElement as HTMLElement;

    expect(element('loading')?.textContent).toContain('Ausschreibung wird geladen…');
    expect(element('back-link')).not.toBeNull();

    httpMock.expectOne('/api/tenders/1').flush(tenderDetail());
    await navigation;
  });

  it('shows the detail page error for a load failure and keeps the back link', async () => {
    await open('/tenders/1/edit', undefined, 404);

    expect(element('load-error')?.textContent).toContain('nicht gefunden');
    expect(element('back-link')).not.toBeNull();
    expect(element('submit')).toBeNull();
  });

  it('shows the detail page error for a non-numeric id without a request', async () => {
    await open('/tenders/abc/edit');

    expect(element('load-error')?.textContent).toContain('nicht gefunden');
  });

  it('shows not-editable and no form for a tender that is not open', async () => {
    await open('/tenders/1/edit', tenderDetail({ status: 'CLOSED' }));

    expect(element('not-editable')).not.toBeNull();
    expect(element('submit')).toBeNull();
  });

  it('prefills the form including the ADR class and the temperature range', async () => {
    await open(
      '/tenders/1/edit',
      tenderDetail({
        dangerousGoods: true,
        adrClass: '4.1',
        temperatureControlled: true,
        temperatureMinC: -18,
        temperatureMaxC: -15,
        equipmentType: 'REEFER',
      }),
    );

    expect(element<HTMLInputElement>('commodity')?.value).toBe('Maschinenteile auf Europaletten');
    expect(element<HTMLInputElement>('pickupDate')?.value).toBe('2099-10-20');
    expect(element<HTMLSelectElement>('adrClass')?.value).toBe('4.1');
    expect(element<HTMLInputElement>('temperatureMinC')?.value).toBe('-18');
    expect(element<HTMLInputElement>('temperatureMaxC')?.value).toBe('-15');
  });

  it('disables Speichern while nothing changed and enables it after a valid change', async () => {
    await open('/tenders/1/edit', tenderDetail());
    expect(submitButton().disabled).toBe(true);

    setValue('commodity', 'Andere Ware');
    expect(submitButton().disabled).toBe(false);

    setValue('commodity', 'Maschinenteile auf Europaletten');
    expect(submitButton().disabled).toBe(true);

    setValue('commodity', '');
    expect(submitButton().disabled).toBe(true);
  });

  it('accepts a stored past bid deadline but rejects a changed past date', async () => {
    await open('/tenders/1/edit', tenderDetail({ bidDeadline: '2000-01-01', pickupDate: '2099-10-20' }));

    setValue('commodity', 'Andere Ware');
    expect(submitButton().disabled).toBe(false);

    setValue('bidDeadline', '2000-01-02');
    expect(submitButton().disabled).toBe(true);
  });

  it('sends the complete data via PUT and navigates to the detail page on success', async () => {
    await open('/tenders/1/edit', tenderDetail());
    const router = TestBed.inject(Router);
    const navigate = vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);

    setValue('commodity', 'Andere Ware');
    submit();

    const request = httpMock.expectOne('/api/tenders/1');
    expect(request.request.method).toBe('PUT');
    expect(request.request.body).toEqual({
      origin: { country: 'DE', postalCode: '20457', city: 'Hamburg' },
      destination: { country: 'NL', postalCode: '3011 AA', city: 'Rotterdam' },
      pickupDate: '2099-10-20',
      deliveryDate: '2099-10-22',
      bidDeadline: '2099-10-16',
      commodity: 'Andere Ware',
      weightKg: 18500,
      loadingMeters: 13.6,
      palletCount: 33,
      equipmentType: 'CURTAIN_SIDER',
      dangerousGoods: false,
      temperatureControlled: false,
      currency: 'EUR',
    });
    request.flush(tenderSummary({ commodity: 'Andere Ware' }));

    expect(navigate).toHaveBeenCalledWith('/tenders/1');
  });

  it('points Abbrechen and the back link at the detail page without a request', async () => {
    await open('/tenders/1/edit', tenderDetail());

    expect(element('cancel')?.getAttribute('href')).toBe('/tenders/1');
    expect(element('back-link')?.getAttribute('href')).toBe('/tenders/1');
  });

  it('locks every field but delivery date and bid deadline when offers exist', async () => {
    await open(
      '/tenders/1/edit',
      tenderDetail({ offers: [offerSummary()] }),
    );

    expect(element('locked-fields-notice')).not.toBeNull();
    expect(element<HTMLInputElement>('commodity')?.disabled).toBe(true);
    expect(element<HTMLInputElement>('pickupDate')?.disabled).toBe(true);
    expect(element<HTMLInputElement>('origin-city')?.disabled).toBe(true);
    expect(element<HTMLInputElement>('deliveryDate')?.disabled).toBe(false);
    expect(element<HTMLInputElement>('bidDeadline')?.disabled).toBe(false);

    setValue('deliveryDate', '2099-10-25');
    submit();

    const request = httpMock.expectOne('/api/tenders/1');
    expect(request.request.body).toMatchObject({
      commodity: 'Maschinenteile auf Europaletten',
      pickupDate: '2099-10-20',
      deliveryDate: '2099-10-25',
      origin: { country: 'DE', postalCode: '20457', city: 'Hamburg' },
    });
    request.flush({}, { status: 500, statusText: 'Error' });
  });

  it('shows the conflict message for a 409 and keeps the entered values', async () => {
    await open('/tenders/1/edit', tenderDetail());

    setValue('commodity', 'Andere Ware');
    submit();
    httpMock.expectOne('/api/tenders/1').flush({}, { status: 409, statusText: 'Conflict' });
    harness.detectChanges();

    const alert = element('conflict-error');
    expect(alert?.getAttribute('role')).toBe('alert');
    expect(alert?.textContent).toContain('kann nicht geändert werden');
    expect(element<HTMLInputElement>('commodity')?.value).toBe('Andere Ware');
  });

  it('shows the generic message for another failure and keeps the entered values', async () => {
    await open('/tenders/1/edit', tenderDetail());

    setValue('commodity', 'Andere Ware');
    submit();
    httpMock.expectOne('/api/tenders/1').flush({}, { status: 500, statusText: 'Error' });
    harness.detectChanges();

    const alert = element('submit-error');
    expect(alert?.getAttribute('role')).toBe('alert');
    expect(alert?.textContent).toContain('konnte nicht gespeichert werden');
    expect(element<HTMLInputElement>('commodity')?.value).toBe('Andere Ware');
  });
});
