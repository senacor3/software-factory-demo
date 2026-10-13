import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { TenderSummary } from '../tender-api';
import { tenderSummary } from '../tender-test-data';
import { TenderOverview } from './tender-overview';

describe('TenderOverview', () => {
  let component: TenderOverview;
  let fixture: ComponentFixture<TenderOverview>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TenderOverview],
      providers: [provideHttpClient(), provideHttpClientTesting(), provideRouter([])],
    }).compileComponents();

    fixture = TestBed.createComponent(TenderOverview);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  function tender(
    id: number,
    originCity: string,
    destinationCity: string,
    status: TenderSummary['status'] = 'OPEN',
  ): TenderSummary {
    return tenderSummary({
      id,
      origin: { country: 'DE', postalCode: '10115', city: originCity },
      destination: { country: 'DE', postalCode: '80331', city: destinationCity },
      status,
    });
  }

  const SORTABLE_TENDERS: TenderSummary[] = [
    tender(1, 'Hamburg', 'Rotterdam'),
    tender(2, 'Aachen', 'Zürich'),
    tender(3, 'Köln', 'Antwerpen'),
    tender(4, 'Stuttgart', 'Frankfurt', 'CLOSED'),
    tender(5, 'Bremen', 'Mailand', 'CLOSED'),
  ];

  function load(tenders: TenderSummary[]): HTMLElement {
    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').flush(tenders);
    fixture.detectChanges();

    return fixture.nativeElement as HTMLElement;
  }

  function origins(compiled: HTMLElement, table: string): string[] {
    return Array.from(compiled.querySelectorAll(`[data-testid="${table}-link"]`)).map(
      (link) => link.textContent?.trim() ?? '',
    );
  }

  function sortBy(compiled: HTMLElement, table: string, column: string): void {
    compiled.querySelector<HTMLButtonElement>(`[data-testid="${table}-sort-${column}"]`)!.click();
    fixture.detectChanges();
  }

  function ariaSortOf(compiled: HTMLElement, table: string, column: string): string | null {
    return (
      compiled
        .querySelector(`[data-testid="${table}-header-${column}"]`)
        ?.getAttribute('aria-sort') ?? null
    );
  }

  function sortButtonText(compiled: HTMLElement, table: string, column: string): string {
    return (
      compiled.querySelector(`[data-testid="${table}-sort-${column}"]`)?.textContent?.trim() ?? ''
    );
  }

  it('should create', () => {
    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').flush([]);
    expect(component).toBeTruthy();
  });

  it('shows a German loading message before the response arrives, not an empty-state', () => {
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('[data-testid="loading"]')?.textContent).toContain(
      'werden geladen',
    );
    expect(compiled.querySelector('[data-testid="open-tenders-empty"]')).toBeFalsy();
    expect(compiled.querySelector('[data-testid="closed-tenders-empty"]')).toBeFalsy();

    httpMock.expectOne('/api/tenders').flush([]);
  });

  it('lists open and closed tenders under their German headings when the backend returns a mix', () => {
    const tenders: TenderSummary[] = [
      tender(1, 'Hamburg', 'Berlin'),
      tender(2, 'München', 'Köln', 'CLOSED'),
    ];

    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').flush(tenders);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h2')?.textContent).toContain('Offene Ausschreibungen');
    expect(compiled.querySelector('[data-testid="open-tenders"]')?.textContent).toContain(
      'Hamburg',
    );
    expect(compiled.querySelector('[data-testid="closed-tenders"]')?.textContent).toContain(
      'München',
    );
  });

  it('shows a German empty-state message for the section with no tenders', () => {
    const tenders: TenderSummary[] = [tender(1, 'Hamburg', 'Berlin')];

    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').flush(tenders);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('[data-testid="closed-tenders-empty"]')?.textContent).toContain(
      'Keine abgeschlossenen Ausschreibungen vorhanden.',
    );
  });

  it("links to the create-tender page and to each tender's detail page", () => {
    const tenders: TenderSummary[] = [tender(1, 'Hamburg', 'Berlin')];

    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').flush(tenders);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const createLink = compiled.querySelector<HTMLAnchorElement>('[data-testid="create-link"]');
    expect(createLink?.getAttribute('href')).toBe('/tenders/new');

    const tenderLink = compiled.querySelector<HTMLAnchorElement>(
      '[data-testid="open-tenders-link"]',
    );
    expect(tenderLink?.getAttribute('href')).toBe('/tenders/1');
  });

  it('shows the city of the origin and destination address in the Von and Nach columns', () => {
    const compiled = load([tender(1, 'Hamburg', 'Rotterdam')]);

    const row = compiled.querySelector('[data-testid="open-tenders-row"]');
    expect(row?.querySelector('[data-testid="open-tenders-link"]')?.textContent?.trim()).toBe(
      'Hamburg',
    );
    expect(row?.querySelector('[data-testid="origin-detail"]')?.textContent?.trim()).toBe(
      'DE-10115',
    );
    expect(row?.querySelector('[data-testid="destination-detail"]')?.textContent?.trim()).toBe(
      'DE-80331',
    );
    expect(row?.textContent).toContain('Rotterdam');
    expect(row?.textContent).not.toContain('[object Object]');
  });

  function textOf(compiled: HTMLElement, table: string, testId: string): string | null {
    const row = compiled.querySelector(`[data-testid="${table}-row"]`);
    return row?.querySelector(`[data-testid="${testId}"]`)?.textContent?.trim() ?? null;
  }

  function tendersWith(overrides: Partial<TenderSummary>): TenderSummary[] {
    return [tenderSummary({ id: 1, ...overrides })];
  }

  it('renders the seven column headers in the open table and an extra Status header in the second table', () => {
    const compiled = load(SORTABLE_TENDERS);
    const base = ['Von', 'Nach', 'Abholung', 'Ladung', 'Fahrzeug', 'Angebotsfrist', 'Angebote'];

    for (const [table, expected] of [
      ['open-tenders', base],
      ['closed-tenders', [...base, 'Status']],
    ] as const) {
      const headers = Array.from(
        compiled.querySelectorAll(`[data-testid="${table}"] thead th`),
      ).map((th) => th.textContent?.trim());
      expect(headers).toEqual(expected);
    }
    expect(compiled.querySelector('[data-testid="open-tenders"] [class*="pill"]')).toBeFalsy();
  });

  it('shows pickup date, load line, German vehicle label, deadline and offer count in a row', () => {
    const compiled = load(tendersWith({ offerCount: 3, lowestOfferAmount: 1450 }));

    expect(textOf(compiled, 'open-tenders', 'pickup-date')).toBe('20.10.2099');
    expect(textOf(compiled, 'open-tenders', 'load')).toBe('18.500 kg · 13,6 ldm');
    expect(textOf(compiled, 'open-tenders', 'equipment')).toBe('Planenauflieger');
    expect(textOf(compiled, 'open-tenders', 'bid-deadline')).toBe('16.10.2099');
    expect(textOf(compiled, 'open-tenders', 'offer-count')).toBe('3');
    expect(textOf(compiled, 'open-tenders', 'lowest-offer')).toBe('ab 1.450,00 €');
  });

  it('shows ADR class and temperature range as hints in the Ladung cell, and nothing for a plain tender', () => {
    const adr = load(tendersWith({ dangerousGoods: true, adrClass: '3' }));
    expect(textOf(adr, 'open-tenders', 'load-hint')).toBe('ADR 3');
  });

  it('shows the temperature range for a reefer tender', () => {
    const compiled = load(
      tendersWith({ temperatureControlled: true, temperatureMinC: 2, temperatureMaxC: 8 }),
    );
    expect(textOf(compiled, 'open-tenders', 'load-hint')).toBe('2 bis 8 °C');
  });

  it('shows no second line in the Ladung cell for a plain tender', () => {
    const compiled = load(tendersWith({}));
    expect(textOf(compiled, 'open-tenders', 'load-hint')).toBeNull();
  });

  it('shows no lowest offer and a count of 0 for a tender without offers', () => {
    const compiled = load(tendersWith({}));

    expect(textOf(compiled, 'open-tenders', 'offer-count')).toBe('0');
    expect(textOf(compiled, 'open-tenders', 'lowest-offer')).toBeNull();
  });

  describe('deadline hints', () => {
    beforeEach(() => {
      vi.useFakeTimers({ toFake: ['Date'] });
      vi.setSystemTime(new Date(2026, 9, 16, 12, 0));
    });

    afterEach(() => {
      vi.useRealTimers();
    });

    it('shows "heute" for an open tender whose deadline is today', () => {
      const compiled = load(tendersWith({ bidDeadline: '2026-10-16' }));
      expect(textOf(compiled, 'open-tenders', 'deadline-hint')).toBe('heute');
    });

    it('shows "abgelaufen" for an open tender whose deadline has passed', () => {
      const compiled = load(tendersWith({ bidDeadline: '2026-10-15' }));
      expect(textOf(compiled, 'open-tenders', 'deadline-hint')).toBe('abgelaufen');
    });

    it('shows no hint for a closed tender with a deadline today or in the past', () => {
      const compiled = load([
        tenderSummary({ id: 1, status: 'CLOSED', bidDeadline: '2026-10-16' }),
        tenderSummary({ id: 2, status: 'CLOSED', bidDeadline: '2026-10-15' }),
      ]);
      expect(compiled.querySelector('[data-testid="deadline-hint"]')).toBeFalsy();
    });
  });

  describe('sorting by the other columns', () => {
    const TENDERS: TenderSummary[] = [
      tenderSummary({
        id: 1,
        pickupDate: '2099-03-01',
        weightKg: 900,
        bidDeadline: '2099-02-01',
        offerCount: 10,
        origin: { country: 'DE', postalCode: '1', city: 'A' },
      }),
      tenderSummary({
        id: 2,
        pickupDate: '2099-01-01',
        weightKg: 18500,
        bidDeadline: '2099-03-01',
        offerCount: 2,
        origin: { country: 'DE', postalCode: '1', city: 'B' },
      }),
      tenderSummary({
        id: 3,
        pickupDate: '2099-02-01',
        weightKg: 5000,
        bidDeadline: '2099-01-01',
        offerCount: 0,
        origin: { country: 'DE', postalCode: '1', city: 'C' },
      }),
    ];

    it.each([
      ['pickupDate', ['B', 'C', 'A']],
      ['weightKg', ['A', 'C', 'B']],
      ['bidDeadline', ['C', 'A', 'B']],
      ['offerCount', ['C', 'B', 'A']],
    ])('sorts by %s ascending and then descending', (column, ascending) => {
      const compiled = load(TENDERS);

      sortBy(compiled, 'open-tenders', column);
      expect(origins(compiled, 'open-tenders')).toEqual(ascending);
      expect(ariaSortOf(compiled, 'open-tenders', column)).toBe('ascending');

      sortBy(compiled, 'open-tenders', column);
      expect(origins(compiled, 'open-tenders')).toEqual([...ascending].reverse());
      expect(ariaSortOf(compiled, 'open-tenders', column)).toBe('descending');
      expect(ariaSortOf(compiled, 'closed-tenders', column)).toBe('none');
    });

    it('has no sort button on the Fahrzeug header', () => {
      const compiled = load(TENDERS);

      expect(compiled.querySelector('[data-testid="open-tenders-sort-equipmentType"]')).toBeFalsy();
      expect(
        compiled.querySelector('[data-testid="open-tenders-header-equipmentType"]')?.textContent,
      ).toContain('Fahrzeug');
    });
  });

  it('shows a German error message when the backend is unreachable', () => {
    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').error(new ProgressEvent('error'));
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('[data-testid="load-error"]')?.textContent).toContain(
      'konnten nicht geladen werden',
    );
  });

  it('shows the page heading and never the raw status enum', () => {
    const compiled = load(SORTABLE_TENDERS);

    expect(compiled.querySelector('[data-testid="page-title"]')?.textContent).toContain(
      'Ausschreibungen',
    );
    expect(compiled.textContent).not.toContain('OPEN');
    expect(compiled.textContent).not.toContain('CLOSED');
  });

  it('orders both tables newest-first with no sort indicator until a column is selected', () => {
    const compiled = load(SORTABLE_TENDERS);

    expect(origins(compiled, 'open-tenders')).toEqual(['Köln', 'Aachen', 'Hamburg']);
    expect(origins(compiled, 'closed-tenders')).toEqual(['Bremen', 'Stuttgart']);

    for (const table of ['open-tenders', 'closed-tenders']) {
      for (const column of ['origin', 'destination']) {
        expect(ariaSortOf(compiled, table, column)).toBe('none');
      }
    }
    expect(sortButtonText(compiled, 'open-tenders', 'origin')).toBe('Von');
    expect(sortButtonText(compiled, 'open-tenders', 'destination')).toBe('Nach');
  });

  it('sorts ascending when a column header is selected and shows the indicator on that column only', () => {
    const compiled = load(SORTABLE_TENDERS);

    sortBy(compiled, 'open-tenders', 'origin');

    expect(origins(compiled, 'open-tenders')).toEqual(['Aachen', 'Hamburg', 'Köln']);
    expect(ariaSortOf(compiled, 'open-tenders', 'origin')).toBe('ascending');
    expect(sortButtonText(compiled, 'open-tenders', 'origin')).toContain('▲');
    expect(ariaSortOf(compiled, 'open-tenders', 'destination')).toBe('none');
    expect(sortButtonText(compiled, 'open-tenders', 'destination')).toBe('Nach');
  });

  it('reverses to descending when the active column header is selected again', () => {
    const compiled = load(SORTABLE_TENDERS);

    sortBy(compiled, 'open-tenders', 'origin');
    sortBy(compiled, 'open-tenders', 'origin');

    expect(origins(compiled, 'open-tenders')).toEqual(['Köln', 'Hamburg', 'Aachen']);
    expect(ariaSortOf(compiled, 'open-tenders', 'origin')).toBe('descending');
    expect(sortButtonText(compiled, 'open-tenders', 'origin')).toContain('▼');
  });

  it('switches to the newly selected column ascending and clears the previous header', () => {
    const compiled = load(SORTABLE_TENDERS);

    sortBy(compiled, 'open-tenders', 'origin');
    sortBy(compiled, 'open-tenders', 'origin');
    sortBy(compiled, 'open-tenders', 'destination');

    // Antwerpen (Köln), Rotterdam (Hamburg), Zürich (Aachen)
    expect(origins(compiled, 'open-tenders')).toEqual(['Köln', 'Hamburg', 'Aachen']);
    expect(ariaSortOf(compiled, 'open-tenders', 'destination')).toBe('ascending');
    expect(sortButtonText(compiled, 'open-tenders', 'destination')).toContain('▲');
    expect(ariaSortOf(compiled, 'open-tenders', 'origin')).toBe('none');
    expect(sortButtonText(compiled, 'open-tenders', 'origin')).toBe('Von');
  });

  it('sorts each table independently of the other', () => {
    const compiled = load(SORTABLE_TENDERS);

    sortBy(compiled, 'open-tenders', 'origin');

    expect(origins(compiled, 'closed-tenders')).toEqual(['Bremen', 'Stuttgart']);
    expect(ariaSortOf(compiled, 'closed-tenders', 'origin')).toBe('none');
    expect(sortButtonText(compiled, 'closed-tenders', 'origin')).toBe('Von');
  });

  it('makes every sort header a real button, so Tab + Enter/Space trigger it like a click', () => {
    const compiled = load(SORTABLE_TENDERS);

    for (const table of ['open-tenders', 'closed-tenders']) {
      for (const column of [
        'origin',
        'destination',
        'pickupDate',
        'weightKg',
        'bidDeadline',
        'offerCount',
      ]) {
        const header = compiled.querySelector(`[data-testid="${table}-header-${column}"]`);
        const button = compiled.querySelector<HTMLButtonElement>(
          `[data-testid="${table}-sort-${column}"]`,
        );
        expect(header?.tagName).toBe('TH');
        expect(button?.tagName).toBe('BUTTON');
        expect(button?.type).toBe('button');
        expect(button?.disabled).toBe(false);
        expect(button?.tabIndex).toBe(0);
        expect(header?.contains(button ?? null)).toBe(true);
      }
    }
  });

  it('still renders the sortable header row when a table is empty, with the empty message in its body', () => {
    const compiled = load([]);

    for (const table of ['open-tenders', 'closed-tenders']) {
      expect(sortButtonText(compiled, table, 'origin')).toBe('Von');
      expect(sortButtonText(compiled, table, 'destination')).toBe('Nach');
      expect(ariaSortOf(compiled, table, 'origin')).toBe('none');
    }

    const openEmpty = compiled.querySelector('[data-testid="open-tenders-empty"]');
    expect(openEmpty?.tagName).toBe('TD');
    expect(openEmpty?.getAttribute('colspan')).toBe('7');
    expect(openEmpty?.textContent).toContain('Keine offenen Ausschreibungen vorhanden.');
    expect(
      compiled.querySelector('[data-testid="open-tenders"]')?.contains(openEmpty ?? null),
    ).toBe(true);
    expect(compiled.querySelector('[data-testid="closed-tenders-empty"]')?.textContent).toContain(
      'Keine abgeschlossenen Ausschreibungen vorhanden.',
    );
    expect(
      compiled.querySelector('[data-testid="closed-tenders-empty"]')?.getAttribute('colspan'),
    ).toBe('8');
  });

  it('lists awarded and closed tenders together with a Status column and Zuschlag line', () => {
    const awarded = {
      ...tender(6, 'Dresden', 'Leipzig', 'AWARDED'),
      awardedSupplierName: 'Acme Logistics',
      awardedAmount: 1234.5,
    };
    const compiled = load([tender(1, 'Hamburg', 'Berlin'), awarded, tender(7, 'Ulm', 'Bonn', 'CLOSED')]);

    expect(compiled.querySelectorAll('h2')[1].textContent).toContain(
      'Abgeschlossene Ausschreibungen',
    );
    expect(origins(compiled, 'closed-tenders')).toEqual(['Ulm', 'Dresden']);
    expect(origins(compiled, 'open-tenders')).toEqual(['Hamburg']);
    expect(
      Array.from(compiled.querySelectorAll('[data-testid="tender-status"]'), (node) =>
        node.textContent?.trim(),
      ),
    ).toEqual(['Geschlossen', 'Vergeben']);
    expect(compiled.querySelector('[data-testid="awarded-offer"]')?.textContent).toContain(
      'Zuschlag: Acme Logistics',
    );

    sortBy(compiled, 'closed-tenders', 'status');
    expect(origins(compiled, 'closed-tenders')).toEqual(['Ulm', 'Dresden']);
    sortBy(compiled, 'closed-tenders', 'status');
    expect(origins(compiled, 'closed-tenders')).toEqual(['Dresden', 'Ulm']);
  });

  it("navigates to the tender's detail page when its row is selected anywhere", () => {
    const router = TestBed.inject(Router);
    const navigateSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    const compiled = load(SORTABLE_TENDERS);

    compiled.querySelector<HTMLElement>('[data-testid="open-tenders-row"]')!.click();

    expect(navigateSpy).toHaveBeenCalledWith(['/tenders', 3]);
  });

  it('does not navigate in place when a row is selected with a modifier key held', () => {
    const router = TestBed.inject(Router);
    const navigateSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    const compiled = load(SORTABLE_TENDERS);

    compiled
      .querySelector<HTMLElement>('[data-testid="open-tenders-row"]')!
      .dispatchEvent(new MouseEvent('click', { bubbles: true, metaKey: true }));

    expect(navigateSpy).not.toHaveBeenCalled();
  });

  it("leaves a click on the row's own link to that link, without navigating a second time", () => {
    const router = TestBed.inject(Router);
    const navigateSpy = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    const navigateByUrlSpy = vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
    const compiled = load(SORTABLE_TENDERS);

    compiled.querySelector<HTMLElement>('[data-testid="open-tenders-link"]')!.click();

    expect(navigateByUrlSpy).toHaveBeenCalledTimes(1);
    expect(navigateSpy).not.toHaveBeenCalled();
  });
});
