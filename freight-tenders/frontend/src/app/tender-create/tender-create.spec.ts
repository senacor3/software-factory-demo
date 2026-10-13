import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { tenderSummary } from '../tender-test-data';
import { TenderCreate } from './tender-create';
import { todayIso } from './tender-create-validators';

describe('TenderCreate', () => {
  let component: TenderCreate;
  let fixture: ComponentFixture<TenderCreate>;
  let httpMock: HttpTestingController;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TenderCreate],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(TenderCreate);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    router = TestBed.inject(Router);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  const root = () => fixture.nativeElement as HTMLElement;

  function element<T extends HTMLElement>(testId: string): T | null {
    return root().querySelector<T>(`[data-testid="${testId}"]`);
  }

  function setValue(testId: string, value: string): void {
    const control = element<HTMLInputElement | HTMLSelectElement>(testId)!;
    control.value = value;
    control.dispatchEvent(new Event(control instanceof HTMLSelectElement ? 'change' : 'input'));
    fixture.detectChanges();
  }

  function setChecked(testId: string, checked: boolean): void {
    const checkbox = element<HTMLInputElement>(testId)!;
    checkbox.checked = checked;
    checkbox.dispatchEvent(new Event('change'));
    fixture.detectChanges();
  }

  function touch(testId: string): void {
    element(testId)!.dispatchEvent(new Event('blur'));
    fixture.detectChanges();
  }

  function errorOf(testId: string): string | null {
    return element(`${testId}-error`)?.textContent?.trim() ?? null;
  }

  function submitButton(): HTMLButtonElement {
    return element<HTMLButtonElement>('submit')!;
  }

  function fillValidForm(): void {
    setValue('origin-postalCode', '20457');
    setValue('origin-city', 'Hamburg');
    setValue('destination-country', 'NL');
    setValue('destination-postalCode', '3011 AA');
    setValue('destination-city', 'Rotterdam');
    setValue('pickupDate', '2099-10-20');
    setValue('deliveryDate', '2099-10-22');
    setValue('commodity', 'Maschinenteile auf Europaletten');
    setValue('weightKg', '18500');
    setValue('loadingMeters', '13.6');
    setValue('palletCount', '33');
    setValue('equipmentType', 'CURTAIN_SIDER');
    setValue('bidDeadline', '2099-10-16');
  }

  function submit(): void {
    root().querySelector('form')!.dispatchEvent(new Event('submit'));
    fixture.detectChanges();
  }

  const FULL_REQUEST = {
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
    temperatureControlled: false,
    currency: 'EUR',
  };

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('shows the five field groups in the specified order', () => {
    const fieldsets = Array.from(root().querySelectorAll('fieldset'));

    expect(fieldsets.map((fieldset) => fieldset.querySelector('legend')?.textContent?.trim())).toEqual([
      'Strecke',
      'Termine',
      'Ladung',
      'Fahrzeug',
      'Ausschreibung',
    ]);
  });

  it('preselects Germany for both addresses and the euro as currency', () => {
    expect(element<HTMLSelectElement>('origin-country')!.value).toBe('DE');
    expect(element<HTMLSelectElement>('destination-country')!.value).toBe('DE');
    expect(element<HTMLSelectElement>('currency')!.value).toBe('EUR');
  });

  it('offers the thirteen countries with German names and the five vehicle types', () => {
    const countries = Array.from(element<HTMLSelectElement>('origin-country')!.options);
    expect(countries.length).toBe(13);
    expect(countries[0].textContent?.trim()).toBe('Deutschland');

    const vehicles = Array.from(element<HTMLSelectElement>('equipmentType')!.options).map((option) =>
      option.textContent?.trim(),
    );
    expect(vehicles).toContain('Planenauflieger');
    expect(vehicles).toContain('Kühlauflieger');
  });

  it('uses date inputs for the three dates', () => {
    for (const testId of ['pickupDate', 'deliveryDate', 'bidDeadline']) {
      expect(element<HTMLInputElement>(testId)!.type).toBe('date');
    }
  });

  it('renders ADR-Klasse only while Gefahrgut (ADR) is checked', () => {
    expect(element('adrClass')).toBeNull();

    setChecked('dangerousGoods', true);
    expect(element('adrClass')).not.toBeNull();

    setChecked('dangerousGoods', false);
    expect(element('adrClass')).toBeNull();
  });

  it('renders the two temperature fields only while Temperaturgeführt is checked', () => {
    expect(element('temperatureMinC')).toBeNull();
    expect(element('temperatureMaxC')).toBeNull();

    setChecked('temperatureControlled', true);
    expect(element('temperatureMinC')).not.toBeNull();
    expect(element('temperatureMaxC')).not.toBeNull();

    setChecked('temperatureControlled', false);
    expect(element('temperatureMinC')).toBeNull();
    expect(element('temperatureMaxC')).toBeNull();
  });

  it('creates the tender with the full request and navigates to / on success', () => {
    const navigateSpy = vi.spyOn(router, 'navigateByUrl');

    fillValidForm();
    submit();

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(FULL_REQUEST);
    req.flush(tenderSummary());

    expect(navigateSpy).toHaveBeenCalledWith('/');
  });

  it('sends the ADR class and the temperature range of a checked option', () => {
    fillValidForm();
    setChecked('dangerousGoods', true);
    setValue('adrClass', '4.1');
    setChecked('temperatureControlled', true);
    setValue('equipmentType', 'REEFER');
    setValue('temperatureMinC', '-18');
    setValue('temperatureMaxC', '-10');
    setValue('currency', 'CHF');
    submit();

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.body).toEqual({
      ...FULL_REQUEST,
      equipmentType: 'REEFER',
      dangerousGoods: true,
      adrClass: '4.1',
      temperatureControlled: true,
      temperatureMinC: -18,
      temperatureMaxC: -10,
      currency: 'CHF',
    });
    req.flush(tenderSummary());
  });

  it('leaves the values of an unchecked option out of the request', () => {
    fillValidForm();
    setChecked('dangerousGoods', true);
    setValue('adrClass', '3');
    setChecked('temperatureControlled', true);
    setValue('equipmentType', 'REEFER');
    setValue('temperatureMinC', '2');
    setValue('temperatureMaxC', '8');

    setChecked('dangerousGoods', false);
    setChecked('temperatureControlled', false);
    setValue('equipmentType', 'CURTAIN_SIDER');
    submit();

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.body).toEqual(FULL_REQUEST);
    req.flush(tenderSummary());
  });

  it('omits the optional pallet count when it is empty', () => {
    fillValidForm();
    setValue('palletCount', '');
    submit();

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.body).not.toHaveProperty('palletCount');
    req.flush(tenderSummary());
  });

  it('shows no error under a field that has not been touched', () => {
    setValue('commodity', '');

    expect(errorOf('commodity')).toBeNull();
    expect(errorOf('origin-city')).toBeNull();
  });

  it('shows a German message under a touched, invalid field', () => {
    touch('commodity');
    touch('origin-postalCode');
    touch('weightKg');

    expect(errorOf('commodity')).toBe('Dieses Feld ist erforderlich.');
    expect(errorOf('origin-postalCode')).toBe('Dieses Feld ist erforderlich.');
    expect(errorOf('weightKg')).toBe('Dieses Feld ist erforderlich.');
  });

  it('rejects values outside the ranges of the backend rules', () => {
    setValue('origin-postalCode', '12345678901');
    touch('origin-postalCode');
    setValue('weightKg', '40001');
    touch('weightKg');
    setValue('loadingMeters', '13.7');
    touch('loadingMeters');
    setValue('palletCount', '67');
    touch('palletCount');

    expect(errorOf('origin-postalCode')).toBe('Es sind höchstens 10 Zeichen erlaubt.');
    expect(errorOf('weightKg')).toBe('Der Wert darf höchstens 40000 betragen.');
    expect(errorOf('loadingMeters')).toBe('Der Wert darf höchstens 13.6 betragen.');
    expect(errorOf('palletCount')).toBe('Der Wert darf höchstens 66 betragen.');

    setValue('weightKg', '0');
    setValue('loadingMeters', '1.25');
    expect(errorOf('weightKg')).toBe('Der Wert muss mindestens 1 betragen.');
    expect(errorOf('loadingMeters')).toBe('Es ist höchstens eine Nachkommastelle erlaubt.');
  });

  it('shows the delivery-before-pickup message under Zustellung bis', () => {
    setValue('pickupDate', '2099-10-20');
    setValue('deliveryDate', '2099-10-19');
    touch('deliveryDate');

    expect(errorOf('deliveryDate')).toBe('Die Zustellung darf nicht vor der Abholung liegen.');

    setValue('deliveryDate', '2099-10-20');
    expect(errorOf('deliveryDate')).toBeNull();
  });

  it('checks the delivery date again when the pickup date changes', () => {
    setValue('pickupDate', '2099-10-20');
    setValue('deliveryDate', '2099-10-21');
    touch('deliveryDate');
    expect(errorOf('deliveryDate')).toBeNull();

    setValue('pickupDate', '2099-10-25');

    expect(errorOf('deliveryDate')).toBe('Die Zustellung darf nicht vor der Abholung liegen.');
  });

  it('rejects a pickup in the past but accepts today', () => {
    setValue('pickupDate', '2000-01-01');
    touch('pickupDate');
    expect(errorOf('pickupDate')).toBe('Die Abholung darf nicht in der Vergangenheit liegen.');

    setValue('pickupDate', todayIso());
    expect(errorOf('pickupDate')).toBeNull();
  });

  it('rejects a bid deadline in the past or after the pickup, and accepts the pickup day', () => {
    setValue('pickupDate', '2099-10-20');
    setValue('bidDeadline', '2000-01-01');
    touch('bidDeadline');
    expect(errorOf('bidDeadline')).toBe(
      'Die Angebotsfrist darf nicht in der Vergangenheit liegen.',
    );

    setValue('bidDeadline', '2099-10-21');
    expect(errorOf('bidDeadline')).toBe('Die Angebotsfrist darf nicht nach der Abholung liegen.');

    setValue('bidDeadline', '2099-10-20');
    expect(errorOf('bidDeadline')).toBeNull();
  });

  it('requires an ADR class once Gefahrgut (ADR) is checked', () => {
    setChecked('dangerousGoods', true);
    touch('adrClass');

    expect(errorOf('adrClass')).toBe('Dieses Feld ist erforderlich.');
  });

  it('reports a temperature range whose minimum is above its maximum under both fields', () => {
    setChecked('temperatureControlled', true);
    setValue('temperatureMinC', '10');
    touch('temperatureMinC');
    setValue('temperatureMaxC', '5');
    touch('temperatureMaxC');

    const message = 'Die Temperatur von darf nicht über der Temperatur bis liegen.';
    expect(errorOf('temperatureMinC')).toBe(message);
    expect(errorOf('temperatureMaxC')).toBe(message);

    setValue('temperatureMaxC', '10');
    expect(errorOf('temperatureMinC')).toBeNull();
    expect(errorOf('temperatureMaxC')).toBeNull();
  });

  it('rejects temperatures outside -30 to 30 °C', () => {
    setChecked('temperatureControlled', true);
    setValue('temperatureMinC', '-31');
    touch('temperatureMinC');
    setValue('temperatureMaxC', '31');
    touch('temperatureMaxC');

    expect(errorOf('temperatureMinC')).toBe('Der Wert muss mindestens -30 betragen.');
    expect(errorOf('temperatureMaxC')).toBe('Der Wert darf höchstens 30 betragen.');
  });

  it('requires a Kühlauflieger for a temperature-controlled load, under Fahrzeugtyp', () => {
    setValue('equipmentType', 'CURTAIN_SIDER');
    touch('equipmentType');
    expect(errorOf('equipmentType')).toBeNull();

    setChecked('temperatureControlled', true);
    expect(errorOf('equipmentType')).toBe('Temperaturgeführte Ladung erfordert einen Kühlauflieger.');

    setValue('equipmentType', 'REEFER');
    expect(errorOf('equipmentType')).toBeNull();
  });

  it('keeps Erstellen disabled until the form is valid', () => {
    expect(submitButton().disabled).toBe(true);

    fillValidForm();
    expect(submitButton().disabled).toBe(false);

    setValue('commodity', '');
    expect(submitButton().disabled).toBe(true);
  });

  it('keeps Erstellen disabled while a request is in flight and sends it only once', () => {
    fillValidForm();
    submit();

    expect(submitButton().disabled).toBe(true);
    submit();

    const req = httpMock.expectOne('/api/tenders');
    req.flush(tenderSummary());
  });

  it('shows a German error and keeps every entered value when creation fails', () => {
    const navigateSpy = vi.spyOn(router, 'navigateByUrl');

    fillValidForm();
    submit();

    httpMock.expectOne('/api/tenders').error(new ProgressEvent('error'));
    fixture.detectChanges();

    expect(element('submit-error')?.textContent).toContain('konnte nicht erstellt werden');
    expect(navigateSpy).not.toHaveBeenCalled();
    expect(element<HTMLInputElement>('origin-city')!.value).toBe('Hamburg');
    expect(element<HTMLInputElement>('commodity')!.value).toBe('Maschinenteile auf Europaletten');
    expect(element<HTMLSelectElement>('destination-country')!.value).toBe('NL');
    expect(submitButton().disabled).toBe(false);
  });

  it('does not submit while the form is invalid, but shows what is missing', () => {
    submit();

    // httpMock.expectNone throws if a matching request was made; wrapping it in an explicit
    // expect(...).not.toThrow() keeps that same check but as a recognized assertion (plain
    // httpMock.expectNone(...) isn't picked up by eslint-plugin-sonarjs's assertions-in-tests
    // rule, part of the new static_analysis check).
    expect(() => httpMock.expectNone('/api/tenders')).not.toThrow();
    expect(errorOf('commodity')).toBe('Dieses Feld ist erforderlich.');
  });
});
