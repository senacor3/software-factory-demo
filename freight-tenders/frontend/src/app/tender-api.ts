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

export interface RemarkSummary {
  id: number;
  text: string;
}

export interface OfferSummary {
  id: number;
  supplierName: string;
  amount: number;
}

export interface TenderDetail {
  id: number;
  origin: string;
  destination: string;
  status: TenderStatus;
  remarks: RemarkSummary[];
  offers: OfferSummary[];
}

@Injectable({
  providedIn: 'root',
})
export class TenderApiService {
  private readonly http = inject(HttpClient);

  list(): Observable<TenderSummary[]> {
    return this.http.get<TenderSummary[]>('/api/tenders');
  }

  create(origin: string, destination: string): Observable<TenderSummary> {
    return this.http.post<TenderSummary>('/api/tenders', { origin, destination });
  }

  detail(id: number): Observable<TenderDetail> {
    return this.http.get<TenderDetail>(`/api/tenders/${id}`);
  }

  addRemark(id: number, text: string): Observable<RemarkSummary> {
    return this.http.post<RemarkSummary>(`/api/tenders/${id}/remarks`, { text });
  }

  addOffer(id: number, supplierName: string, amount: number): Observable<OfferSummary> {
    return this.http.post<OfferSummary>(`/api/tenders/${id}/offers`, { supplierName, amount });
  }
}
