import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router, provideRouter } from '@angular/router';
import { TenderCreate } from './tender-create';

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
  });

  afterEach(() => {
    httpMock.verify();
  });

  function fillForm(origin: string, destination: string): void {
    const compiled = fixture.nativeElement as HTMLElement;
    const originInput = compiled.querySelector<HTMLInputElement>('[data-testid="origin-input"]');
    const destinationInput = compiled.querySelector<HTMLInputElement>(
      '[data-testid="destination-input"]',
    );

    originInput!.value = origin;
    originInput!.dispatchEvent(new Event('input'));
    destinationInput!.value = destination;
    destinationInput!.dispatchEvent(new Event('input'));
    fixture.detectChanges();
  }

  it('should create', () => {
    fixture.detectChanges();
    expect(component).toBeTruthy();
  });

  it('navigates to / and creates the tender when the form is submitted successfully', () => {
    const navigateSpy = vi.spyOn(router, 'navigateByUrl');

    fixture.detectChanges();
    fillForm('Hamburg', 'Berlin');

    const compiled = fixture.nativeElement as HTMLElement;
    compiled.querySelector('form')!.dispatchEvent(new Event('submit'));

    const req = httpMock.expectOne('/api/tenders');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ origin: 'Hamburg', destination: 'Berlin' });
    req.flush({ id: 1, origin: 'Hamburg', destination: 'Berlin', status: 'OPEN' });

    expect(navigateSpy).toHaveBeenCalledWith('/');
  });

  it('shows a German error message and does not navigate when creation fails', () => {
    const navigateSpy = vi.spyOn(router, 'navigateByUrl');

    fixture.detectChanges();
    fillForm('Hamburg', 'Berlin');

    const compiled = fixture.nativeElement as HTMLElement;
    compiled.querySelector('form')!.dispatchEvent(new Event('submit'));

    const req = httpMock.expectOne('/api/tenders');
    req.error(new ProgressEvent('error'));
    fixture.detectChanges();

    expect(compiled.querySelector('[data-testid="submit-error"]')?.textContent).toContain(
      'konnte nicht erstellt werden',
    );
    expect(navigateSpy).not.toHaveBeenCalled();
  });

  it('does not submit while the form is invalid', () => {
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    compiled.querySelector('form')!.dispatchEvent(new Event('submit'));

    // httpMock.expectNone throws if a matching request was made; wrapping it in an explicit
    // expect(...).not.toThrow() keeps that same check but as a recognized assertion (plain
    // httpMock.expectNone(...) isn't picked up by eslint-plugin-sonarjs's assertions-in-tests
    // rule, part of the new static_analysis check).
    expect(() => httpMock.expectNone('/api/tenders')).not.toThrow();
  });
});
