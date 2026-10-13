import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { TenderDetail as TenderDetailModel } from '../tender-api';
import { offerSummary, tenderDetail, tenderSummary } from '../tender-test-data';
import { formatDate, localToday } from '../tender-format';
import { TenderDetail } from './tender-detail';

const BERLIN = { country: 'DE', postalCode: '10115', city: 'Berlin' };

const OPEN_TENDER: TenderDetailModel = tenderDetail({
  destination: BERLIN,
  remarks: [{ id: 10, text: 'Bestehende Bemerkung' }],
  offers: [offerSummary({ id: 20, supplierName: 'Spedition Muster', amount: 500 })],
});

const CLOSED_TENDER: TenderDetailModel = {
  ...OPEN_TENDER,
  status: 'CLOSED',
};

const SORTABLE_TENDER: TenderDetailModel = tenderDetail({
  remarks: [
    { id: 10, text: 'Bitte schnell liefern' },
    { id: 11, text: 'Angebot angenommen' },
    { id: 12, text: 'Zoll beachten' },
  ],
  offers: [
    offerSummary({ id: 20, supplierName: 'Spedition Muster', amount: 980 }),
    offerSummary({ id: 21, supplierName: 'Acme Logistics', amount: 1234.56 }),
    offerSummary({ id: 22, supplierName: 'Nordfracht', amount: 99 }),
  ],
});

const EMPTY_TENDER: TenderDetailModel = {
  ...OPEN_TENDER,
  remarks: [],
  offers: [],
};

