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
      'Keine geschlossenen Ausschreibungen vorhanden.',
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
    const cells = Array.from(row?.querySelectorAll('td') ?? []).map((cell) =>
      cell.textContent?.trim(),
    );
    expect(cells.slice(0, 2)).toEqual(['Hamburg', 'Rotterdam']);
    expect(row?.textContent).not.toContain('20457');
    expect(row?.textContent).not.toContain('[object Object]');
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

  it("shows the page heading and each tender's status as a German pill, never the raw enum", () => {
    const compiled = load(SORTABLE_TENDERS);

    expect(compiled.querySelector('[data-testid="page-title"]')?.textContent).toContain(
      'Ausschreibungen',
    );

    const openRow = compiled.querySelector('[data-testid="open-tenders-row"]');
    const closedRow = compiled.querySelector('[data-testid="closed-tenders-row"]');
    expect(openRow?.textContent).toContain('Offen');
    expect(openRow?.textContent).not.toContain('OPEN');
    expect(closedRow?.textContent).toContain('Geschlossen');
    expect(closedRow?.textContent).not.toContain('CLOSED');
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
      for (const column of ['origin', 'destination']) {
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
    expect(openEmpty?.getAttribute('colspan')).toBe('3');
    expect(openEmpty?.textContent).toContain('Keine offenen Ausschreibungen vorhanden.');
    expect(
      compiled.querySelector('[data-testid="open-tenders"]')?.contains(openEmpty ?? null),
    ).toBe(true);
    expect(compiled.querySelector('[data-testid="closed-tenders-empty"]')?.textContent).toContain(
      'Keine geschlossenen Ausschreibungen vorhanden.',
    );
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
