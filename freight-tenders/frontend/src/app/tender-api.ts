import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export type TenderStatus = 'OPEN' | 'CLOSED';

export interface TenderSummary {
  id: number;
  origin: string;
  destination: string;
  status: TenderStatus;
}

@Injectable({
  providedIn: 'root',
})
export class TenderApiService {
  private readonly http = inject(HttpClient);

  list(): Observable<TenderSummary[]> {
    return this.http.get<TenderSummary[]>('/api/tenders');
  }
}