describe('TenderDetail', () => {
  let httpMock: HttpTestingController;
  let harness: RouterTestingHarness;

  async function render(tender: TenderDetailModel): Promise<HTMLElement> {
    harness = await RouterTestingHarness.create('/tenders/1');
    httpMock.expectOne('/api/tenders/1').flush(tender);
    harness.detectChanges();

    return harness.routeNativeElement as HTMLElement;
  }

  function texts(element: HTMLElement, testId: string): string[] {
    return Array.from(element.querySelectorAll(`[data-testid="${testId}"]`)).map(
      (node) => node.textContent?.trim() ?? '',
    );
  }

  function sortBy(element: HTMLElement, table: string, column: string): void {
    element.querySelector<HTMLButtonElement>(`[data-testid="${table}-sort-${column}"]`)!.click();
    harness.detectChanges();
  }

  function ariaSortOf(element: HTMLElement, table: string, column: string): string | null {
    return (
      element
        .querySelector(`[data-testid="${table}-header-${column}"]`)
        ?.getAttribute('aria-sort') ?? null
    );
  }

  function sortButtonText(element: HTMLElement, table: string, column: string): string {
    return (
      element.querySelector(`[data-testid="${table}-sort-${column}"]`)?.textContent?.trim() ?? ''
    );
  }

  function fill(element: HTMLElement, testId: string, value: string): void {
    const input = element.querySelector<HTMLInputElement>(`[data-testid="${testId}"]`)!;
    input.value = value;
    input.dispatchEvent(new Event('input'));
    harness.detectChanges();
  }

  function fillOfferTerms(element: HTMLElement): void {
    fill(element, 'offer-delivery-date-input', '2099-10-21');
    fill(element, 'offer-valid-until-input', '2099-10-30');
  }

  function submitFormOf(element: HTMLElement, testId: string): void {
    element
      .querySelector(`[data-testid="${testId}"]`)!
      .closest('form')!
      .dispatchEvent(new Event('submit'));
    harness.detectChanges();
  }

  function isBefore(first: Element, second: Element): boolean {
    return (first.compareDocumentPosition(second) & Node.DOCUMENT_POSITION_FOLLOWING) !== 0;
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        provideRouter([
          { path: '', component: TenderDetail },
          { path: 'tenders/:id', component: TenderDetail },
        ]),
      ],
    }).compileComponents();

    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  function backLink(element: HTMLElement): HTMLAnchorElement | null {
    return element.querySelector<HTMLAnchorElement>('[data-testid="back-link"]');
  }

  it('shows the back link while loading, before the response arrives', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');
    const element = harness.routeNativeElement as HTMLElement;

    expect(backLink(element)?.getAttribute('href')).toBe('/');
    expect(backLink(element)?.textContent).toContain('Zurück zur Übersicht');
    expect(element.querySelector('main')?.firstElementChild).toBe(backLink(element));

    httpMock.expectOne('/api/tenders/1').flush(OPEN_TENDER);
  });

  it('shows the back link when the tender cannot be loaded', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');
    httpMock.expectOne('/api/tenders/1').flush('nope', { status: 404, statusText: 'Not Found' });
    harness.detectChanges();

    const element = harness.routeNativeElement as HTMLElement;
    expect(element.querySelector('[data-testid="load-error"]')).not.toBeNull();
    expect(backLink(element)?.getAttribute('href')).toBe('/');
  });

  it('shows the back link when the route id is not a number', async () => {
    const harness = await RouterTestingHarness.create('/tenders/abc');

    const element = harness.routeNativeElement as HTMLElement;
    expect(backLink(element)?.getAttribute('href')).toBe('/');
    expect(element.querySelector('main')?.firstElementChild).toBe(backLink(element));
  });

  it('shows the back link as the first element in main for an open tender', async () => {
    const element = await render(OPEN_TENDER);

    expect(element.querySelector('main')?.firstElementChild).toBe(backLink(element));
  });

  it('shows the back link as the first element in main for a closed tender', async () => {
    const element = await render(CLOSED_TENDER);

    expect(element.querySelector('main')?.firstElementChild).toBe(backLink(element));
  });

  it('navigates to the overview when the back link is clicked', async () => {
    const element = await render(OPEN_TENDER);

    backLink(element)!.click();
    await harness.fixture.whenStable();

    expect(TestBed.inject(Router).url).toBe('/');
  });

  it('shows a German loading message before the response arrives', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');

    const element = harness.routeNativeElement as HTMLElement;
    expect(element.querySelector('[data-testid="loading"]')?.textContent).toContain('wird geladen');

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

    element
      .querySelector('[data-testid="remark-input"]')!
      .closest('form')!
      .dispatchEvent(new Event('submit'));

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
    fill(element, 'offer-delivery-date-input', '2099-10-21');
    fill(element, 'offer-valid-until-input', '2099-10-30');
    fill(element, 'offer-note-input', 'Inkl. Maut');

    element
      .querySelector('[data-testid="offer-supplier-input"]')!
      .closest('form')!
      .dispatchEvent(new Event('submit'));

    const offerReq = httpMock.expectOne('/api/tenders/1/offers');
    expect(offerReq.request.body).toEqual({
      supplierName: 'Neuer Anbieter',
      amount: 750,
      deliveryDate: '2099-10-21',
      validUntil: '2099-10-30',
      note: 'Inkl. Maut',
    });
    offerReq.flush(offerSummary({ id: 21, supplierName: 'Neuer Anbieter', amount: 750 }));
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
    expect(element.querySelector('[data-testid="status"]')?.textContent).toContain('Geschlossen');
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

  it('shows the route as the page heading and the status as a German pill, never the raw enum', async () => {
    const element = await render(SORTABLE_TENDER);

    expect(element.querySelector('[data-testid="page-title"]')?.textContent).toContain(
      'Hamburg → Rotterdam',
    );
    expect(texts(element, 'status')).toEqual(['Offen']);
    expect(element.querySelector('[data-testid="page-title"]')?.textContent).not.toContain(
      '[object Object]',
    );
  });

  it('orders remarks and offers newest-first with no sort indicator until a column is selected', async () => {
    const element = await render(SORTABLE_TENDER);

    expect(texts(element, 'remarks-row')).toEqual([
      'Zoll beachten',
      'Angebot angenommen',
      'Bitte schnell liefern',
    ]);
    expect(texts(element, 'offer-amount')).toEqual([
      '99,00\u00a0€',
      '1.234,56\u00a0€',
      '980,00\u00a0€',
    ]);

    expect(ariaSortOf(element, 'remarks', 'text')).toBe('none');
    expect(ariaSortOf(element, 'offers', 'supplierName')).toBe('none');
    expect(ariaSortOf(element, 'offers', 'amount')).toBe('none');
    expect(sortButtonText(element, 'remarks', 'text')).toBe('Bemerkung');
    expect(sortButtonText(element, 'offers', 'supplierName')).toBe('Anbieter');
    expect(sortButtonText(element, 'offers', 'amount')).toBe('Betrag (EUR)');
  });

  it('sorts remarks ascending when the header is selected, and descending when selected again', async () => {
    const element = await render(SORTABLE_TENDER);

    sortBy(element, 'remarks', 'text');

    expect(texts(element, 'remarks-row')).toEqual([
      'Angebot angenommen',
      'Bitte schnell liefern',
      'Zoll beachten',
    ]);
    expect(ariaSortOf(element, 'remarks', 'text')).toBe('ascending');
    expect(sortButtonText(element, 'remarks', 'text')).toContain('▲');

    sortBy(element, 'remarks', 'text');

    expect(texts(element, 'remarks-row')).toEqual([
      'Zoll beachten',
      'Bitte schnell liefern',
      'Angebot angenommen',
    ]);
    expect(ariaSortOf(element, 'remarks', 'text')).toBe('descending');
    expect(sortButtonText(element, 'remarks', 'text')).toContain('▼');
  });

  it('sorts offers by amount numerically, not as strings, showing German euro amounts', async () => {
    const element = await render(SORTABLE_TENDER);

    sortBy(element, 'offers', 'amount');

    expect(texts(element, 'offer-amount')).toEqual([
      '99,00\u00a0€',
      '980,00\u00a0€',
      '1.234,56\u00a0€',
    ]);
    expect(ariaSortOf(element, 'offers', 'amount')).toBe('ascending');
    expect(sortButtonText(element, 'offers', 'amount')).toContain('▲');
    expect(ariaSortOf(element, 'offers', 'supplierName')).toBe('none');
    expect(sortButtonText(element, 'offers', 'supplierName')).toBe('Anbieter');

    sortBy(element, 'offers', 'amount');

    expect(texts(element, 'offer-amount')).toEqual([
      '1.234,56\u00a0€',
      '980,00\u00a0€',
      '99,00\u00a0€',
    ]);
    expect(ariaSortOf(element, 'offers', 'amount')).toBe('descending');
    expect(sortButtonText(element, 'offers', 'amount')).toContain('▼');
  });

  it('switches the offers sort to a newly selected column ascending and clears the previous header', async () => {
    const element = await render(SORTABLE_TENDER);

    sortBy(element, 'offers', 'amount');
    sortBy(element, 'offers', 'amount');
    sortBy(element, 'offers', 'supplierName');

    // Acme Logistics, Nordfracht, Spedition Muster
    expect(texts(element, 'offer-amount')).toEqual([
      '1.234,56\u00a0€',
      '99,00\u00a0€',
      '980,00\u00a0€',
    ]);
    expect(ariaSortOf(element, 'offers', 'supplierName')).toBe('ascending');
    expect(sortButtonText(element, 'offers', 'supplierName')).toContain('▲');
    expect(ariaSortOf(element, 'offers', 'amount')).toBe('none');
    expect(sortButtonText(element, 'offers', 'amount')).toBe('Betrag (EUR)');
  });

  it('sorts the remarks and offers tables independently of each other', async () => {
    const element = await render(SORTABLE_TENDER);

    sortBy(element, 'offers', 'amount');

    expect(ariaSortOf(element, 'remarks', 'text')).toBe('none');
    expect(texts(element, 'remarks-row')[0]).toBe('Zoll beachten');
  });

  it('makes every sort header a real button, so Tab + Enter/Space trigger it like a click', async () => {
    const element = await render(SORTABLE_TENDER);

    for (const [table, column] of [
      ['remarks', 'text'],
      ['offers', 'supplierName'],
      ['offers', 'amount'],
    ]) {
      const button = element.querySelector<HTMLButtonElement>(
        `[data-testid="${table}-sort-${column}"]`,
      );
      expect(button?.tagName).toBe('BUTTON');
      expect(button?.type).toBe('button');
      expect(button?.disabled).toBe(false);
      expect(button?.tabIndex).toBe(0);
      expect(ariaSortOf(element, table, column)).toBe('none');
    }
  });

  it('still renders the sortable header rows when a tender has no remarks or offers, with the empty messages in the table bodies', async () => {
    const element = await render(EMPTY_TENDER);

    expect(sortButtonText(element, 'remarks', 'text')).toBe('Bemerkung');
    expect(sortButtonText(element, 'offers', 'supplierName')).toBe('Anbieter');
    expect(sortButtonText(element, 'offers', 'amount')).toBe('Betrag (EUR)');

    const remarksEmpty = element.querySelector('[data-testid="remarks-empty"]');
    const offersEmpty = element.querySelector('[data-testid="offers-empty"]');
    expect(remarksEmpty?.tagName).toBe('TD');
    expect(remarksEmpty?.textContent).toContain('Keine Bemerkungen vorhanden.');
    expect(element.querySelector('[data-testid="remarks"]')?.contains(remarksEmpty ?? null)).toBe(
      true,
    );
    expect(offersEmpty?.getAttribute('colspan')).toBe('6');
    expect(offersEmpty?.textContent).toContain('Keine Angebote vorhanden.');
  });

  it('puts a newly added remark and offer at the top while no column is sorted', async () => {
    const element = await render(SORTABLE_TENDER);

    fill(element, 'remark-input', 'Mittlere Bemerkung');
    submitFormOf(element, 'remark-input');
    httpMock.expectOne('/api/tenders/1/remarks').flush({ id: 13, text: 'Mittlere Bemerkung' });
    harness.detectChanges();

    expect(texts(element, 'remarks-row')[0]).toBe('Mittlere Bemerkung');
    expect(element.querySelector('[data-testid="remarks-empty"]')).toBeFalsy();

    fill(element, 'offer-supplier-input', 'Neuer Anbieter');
    fill(element, 'offer-amount-input', '500');
    fillOfferTerms(element);
    submitFormOf(element, 'offer-supplier-input');
    httpMock
      .expectOne('/api/tenders/1/offers')
      .flush(offerSummary({ id: 23, supplierName: 'Neuer Anbieter', amount: 500 }));
    harness.detectChanges();

    expect(texts(element, 'offer-amount')[0]).toBe('500,00\u00a0€');
  });

  it('puts a newly added remark and offer at their sorted position while a column is sorted', async () => {
    const element = await render(SORTABLE_TENDER);
    sortBy(element, 'remarks', 'text');
    sortBy(element, 'offers', 'amount');

    fill(element, 'remark-input', 'Mittlere Bemerkung');
    submitFormOf(element, 'remark-input');
    httpMock.expectOne('/api/tenders/1/remarks').flush({ id: 13, text: 'Mittlere Bemerkung' });
    harness.detectChanges();

    expect(texts(element, 'remarks-row')).toEqual([
      'Angebot angenommen',
      'Bitte schnell liefern',
      'Mittlere Bemerkung',
      'Zoll beachten',
    ]);

    fill(element, 'offer-supplier-input', 'Neuer Anbieter');
    fill(element, 'offer-amount-input', '500');
    fillOfferTerms(element);
    submitFormOf(element, 'offer-supplier-input');
    httpMock
      .expectOne('/api/tenders/1/offers')
      .flush(offerSummary({ id: 23, supplierName: 'Neuer Anbieter', amount: 500 }));
    harness.detectChanges();

    expect(texts(element, 'offer-amount')).toEqual([
      '99,00\u00a0€',
      '500,00\u00a0€',
      '980,00\u00a0€',
      '1.234,56\u00a0€',
    ]);
  });

  it('shows the remark error below the field and above the submit button, keeping the typed text', async () => {
    const element = await render(OPEN_TENDER);

    fill(element, 'remark-input', 'Neue Bemerkung');
    submitFormOf(element, 'remark-input');
    httpMock.expectOne('/api/tenders/1/remarks').error(new ProgressEvent('error'));
    harness.detectChanges();

    const input = element.querySelector<HTMLInputElement>('[data-testid="remark-input"]')!;
    const error = element.querySelector('[data-testid="remark-error"]')!;
    const submit = element.querySelector<HTMLButtonElement>('[data-testid="remark-submit"]')!;
    expect(error.textContent).toContain('Die Bemerkung konnte nicht gespeichert werden.');
    expect(isBefore(input, error)).toBe(true);
    expect(isBefore(error, submit)).toBe(true);
    expect(input.value).toBe('Neue Bemerkung');
    expect(submit.disabled).toBe(false);
    expect(texts(element, 'remarks-row')).toEqual(['Bestehende Bemerkung']);
  });

  it('shows the offer error below the fields and above the submit button, keeping the entered values', async () => {
    const element = await render(OPEN_TENDER);

    fill(element, 'offer-supplier-input', 'Neuer Anbieter');
    fill(element, 'offer-amount-input', '750');
    fillOfferTerms(element);
    submitFormOf(element, 'offer-supplier-input');
    httpMock.expectOne('/api/tenders/1/offers').error(new ProgressEvent('error'));
    harness.detectChanges();

    const supplier = element.querySelector<HTMLInputElement>(
      '[data-testid="offer-supplier-input"]',
    )!;
    const amount = element.querySelector<HTMLInputElement>('[data-testid="offer-amount-input"]')!;
    const error = element.querySelector('[data-testid="offer-error"]')!;
    const submit = element.querySelector<HTMLButtonElement>('[data-testid="offer-submit"]')!;
    expect(error.textContent).toContain('Das Angebot konnte nicht gespeichert werden.');
    expect(isBefore(amount, error)).toBe(true);
    expect(isBefore(error, submit)).toBe(true);
    expect(supplier.value).toBe('Neuer Anbieter');
    expect(amount.value).toBe('750');
    expect(submit.disabled).toBe(false);
  });

  it('disables each submit button while its request is in flight and ignores a second submit', async () => {
    const element = await render(OPEN_TENDER);
    const remarkSubmit = element.querySelector<HTMLButtonElement>('[data-testid="remark-submit"]')!;
    const offerSubmit = element.querySelector<HTMLButtonElement>('[data-testid="offer-submit"]')!;

    fill(element, 'remark-input', 'Neue Bemerkung');
    expect(remarkSubmit.disabled).toBe(false);
    submitFormOf(element, 'remark-input');
    expect(remarkSubmit.disabled).toBe(true);
    submitFormOf(element, 'remark-input');

    httpMock.expectOne('/api/tenders/1/remarks').flush({ id: 11, text: 'Neue Bemerkung' });
    harness.detectChanges();

    fill(element, 'remark-input', 'Noch eine Bemerkung');
    expect(remarkSubmit.disabled).toBe(false);

    fill(element, 'offer-supplier-input', 'Neuer Anbieter');
    fill(element, 'offer-amount-input', '750');
    fillOfferTerms(element);
    expect(offerSubmit.disabled).toBe(false);
    submitFormOf(element, 'offer-supplier-input');
    expect(offerSubmit.disabled).toBe(true);
    submitFormOf(element, 'offer-supplier-input');

    httpMock
      .expectOne('/api/tenders/1/offers')
      .flush(offerSummary({ id: 21, supplierName: 'Neuer Anbieter', amount: 750 }));
  });

  it('places the single closed explanation before both add-forms in DOM order', async () => {
    const element = await render(CLOSED_TENDER);

    const explanations = element.querySelectorAll('[data-testid="closed-explanation"]');
    expect(explanations.length).toBe(1);
    expect(isBefore(explanations[0], element.querySelector('[data-testid="remark-input"]')!)).toBe(
      true,
    );
    expect(
      isBefore(explanations[0], element.querySelector('[data-testid="offer-supplier-input"]')!),
    ).toBe(true);
    expect(
      element.querySelector<HTMLInputElement>('[data-testid="offer-amount-input"]')?.disabled,
    ).toBe(true);
  });

  function closeButton(element: HTMLElement): HTMLButtonElement | null {
    return element.querySelector<HTMLButtonElement>('[data-testid="close-tender"]');
  }

  it('shows a secondary German close button for an open tender', async () => {
    const element = await render(OPEN_TENDER);

    const button = closeButton(element)!;
    expect(button.textContent?.trim()).toBe('Ausschreibung schließen');
    expect(button.type).toBe('button');
    expect(button.classList.contains('btn-primary')).toBe(false);
    expect(button.classList.contains('btn-secondary')).toBe(true);
  });

  it('never shows the close button for a tender that loads closed', async () => {
    const element = await render(CLOSED_TENDER);

    expect(closeButton(element)).toBeNull();
  });

  it('closes the tender in place, keeping remarks and offers and disabling the add-forms', async () => {
    const element = await render(OPEN_TENDER);

    closeButton(element)!.click();
    harness.detectChanges();

    const req = httpMock.expectOne('/api/tenders/1/close');
    expect(req.request.method).toBe('POST');
    req.flush(tenderSummary({ destination: BERLIN, status: 'CLOSED' }));
    harness.detectChanges();

    expect(texts(element, 'status')).toEqual(['Geschlossen']);
    expect(element.querySelector('[data-testid="closed-explanation"]')).not.toBeNull();
    expect(closeButton(element)).toBeNull();
    expect(document.activeElement).toBe(
      element.querySelector('[data-testid="closed-explanation"]'),
    );
    expect(
      element.querySelector<HTMLButtonElement>('[data-testid="remark-submit"]')!.disabled,
    ).toBe(true);
    expect(element.querySelector<HTMLButtonElement>('[data-testid="offer-submit"]')!.disabled).toBe(
      true,
    );
    expect(texts(element, 'remarks-row')).toEqual(['Bestehende Bemerkung']);
    expect(texts(element, 'offers-row').length).toBe(1);
  });

  it('disables the close button while the request is in flight and ignores a second click', async () => {
    const element = await render(OPEN_TENDER);
    const button = closeButton(element)!;

    button.click();
    harness.detectChanges();
    expect(button.disabled).toBe(true);
    button.click();

    httpMock
      .expectOne('/api/tenders/1/close')
      .flush(tenderSummary({ destination: BERLIN, status: 'CLOSED' }));
  });

  it('shows a German error and keeps the tender open when closing fails', async () => {
    const element = await render(OPEN_TENDER);

    closeButton(element)!.click();
    harness.detectChanges();
    httpMock
      .expectOne('/api/tenders/1/close')
      .flush('boom', { status: 500, statusText: 'Server Error' });
    harness.detectChanges();

    expect(element.querySelector('[data-testid="close-error"]')?.textContent).toContain(
      'konnte nicht geschlossen werden',
    );
    expect(element.querySelector('[data-testid="close-error"]')?.getAttribute('role')).toBe(
      'alert',
    );
    expect(texts(element, 'status')).toEqual(['Offen']);
    expect(closeButton(element)!.disabled).toBe(false);

    fill(element, 'remark-input', 'Weiterhin möglich');
    expect(
      element.querySelector<HTMLButtonElement>('[data-testid="remark-submit"]')!.disabled,
    ).toBe(false);
  });

  function text(element: HTMLElement, testId: string): string {
    return element.querySelector(`[data-testid="${testId}"]`)?.textContent?.trim() ?? '';
  }

  it('shows the summary line with pickup, delivery, vehicle and weight', async () => {
    const element = await render(OPEN_TENDER);

    expect(text(element, 'tender-summary')).toBe(
      '20.10.2099 · 22.10.2099 · Planenauflieger · 18.500 kg',
    );
  });

  it('renders the four shipment data cards in order with every row', async () => {
    const element = await render(
      tenderDetail({
        dangerousGoods: true,
        adrClass: '3',
        temperatureControlled: true,
        temperatureMinC: 2,
        temperatureMaxC: 8,
      }),
    );

    const cards = ['card-route', 'card-dates', 'card-cargo', 'card-vehicle'].map((id) =>
      element.querySelector(`[data-testid="${id}"]`)!,
    );
    expect(cards.every((card) => card !== null)).toBe(true);
    expect(isBefore(cards[0], cards[1])).toBe(true);
    expect(isBefore(cards[1], cards[2])).toBe(true);
    expect(isBefore(cards[2], cards[3])).toBe(true);

    expect(text(element, 'origin-country')).toBe('Deutschland');
    expect(text(element, 'origin-postal-city')).toBe('20457 Hamburg');
    expect(text(element, 'destination-country')).toBe('Niederlande');
    expect(text(element, 'destination-postal-city')).toBe('3011 AA Rotterdam');
    expect(text(element, 'pickup-date')).toBe('20.10.2099');
    expect(text(element, 'delivery-date')).toBe('22.10.2099');
    expect(text(element, 'bid-deadline')).toBe('16.10.2099');
    expect(text(element, 'commodity')).toBe('Maschinenteile auf Europaletten');
    expect(text(element, 'weight')).toBe('18.500 kg');
    expect(text(element, 'loading-meters')).toContain('ldm');
    expect(text(element, 'pallet-count')).toBe('33');
    expect(text(element, 'equipment')).toBe('Planenauflieger');
    expect(text(element, 'dangerous-goods')).toBe('Ja, ADR-Klasse 3');
    expect(text(element, 'temperature')).toBe('2 bis 8 °C');
    expect(text(element, 'currency')).toBe('EUR');
  });

  it('shows fallback values for missing pallets, dangerous goods and temperature control', async () => {
    const element = await render(tenderDetail({ palletCount: null }));

    expect(text(element, 'pallet-count')).toBe('Keine Angabe');
    expect(text(element, 'dangerous-goods')).toBe('Nein');
    expect(text(element, 'temperature')).toBe('Keine Vorgabe');
  });

  it('marks an open tender with a past bid deadline as abgelaufen', async () => {
    const element = await render(tenderDetail({ bidDeadline: '2000-01-01' }));

    expect(text(element, 'bid-deadline')).toBe('01.01.2000 (abgelaufen)');
  });

  it('marks an open tender whose bid deadline is today as heute', async () => {
    const today = localToday();
    const element = await render(tenderDetail({ bidDeadline: today }));

    expect(text(element, 'bid-deadline')).toBe(`${formatDate(today)} (heute)`);
  });

  it('shows no deadline hint for a closed tender with a past bid deadline', async () => {
    const element = await render(tenderDetail({ bidDeadline: '2000-01-01', status: 'CLOSED' }));

    expect(text(element, 'bid-deadline')).toBe('01.01.2000');
  });

  it('places the offers section before the remarks section', async () => {
    const element = await render(OPEN_TENDER);

    expect(
      isBefore(
        element.querySelector('[data-testid="offers"]')!,
        element.querySelector('[data-testid="remarks"]')!,
      ),
    ).toBe(true);
  });

  it('formats offer amounts and names the amount label in the tender currency', async () => {
    const element = await render(
      tenderDetail({
        currency: 'CHF',
        offers: [offerSummary({ id: 20, supplierName: 'Spedition Muster', amount: 500 })],
      }),
    );

    expect(text(element, 'offer-amount')).toContain('CHF');
    expect(text(element, 'offer-amount')).not.toContain('€');
    expect(sortButtonText(element, 'offers', 'amount')).toBe('Betrag (CHF)');
    expect(element.querySelector('label[for="offer-amount"]')?.textContent).toContain(
      'Betrag (CHF)',
    );
  });

  it('renders six offer columns with a trailing Vergeben column, Hinweis not sortable', async () => {
    const element = await render(SORTABLE_TENDER);

    const headers = Array.from(element.querySelectorAll('[data-testid="offers"] thead th'), (th) =>
      th.textContent?.trim().replace(/\s+/g, ' '),
    );
    expect(headers).toEqual([
      'Anbieter',
      'Betrag (EUR)',
      'Zustellung',
      'Gültig bis',
      'Hinweis',
      'Vergeben',
    ]);
    expect(element.querySelector('[data-testid="offers-sort-note"]')).toBeNull();
  });

  describe('awarding an offer', () => {
    const AWARD_TENDER: TenderDetailModel = tenderDetail({
      offers: [
        offerSummary({ id: 20, supplierName: 'Spedition Muster' }),
        offerSummary({ id: 21, supplierName: 'Acme Logistics' }),
        offerSummary({ id: 22, supplierName: 'Abgelaufen GmbH', validUntil: '2000-01-01' }),
      ],
    });

    function click(element: HTMLElement, testId: string, index = 0): void {
      element.querySelectorAll<HTMLButtonElement>(`[data-testid="${testId}"]`)[index].click();
      harness.detectChanges();
    }

    it('offers Vergeben only for non-expired offers of an open tender', async () => {
      const element = await render(AWARD_TENDER);

      expect(element.querySelectorAll('[data-testid="award-offer"]')).toHaveLength(2);
    });

    it('offers no award actions on closed tenders', async () => {
      const element = await render({ ...AWARD_TENDER, status: 'CLOSED' });

      expect(element.querySelector('[data-testid="award-offer"]')).toBeNull();
      expect(element.querySelector('[data-testid="offers-header-award"]')).toBeNull();
    });

    it('confirms in place for one row only and cancels without a request', async () => {
      const element = await render(AWARD_TENDER);

      click(element, 'award-offer', 0);
      expect(element.querySelectorAll('[data-testid="award-confirm"]')).toHaveLength(1);
      click(element, 'award-offer', 0);
      expect(element.querySelectorAll('[data-testid="award-confirm"]')).toHaveLength(1);
      expect(element.querySelector('[data-testid="award-confirm"]')?.textContent).toContain(
        'Zuschlag bestätigen',
      );

      click(element, 'award-cancel');
      expect(element.querySelector('[data-testid="award-confirm"]')).toBeNull();
      expect(element.querySelectorAll('[data-testid="award-offer"]')).toHaveLength(2);
    });

    it('disables the buttons while the request is in flight', async () => {
      const element = await render(AWARD_TENDER);

      click(element, 'award-offer', 0);
      click(element, 'award-confirm');

      // Offers are listed newest-first, so row 0 is offer 21.
      const req = httpMock.expectOne('/api/tenders/1/offers/21/award');
      expect(
        element.querySelector<HTMLButtonElement>('[data-testid="award-confirm"]')?.disabled,
      ).toBe(true);
      expect(
        element.querySelector<HTMLButtonElement>('[data-testid="award-cancel"]')?.disabled,
      ).toBe(true);
      req.flush({ ...AWARD_TENDER, status: 'AWARDED', awardedOfferId: 21 });
    });

    it('shows a German alert and keeps the tender open when awarding fails', async () => {
      const element = await render(AWARD_TENDER);

      click(element, 'award-offer', 0);
      click(element, 'award-confirm');
      httpMock
        .expectOne('/api/tenders/1/offers/21/award')
        .flush({},{ status: 409, statusText: 'Conflict' });
      harness.detectChanges();

      const error = element.querySelector('[data-testid="award-error"]');
      expect(error?.getAttribute('role')).toBe('alert');
      expect(error?.textContent).toContain('Der Zuschlag konnte nicht erteilt werden.');
      expect(element.querySelector('[data-testid="status"]')?.textContent).toContain('Offen');
      expect(element.querySelector('[data-testid="close-tender"]')).not.toBeNull();
    });

    it('updates the page in place after a successful award', async () => {
      const element = await render(AWARD_TENDER);

      click(element, 'award-offer', 0);
      click(element, 'award-confirm');
      httpMock
        .expectOne('/api/tenders/1/offers/21/award')
        .flush({ ...AWARD_TENDER, status: 'AWARDED', awardedOfferId: 21 });
      harness.detectChanges();
      await harness.fixture.whenStable();

      expect(element.querySelector('[data-testid="status"]')?.textContent).toContain('Vergeben');
      expect(texts(element, 'offer-awarded')).toEqual(['Zuschlag']);
      expect(element.querySelector('[data-testid="offers-row"]')?.textContent).toContain(
        'Acme Logistics',
      );
      expect(element.querySelector('[data-testid="close-tender"]')).toBeNull();
      expect(element.querySelector('[data-testid="award-offer"]')).toBeNull();
      expect(element.querySelector<HTMLButtonElement>('[data-testid="offer-submit"]')?.disabled).toBe(
        true,
      );
      expect(element.querySelector<HTMLButtonElement>('[data-testid="remark-submit"]')?.disabled).toBe(
        true,
      );
      const explanation = element.querySelector('[data-testid="awarded-explanation"]');
      expect(explanation?.textContent).toContain('vergeben');
      expect(document.activeElement).toBe(explanation);
    });
  });

  it('sorts offers by delivery date and validity date in both directions', async () => {
    const element = await render(
      tenderDetail({
        offers: [
          offerSummary({ id: 20, deliveryDate: '2099-10-22', validUntil: '2099-11-01' }),
          offerSummary({ id: 21, deliveryDate: '2099-10-20', validUntil: '2099-12-01' }),
          offerSummary({ id: 22, deliveryDate: '2099-10-21', validUntil: '2099-10-15' }),
        ],
      }),
    );

    sortBy(element, 'offers', 'deliveryDate');
    expect(texts(element, 'offer-delivery-date')).toEqual([
      '20.10.2099',
      '21.10.2099',
      '22.10.2099',
    ]);
    sortBy(element, 'offers', 'deliveryDate');
    expect(texts(element, 'offer-delivery-date')).toEqual([
      '22.10.2099',
      '21.10.2099',
      '20.10.2099',
    ]);

    sortBy(element, 'offers', 'validUntil');
    expect(texts(element, 'offer-valid-until')).toEqual(['15.10.2099', '01.11.2099', '01.12.2099']);
    sortBy(element, 'offers', 'validUntil');
    expect(texts(element, 'offer-valid-until')).toEqual(['01.12.2099', '01.11.2099', '15.10.2099']);
  });

  it('shows the late-delivery and expired hints only where they apply', async () => {
    const element = await render(
      tenderDetail({
        deliveryDate: '2099-10-22',
        offers: [
          offerSummary({ id: 20, deliveryDate: '2099-10-23', validUntil: '2000-01-01' }),
          offerSummary({ id: 21, deliveryDate: '2099-10-22', validUntil: localToday() }),
        ],
      }),
    );

    const rows = Array.from(element.querySelectorAll('[data-testid="offers-row"]'));
    // Newest first: id 21 is the first row, id 20 the second.
    expect(rows[0].querySelector('[data-testid="offer-delivery-hint"]')).toBeNull();
    expect(rows[0].querySelector('[data-testid="offer-expired-hint"]')).toBeNull();
    expect(rows[1].querySelector('[data-testid="offer-delivery-hint"]')?.textContent).toContain(
      'nach Wunschtermin',
    );
    expect(rows[1].querySelector('[data-testid="offer-expired-hint"]')?.textContent).toContain(
      'abgelaufen',
    );
  });

  it('shows the note of an offer', async () => {
    const element = await render(tenderDetail({ offers: [offerSummary({ note: 'Inkl. Maut' })] }));

    expect(text(element, 'offer-note')).toBe('Inkl. Maut');
  });

  it('shows German errors under invalid touched offer fields', async () => {
    const element = await render(OPEN_TENDER);

    fill(element, 'offer-supplier-input', 'x'.repeat(101));
    fill(element, 'offer-delivery-date-input', '2099-10-19');
    fill(element, 'offer-valid-until-input', '2000-01-01');
    fill(element, 'offer-note-input', 'n'.repeat(501));
    for (const id of [
      'offer-supplier-input',
      'offer-amount-input',
      'offer-delivery-date-input',
      'offer-valid-until-input',
      'offer-note-input',
    ]) {
      element.querySelector(`[data-testid="${id}"]`)!.dispatchEvent(new Event('blur'));
    }
    harness.detectChanges();

    expect(text(element, 'offer-supplierName-error')).toContain('100 Zeichen');
    expect(text(element, 'offer-amount-error')).toContain('Betrag');
    expect(text(element, 'offer-deliveryDate-error')).toContain('nicht vor der Abholung');
    expect(text(element, 'offer-validUntil-error')).toContain('Vergangenheit');
    expect(text(element, 'offer-note-error')).toContain('500 Zeichen');
    expect(element.querySelector<HTMLButtonElement>('[data-testid="offer-submit"]')?.disabled).toBe(
      true,
    );
  });

  it('disables the offer form with a notice when the bid deadline has passed, keeping remarks enabled', async () => {
    const element = await render(tenderDetail({ bidDeadline: '2000-01-01' }));

    expect(text(element, 'deadline-passed-notice')).toContain('Angebotsfrist');
    expect(element.querySelector('[data-testid="closed-explanation"]')).toBeNull();
    for (const id of [
      'offer-supplier-input',
      'offer-amount-input',
      'offer-delivery-date-input',
      'offer-valid-until-input',
      'offer-note-input',
      'offer-submit',
    ]) {
      expect(element.querySelector<HTMLInputElement>(`[data-testid="${id}"]`)?.disabled).toBe(true);
    }
    expect(element.querySelector<HTMLInputElement>('[data-testid="remark-input"]')?.disabled).toBe(
      false,
    );
  });

  it('shows only the closed explanation for a closed tender past its deadline', async () => {
    const element = await render({
      ...tenderDetail({ bidDeadline: '2000-01-01' }),
      status: 'CLOSED',
    });

    expect(element.querySelector('[data-testid="closed-explanation"]')).not.toBeNull();
    expect(element.querySelector('[data-testid="deadline-passed-notice"]')).toBeNull();
  });

  it('keeps the entered values and shows the offer error when saving fails with 409', async () => {
    const element = await render(OPEN_TENDER);
    fill(element, 'offer-supplier-input', 'Neuer Anbieter');
    fill(element, 'offer-amount-input', '750');
    fillOfferTerms(element);
    submitFormOf(element, 'offer-supplier-input');

    httpMock
      .expectOne('/api/tenders/1/offers')
      .flush('deadline', { status: 409, statusText: 'Conflict' });
    harness.detectChanges();

    expect(text(element, 'offer-error')).toContain('konnte nicht gespeichert werden');
    expect(
      element.querySelector<HTMLInputElement>('[data-testid="offer-supplier-input"]')?.value,
    ).toBe('Neuer Anbieter');
    expect(
      element.querySelector<HTMLInputElement>('[data-testid="offer-valid-until-input"]')?.value,
    ).toBe('2099-10-30');
  });

  it('shows no summary line or data cards while loading', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');
    const element = harness.routeNativeElement as HTMLElement;

    expect(element.querySelector('[data-testid="tender-summary"]')).toBeNull();
    expect(element.querySelector('[data-testid="shipment-data"]')).toBeNull();
    expect(element.querySelector('[data-testid="card-route"]')).toBeNull();

    httpMock.expectOne('/api/tenders/1').flush(OPEN_TENDER);
  });

  it('shows no summary line or data cards when the tender cannot be loaded', async () => {
    const harness = await RouterTestingHarness.create('/tenders/1');
    httpMock.expectOne('/api/tenders/1').flush('nope', { status: 404, statusText: 'Not Found' });
    harness.detectChanges();
    const element = harness.routeNativeElement as HTMLElement;

    expect(element.querySelector('[data-testid="tender-summary"]')).toBeNull();
    expect(element.querySelector('[data-testid="shipment-data"]')).toBeNull();
    expect(element.querySelector('[data-testid="card-vehicle"]')).toBeNull();
  });
});
