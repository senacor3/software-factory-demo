import { HttpClient } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { catchError, map, of } from 'rxjs';

interface HealthResponse {
  status: string;
}

const UNAVAILABLE_LABEL = 'nicht verfügbar';

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  private readonly http = inject(HttpClient);

  protected readonly systemStatus = signal<string>('…');

  constructor() {
    this.http
      .get<HealthResponse>('/api/health')
      .pipe(
        map((response) => response.status),
        catchError(() => of(UNAVAILABLE_LABEL)),
      )
      .subscribe((status) => this.systemStatus.set(status));
  }
}
