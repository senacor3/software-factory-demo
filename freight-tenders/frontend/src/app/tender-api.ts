import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export type TenderStatus = 'OPEN' | 'CLOSED';

export const STATUS_LABELS: Record<TenderStatus, string> = {
  OPEN: 'Offen',
  CLOSED: 'Geschlossen',
};

export type EquipmentType = 'CURTAIN_SIDER' | 'BOX' | 'REEFER' | 'FLATBED' | 'MEGA_TRAILER';

export const EQUIPMENT_LABELS: Record<EquipmentType, string> = {
  CURTAIN_SIDER: 'Planenauflieger',
  BOX: 'Kofferauflieger',
  REEFER: 'Kühlauflieger',
  FLATBED: 'Plateauauflieger',
  MEGA_TRAILER: 'Megatrailer',
};

export type Currency = 'EUR' | 'CHF' | 'GBP' | 'PLN' | 'CZK' | 'DKK' | 'SEK';

export const CURRENCIES: readonly Currency[] = ['EUR', 'CHF', 'GBP', 'PLN', 'CZK', 'DKK', 'SEK'];

// Only the choices the create form offers: the backend accepts any two uppercase letters.
export const COUNTRY_LABELS: Record<string, string> = {
  DE: 'Deutschland',
  AT: 'Österreich',
  CH: 'Schweiz',
  NL: 'Niederlande',
  BE: 'Belgien',
  LU: 'Luxemburg',
  FR: 'Frankreich',
  IT: 'Italien',
  ES: 'Spanien',
  PL: 'Polen',
  CZ: 'Tschechien',
  DK: 'Dänemark',
  SE: 'Schweden',
};

export const ADR_CLASSES: readonly string[] = [
  '1',
  '2',
  '3',
  '4.1',
  '4.2',
  '4.3',
  '5.1',
  '5.2',
  '6.1',
  '6.2',
  '7',
  '8',
  '9',
];

export interface Address {
  country: string;
  postalCode: string;
  city: string;
}

export interface CreateTenderRequest {
  origin: Address;
  destination: Address;
  pickupDate: string;
  deliveryDate: string;
  bidDeadline: string;
  commodity: string;
  weightKg: number;
  loadingMeters: number;
  palletCount?: number;
  equipmentType: EquipmentType;
  dangerousGoods: boolean;
  adrClass?: string;
  temperatureControlled: boolean;
  temperatureMinC?: number;
  temperatureMaxC?: number;
  currency: Currency;
}

export interface TenderSummary {
  id: number;
  origin: Address;
  destination: Address;
  pickupDate: string;
  deliveryDate: string;
  bidDeadline: string;
  commodity: string;
  weightKg: number;
  loadingMeters: number;
  palletCount: number | null;
  equipmentType: EquipmentType;
  dangerousGoods: boolean;
  adrClass: string | null;
  temperatureControlled: boolean;
  temperatureMinC: number | null;
  temperatureMaxC: number | null;
  currency: Currency;
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

export interface TenderDetail extends TenderSummary {
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

  create(request: CreateTenderRequest): Observable<TenderSummary> {
    return this.http.post<TenderSummary>('/api/tenders', request);
  }

  detail(id: number): Observable<TenderDetail> {
    return this.http.get<TenderDetail>(`/api/tenders/${id}`);
  }

  close(id: number): Observable<TenderSummary> {
    return this.http.post<TenderSummary>(`/api/tenders/${id}/close`, null);
  }

  addRemark(id: number, text: string): Observable<RemarkSummary> {
    return this.http.post<RemarkSummary>(`/api/tenders/${id}/remarks`, { text });
  }

  addOffer(id: number, supplierName: string, amount: number): Observable<OfferSummary> {
    return this.http.post<OfferSummary>(`/api/tenders/${id}/offers`, { supplierName, amount });
  }
}
