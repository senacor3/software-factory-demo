import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { TenderDetail } from '../tender-api';
import { offerSummary, tenderDetail, tenderSummary } from '../tender-test-data';
import { TenderEdit } from './tender-edit';

const OPEN_TENDER: TenderDetail = tenderDetail();

describe('TenderEdit', () => {
  let httpMock: HttpTestingController;
  let harness: RouterTestingHarness;
  let root: HTMLElement;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([
          { path: 'tenders/:id/edit', component: TenderEdit },
          { path: 'tenders/:id', children: [] },
        ]),
      ],
    });
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  async function open(url: string, tender?: TenderDetail): Promise<void> {
    harness = await RouterTestingHarness.create(url);
    if (tender) {
      httpMock.expectOne('/api/tenders/1').flush(tender);
    }
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
    control.dispatchEvent(new Event('blur'));
    harness.detectChanges();
  }

  function setChecked(testId: string, checked: boolean): void {
    const checkbox = element<HTMLInputElement>(testId)!;
    checkbox.checked = checked;
    checkbox.dispatchEvent(new Event('change'));
    harness.detectChanges();
  }

  const saveButton = () => element<HTMLButtonElement>('submit')!;

  function submit(): void {
    saveButton().click();
    harness.detectChanges();
  }

  it('shows a loading message before the tender arrives', async () => {
    await open('/tenders/1/edit');

    expect(element('loading')?.textContent).toContain('wird geladen');
    expect(element('back-link')).not.toBeNull();
    httpMock.expectOne('/api/tenders/1').flush(OPEN_TENDER);
  });

  it('shows a German error and the back link when the tender cannot be loaded', async () => {
    await open('/tenders/1/edit');
    httpMock.expectOne('/api/tenders/1').flush({}, { status: 404, statusText: 'Not Found' });
    harness.detectChanges();

    expect(element('load-error')?.textContent).toContain('nicht gefunden');
    expect(element('back-link')).not.toBeNull();
    expect(element('submit')).toBeNull();
  });

  it('shows the load error without a request for a non-numeric id', async () => {
    await open('/tenders/abc/edit');

    expect(element('load-error')).not.toBeNull();
    expect(element('back-link')).not.toBeNull();
  });

  it('explains that an awarded or a closed tender cannot be edited', async () => {
    await open('/tenders/1/edit', { ...OPEN_TENDER, status: 'CLOSED' });

    expect(element('not-editable')?.textContent).toContain('nicht mehr offen');
    expect(element('back-link')).not.toBeNull();
    expect(element('submit')).toBeNull();
  });

  it('prefills every field, including the conditional ADR and temperature fields', async () => {
    await open(
      '/tenders/1/edit',
      tenderDetail({
        dangerousGoods: true,
        adrClass: '4.1',
        temperatureControlled: true,
        temperatureMinC: -18,
        temperatureMaxC: -10,
        equipmentType: 'REEFER',
      }),
    );

    expect(element<HTMLInputElement>('origin-city')!.value).toBe('Hamburg');
    expect(element<HTMLSelectElement>('destination-country')!.value).toBe('NL');
    expect(element<HTMLInputElement>('pickupDate')!.value).toBe('2099-10-20');
    expect(element<HTMLInputElement>('loadingMeters')!.value).toBe('13.6');
    expect(element<HTMLInputElement>('palletCount')!.value).toBe('33');
    expect(element<HTMLSelectElement>('adrClass')!.value).toBe('4.1');
    expect(element<HTMLInputElement>('temperatureMinC')!.value).toBe('-18');
    expect(element<HTMLInputElement>('temperatureMaxC')!.value).toBe('-10');
    expect(element<HTMLSelectElement>('equipmentType')!.value).toBe('REEFER');
    expect(element('locked-fields-notice')).toBeNull();
  });

  it('disables Speichern until a valid change is made', async () => {
    await open('/tenders/1/edit', OPEN_TENDER);
    expect(saveButton().disabled).toBe(true);

    setValue('commodity', 'Paletten');
    expect(saveButton().disabled).toBe(false);

    setValue('commodity', '');
    expect(saveButton().disabled).toBe(true);

    setValue('commodity', OPEN_TENDER.commodity);
    expect(saveButton().disabled).toBe(true);
  });

  it('saves with a complete PUT, disables Speichern in flight and navigates to the detail page', async () => {
    const navigateSpy = vi.spyOn(TestBed.inject(Router), 'navigateByUrl');
    await open('/tenders/1/edit', OPEN_TENDER);

    setValue('commodity', 'Paletten');
    submit();
    expect(saveButton().disabled).toBe(true);

    const req = httpMock.expectOne('/api/tenders/1');
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual({
      origin: { country: 'DE', postalCode: '20457', city: 'Hamburg' },
      destination: { country: 'NL', postalCode: '3011 AA', city: 'Rotterdam' },
      pickupDate: '2099-10-20',
      deliveryDate: '2099-10-22',
      bidDeadline: '2099-10-16',
      commodity: 'Paletten',
      weightKg: 18500,
      loadingMeters: 13.6,
      palletCount: 33,
      equipmentType: 'CURTAIN_SIDER',
      dangerousGoods: false,
      temperatureControlled: false,
      currency: 'EUR',
    });
    req.flush(tenderSummary());

    expect(navigateSpy).toHaveBeenCalledWith('/tenders/1');
  });

  it('links Abbrechen and the back link to the detail page without a request', async () => {
    await open('/tenders/1/edit', OPEN_TENDER);

    expect(element('cancel')?.getAttribute('href')).toBe('/tenders/1');
    expect(element('back-link')?.getAttribute('href')).toBe('/tenders/1');
  });

  it('locks everything but the two deadlines for a tender with offers and still sends all data', async () => {
    await open('/tenders/1/edit', tenderDetail({ offers: [offerSummary()] }));

    expect(element('locked-fields-notice')).not.toBeNull();
    for (const testId of ['origin-city', 'pickupDate', 'commodity', 'currency', 'equipmentType']) {
      expect(element<HTMLInputElement>(testId)!.disabled).toBe(true);
    }
    expect(element<HTMLInputElement>('deliveryDate')!.disabled).toBe(false);
    expect(element<HTMLInputElement>('bidDeadline')!.disabled).toBe(false);

    setValue('deliveryDate', '2099-10-25');
    submit();

    const req = httpMock.expectOne('/api/tenders/1');
    expect(req.request.body).toMatchObject({
      commodity: 'Maschinenteile auf Europaletten',
      pickupDate: '2099-10-20',
      deliveryDate: '2099-10-25',
      currency: 'EUR',
    });
    req.flush(tenderSummary());
  });

  it('shows a German alert for a 409 and keeps the entered values', async () => {
    await open('/tenders/1/edit', OPEN_TENDER);
    setValue('commodity', 'Paletten');
    submit();
    httpMock.expectOne('/api/tenders/1').flush({}, { status: 409, statusText: 'Conflict' });
    harness.detectChanges();

    const error = element('submit-error')!;
    expect(error.getAttribute('role')).toBe('alert');
    expect(error.textContent).toContain('nicht mehr in dieser Form geändert');
    expect(element<HTMLInputElement>('commodity')!.value).toBe('Paletten');
    expect(saveButton().disabled).toBe(false);
  });

  it('shows a generic German alert for any other failure and keeps the entered values', async () => {
    await open('/tenders/1/edit', OPEN_TENDER);
    setValue('commodity', 'Paletten');
    submit();
    httpMock.expectOne('/api/tenders/1').flush({}, { status: 500, statusText: 'Server Error' });
    harness.detectChanges();

    const error = element('submit-error')!;
    expect(error.getAttribute('role')).toBe('alert');
    expect(error.textContent).toContain('konnten nicht gespeichert werden');
    expect(element<HTMLInputElement>('commodity')!.value).toBe('Paletten');
  });

  it('checks today-or-later only for dates that changed', async () => {
    await open(
      '/tenders/1/edit',
      tenderDetail({
        pickupDate: '2020-01-10',
        deliveryDate: '2020-01-12',
        bidDeadline: '2020-01-05',
      }),
    );

    // The stored past dates are accepted while untouched ...
    setValue('commodity', 'Paletten');
    expect(element('pickupDate-error')).toBeNull();
    expect(element('bidDeadline-error')).toBeNull();
    expect(saveButton().disabled).toBe(false);

    // ... but a different past date is not.
    setValue('bidDeadline', '2020-01-06');
    expect(element('bidDeadline-error')?.textContent).toContain('Vergangenheit');
    expect(saveButton().disabled).toBe(true);
  });

  it('enables the conditional fields when their checkbox is checked on the edit page', async () => {
    await open('/tenders/1/edit', OPEN_TENDER);

    expect(element('adrClass')).toBeNull();
    setChecked('dangerousGoods', true);
    expect(element('adrClass')).not.toBeNull();
  });
});
