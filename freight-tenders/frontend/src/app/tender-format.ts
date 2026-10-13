import { Currency, TenderStatus, TenderSummary } from './tender-api';

const LOCALE = 'de-DE';

const NUMBER = new Intl.NumberFormat(LOCALE);
const LOADING_METERS = new Intl.NumberFormat(LOCALE, { maximumFractionDigits: 1 });

// '2026-10-20' -> '20.10.2026'. Works on the string, so no time zone can shift the day.
export function formatDate(isoDate: string): string {
  const [year, month, day] = isoDate.split('-');
  return `${day}.${month}.${year}`;
}

export function formatWeight(weightKg: number): string {
  return `${NUMBER.format(weightKg)} kg`;
}

export function formatLoadingMeters(loadingMeters: number): string {
  return `${LOADING_METERS.format(loadingMeters)} ldm`;
}

export function formatAmount(amount: number, currency: Currency): string {
  return new Intl.NumberFormat(LOCALE, { style: 'currency', currency }).format(amount);
}

export function formatTemperatureRange(minC: number, maxC: number): string {
  return `${minC} bis ${maxC} °C`;
}

// Second line of the Ladung cell: "ADR <class>" and the temperature range, when they apply.
export function cargoHint(tender: TenderSummary): string {
  const parts: string[] = [];

  if (tender.dangerousGoods && tender.adrClass) {
    parts.push(`ADR ${tender.adrClass}`);
  }

  if (
    tender.temperatureControlled &&
    tender.temperatureMinC !== null &&
    tender.temperatureMaxC !== null
  ) {
    parts.push(formatTemperatureRange(tender.temperatureMinC, tender.temperatureMaxC));
  }

  return parts.join(' · ');
}

// Today's date in the browser's time zone, as an ISO date string.
export function localToday(now: Date = new Date()): string {
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${now.getFullYear()}-${month}-${day}`;
}

// Only an open tender can still run out of time, so a closed one never gets a hint.
export function deadlineHint(bidDeadline: string, status: TenderStatus, today: string): string {
  if (status !== 'OPEN') {
    return '';
  }

  if (bidDeadline === today) {
    return 'heute';
  }

  return bidDeadline < today ? 'abgelaufen' : '';
}

// An offer whose validity ended before today can no longer be accepted.
export function isOfferExpired(validUntil: string, today: string): boolean {
  return validUntil < today;
}

// The supplier offers delivery later than the tender asked for.
export function isDeliveryLate(offerDeliveryDate: string, tenderDeliveryDate: string): boolean {
  return offerDeliveryDate > tenderDeliveryDate;
}

// Only an open tender can still reject offers because of its deadline; a closed one has its own
// explanation.
export function isBidDeadlinePassed(
  bidDeadline: string,
  status: TenderStatus,
  today: string,
): boolean {
  return status === 'OPEN' && bidDeadline < today;
}
