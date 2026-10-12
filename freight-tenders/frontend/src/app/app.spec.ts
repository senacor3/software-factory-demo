import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('App', () => {
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();

    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create the app and render the tender overview', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();

    httpMock.expectOne('/api/tenders').flush([]);

    const app = fixture.componentInstance;
    expect(app).toBeTruthy();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('app-tender-overview')).toBeTruthy();
  });
});
