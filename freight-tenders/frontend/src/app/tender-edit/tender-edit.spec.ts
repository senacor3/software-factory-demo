import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { TenderDetail } from '../tender-api';
import { offerSummary, tenderDetail, tenderSummary } from '../tender-test-data';
import { TenderEdit } from './tender-edit';

const OPEN_TENDER: TenderDetail = tenderDetail();
const TENDER_WITH_OFFERS: TenderDetail = tenderDetail({ offers: [offerSummary()] });
const SPECIAL_TENDER: TenderDetail = tenderDetail({
  equipmentType: 'REEFER',
  dangerousGoods: true,
  adrClass: '3',
  temperatureControlled: true,
  temperatureMinC: -18,
  temperatureMaxC: -5,
});
const PAST_TENDER: TenderDetail = tenderDetail({
  pickupDate: '2020-01-10',
  deliveryDate: '2020-01-12',
  bidDeadline: '2020-01-05',
});

describe('TenderEdit', () => {
  let httpMock: HttpTestingController;
  let harness: RouterTestingHarness;
  let router: Router;

  async function open(url = '/tenders/1/edit'): Promise<HTMLElement> {
    harness = await RouterTestingHarness.create(url);
    return harness.routeNativeElement as HTMLElement;
  }

  async function render(tender: TenderDetail): Promise<HTMLElement> {
    const element = await open();
    httpMock.expectOne('/api/tenders/1').flush(tender);
    harness.detectChanges();
    return element;
  }

  function el<T extends HTMLElement>(root: HTMLElement, testId: string): T | null {
    return root.querySelector<T>(`[data-testid="${testId}"]`);
  }

  function setValue(root: HTMLElement, testId: string, value: string): void {
    const control = el<HTMLInputElement | HTMLSelectElement>(root, testId)!;
    control.value = value;
    control.dispatchEvent(new Event(control instanceof HTMLSelectElement ? 'change' : 'input'));
    harness.detectChanges();
  }

  function submit(root: HTMLElement): void {
    root.querySelector('form')!.dispatchEvent(new Event('submit'));
    harness.detectChanges();
  }

  function saveButton(root: HTMLElement): HTMLButtonElement {
    return el<HTMLButtonElement>(root, 'submit')!;
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([{ path: 'tenders/:id/edit', component: TenderEdit }]),
      ],
    }).compileComponents();

    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('shows a German loading message and the back link before the response arrives', async () => {
    const element = await open();

    expect(el(element, 'loading')?.textContent).toContain('Ausschreibung wird geladen');
    expect(el(element, 'back-link')?.getAttribute('href')).toBe('/tenders/1');
    httpMock.expectOne('/api/tenders/1').flush(OPEN_TENDER);
  });

  it('shows the load error and the back link when the tender cannot be loaded', async () => {
    const element = await open();
    httpMock.expectOne('/api/tenders/1').flush(null, { status: 404, statusText: 'Not Found' });
    harness.detectChanges();

    expect(el(element, 'load-error')?.textContent).toContain('nicht gefunden');
    expect(el(element, 'back-link')).not.toBeNull();
    expect(el(element, 'submit')).toBeNull();
  });

  it('shows the load error without a request when the route id is not a number', async () => {
    const element = await open('/tenders/abc/edit');

    expect(el(element, 'load-error')).not.toBeNull();
    expect(el(element, 'back-link')?.getAttribute('href')).toBe('/tenders/abc');
  });

  it('shows not-editable and no form for awarded and closed tenders', async () => {
    for (const status of ['AWARDED', 'CLOSED'] as const) {
      const element = await render({ ...OPEN_TENDER, status });

      expect(el(element, 'not-editable')).not.toBeNull();
      expect(element.querySelector('form')).toBeNull();
      expect(el(element, 'back-link')).not.toBeNull();
    }
  });

  it('prefills the form with the stored values including ADR class and temperature range', async () => {
    const element = await render(SPECIAL_TENDER);

    expect(el<HTMLInputElement>(element, 'origin-city')!.value).toBe('Hamburg');
    expect(el<HTMLInputElement>(element, 'commodity')!.value).toBe(SPECIAL_TENDER.commodity);
    expect(el<HTMLInputElement>(element, 'weightKg')!.value).toBe('18500');
    expect(el<HTMLSelectElement>(element, 'equipmentType')!.value).toBe('REEFER');
    expect(el<HTMLInputElement>(element, 'dangerousGoods')!.checked).toBe(true);
    expect(el<HTMLSelectElement>(element, 'adrClass')!.value).toBe('3');
    expect(el<HTMLInputElement>(element, 'temperatureMinC')!.value).toBe('-18');
    expect(el<HTMLInputElement>(element, 'temperatureMaxC')!.value).toBe('-5');
    expect(saveButton(element).textContent?.trim()).toBe('Speichern');
  });

  it('disables Speichern while unchanged or invalid and enables it for a valid change', async () => {
    const element = await render(OPEN_TENDER);

    expect(saveButton(element).disabled).toBe(true);

    setValue(element, 'commodity', 'Andere Ware');
    expect(saveButton(element).disabled).toBe(false);

    setValue(element, 'commodity', '');
    expect(saveButton(element).disabled).toBe(true);

    setValue(element, 'commodity', OPEN_TENDER.commodity);
    expect(saveButton(element).disabled).toBe(true);
  });

  it('disables Speichern while the save is in flight and ignores a second submit', async () => {
    const element = await render(OPEN_TENDER);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
    setValue(element, 'commodity', 'Andere Ware');

    submit(element);
    submit(element);

    expect(saveButton(element).disabled).toBe(true);
    const request = httpMock.expectOne('/api/tenders/1');
    expect(request.request.method).toBe('PUT');
    request.flush(tenderSummary());
  });

  it('shows the locked-fields notice and enables only the two dates when the tender has offers', async () => {
    const element = await render(TENDER_WITH_OFFERS);

    expect(el(element, 'locked-fields-notice')).not.toBeNull();
    const enabled = Array.from(
      element.querySelectorAll<HTMLInputElement>('input, select'),
    ).filter((control) => !control.disabled);
    expect(enabled.map((control) => control.id).sort()).toEqual(['bidDeadline', 'deliveryDate']);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);

    setValue(element, 'deliveryDate', '2099-10-25');
    submit(element);

    const request = httpMock.expectOne('/api/tenders/1');
    expect(request.request.body).toEqual({
      origin: TENDER_WITH_OFFERS.origin,
      destination: TENDER_WITH_OFFERS.destination,
      pickupDate: '2099-10-20',
      deliveryDate: '2099-10-25',
      bidDeadline: '2099-10-16',
      commodity: TENDER_WITH_OFFERS.commodity,
      weightKg: 18500,
      loadingMeters: 13.6,
      palletCount: 33,
      equipmentType: 'CURTAIN_SIDER',
      dangerousGoods: false,
      temperatureControlled: false,
      currency: 'EUR',
    });
    request.flush(tenderSummary());
  });

  it('shows no locked-fields notice for a tender without offers', async () => {
    const element = await render(OPEN_TENDER);

    expect(el(element, 'locked-fields-notice')).toBeNull();
    expect(el<HTMLInputElement>(element, 'commodity')!.disabled).toBe(false);
  });

  it('accepts a past date equal to the loaded value but rejects a changed past date', async () => {
    const element = await render(PAST_TENDER);

    setValue(element, 'commodity', 'Andere Ware');
    el(element, 'pickupDate')!.dispatchEvent(new Event('blur'));
    harness.detectChanges();
    expect(el(element, 'pickupDate-error')).toBeNull();
    expect(saveButton(element).disabled).toBe(false);

    setValue(element, 'pickupDate', '2020-01-11');
    el(element, 'pickupDate')!.dispatchEvent(new Event('blur'));
    harness.detectChanges();
    expect(el(element, 'pickupDate-error')?.textContent).toContain('Vergangenheit');
    expect(saveButton(element).disabled).toBe(true);
  });

  it('navigates to the detail page after a successful save', async () => {
    const element = await render(OPEN_TENDER);
    const navigateSpy = vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
    setValue(element, 'commodity', 'Andere Ware');

    submit(element);
    httpMock.expectOne('/api/tenders/1').flush(tenderSummary());

    expect(navigateSpy).toHaveBeenCalledWith('/tenders/1');
  });

  it('shows the conflict alert and keeps the entered values on a 409', async () => {
    const element = await render(OPEN_TENDER);
    setValue(element, 'commodity', 'Andere Ware');

    submit(element);
    httpMock.expectOne('/api/tenders/1').flush(null, { status: 409, statusText: 'Conflict' });
    harness.detectChanges();

    const alert = el(element, 'submit-error')!;
    expect(alert.getAttribute('role')).toBe('alert');
    expect(alert.textContent).toContain('nicht mehr in dieser Form geändert');
    expect(el<HTMLInputElement>(element, 'commodity')!.value).toBe('Andere Ware');
    expect(saveButton(element).disabled).toBe(false);
  });

  it('shows the generic save error and keeps the entered values on other failures', async () => {
    const element = await render(OPEN_TENDER);
    setValue(element, 'commodity', 'Andere Ware');

    submit(element);
    httpMock.expectOne('/api/tenders/1').flush(null, { status: 500, statusText: 'Server Error' });
    harness.detectChanges();

    expect(el(element, 'submit-error')?.textContent).toContain('nicht gespeichert werden');
    expect(el<HTMLInputElement>(element, 'commodity')!.value).toBe('Andere Ware');
  });

  it('links Abbrechen and the back link to the detail page without any request', async () => {
    const element = await render(OPEN_TENDER);

    expect(el(element, 'cancel')?.getAttribute('href')).toBe('/tenders/1');
    expect(el(element, 'back-link')?.getAttribute('href')).toBe('/tenders/1');
  });
});
