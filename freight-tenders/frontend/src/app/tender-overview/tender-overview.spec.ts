import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { TenderSummary } from '../tender-api';
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
      { id: 1, origin: 'Hamburg', destination: 'Berlin', status: 'OPEN' },
      { id: 2, origin: 'München', destination: 'Köln', status: 'CLOSED' },
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
    const tenders: TenderSummary[] = [
      { id: 1, origin: 'Hamburg', destination: 'Berlin', status: 'OPEN' },
    ];

    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').flush(tenders);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('[data-testid="closed-tenders-empty"]')?.textContent).toContain(
      'Keine geschlossenen Ausschreibungen vorhanden.',
    );
  });

  it('links to the create-tender page and to each tender\'s detail page', () => {
    const tenders: TenderSummary[] = [
      { id: 1, origin: 'Hamburg', destination: 'Berlin', status: 'OPEN' },
    ];

    fixture.detectChanges();
    httpMock.expectOne('/api/tenders').flush(tenders);
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const createLink = compiled.querySelector<HTMLAnchorElement>('[data-testid="create-link"]');
    expect(createLink?.getAttribute('href')).toBe('/tenders/new');

    const tenderLink = compiled.querySelector<HTMLAnchorElement>(
      '[data-testid="open-tenders"] a',
    );
    expect(tenderLink?.getAttribute('href')).toBe('/tenders/1');
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
});
