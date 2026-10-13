import {
  isBidDeadlinePassed,
  isDeliveryLate,
  isOfferExpired,
  cargoHint,
  deadlineHint,
  formatAmount,
  formatDate,
  formatLoadingMeters,
  formatWeight,
  localToday,
} from './tender-format';
import { tenderSummary } from './tender-test-data';

describe('tender formatting helpers', () => {
  it('formats an ISO date as dd.MM.yyyy', () => {
    expect(formatDate('2026-10-20')).toBe('20.10.2026');
  });

  it('formats weight with a German thousands separator', () => {
    expect(formatWeight(18500)).toBe('18.500 kg');
  });

  it('formats loading meters with a decimal comma', () => {
    expect(formatLoadingMeters(13.6)).toBe('13,6 ldm');
  });

  it('formats an amount in the given currency', () => {
    expect(formatAmount(1450, 'EUR')).toBe('1.450,00 €');
  });

  it('joins ADR class and temperature range in the cargo hint', () => {
    const tender = tenderSummary({
      dangerousGoods: true,
      adrClass: '3',
      temperatureControlled: true,
      temperatureMinC: 2,
      temperatureMaxC: 8,
    });

    expect(cargoHint(tender)).toBe('ADR 3 · 2 bis 8 °C');
  });

  it('returns an empty cargo hint when neither ADR nor temperature applies', () => {
    expect(cargoHint(tenderSummary())).toBe('');
  });

  it('builds the local date from the given instant', () => {
    expect(localToday(new Date(2026, 9, 5, 23, 30))).toBe('2026-10-05');
  });

  it('hints "heute" and "abgelaufen" for open tenders only', () => {
    expect(deadlineHint('2026-10-16', 'OPEN', '2026-10-16')).toBe('heute');
    expect(deadlineHint('2026-10-15', 'OPEN', '2026-10-16')).toBe('abgelaufen');
    expect(deadlineHint('2026-10-17', 'OPEN', '2026-10-16')).toBe('');
    expect(deadlineHint('2026-10-16', 'CLOSED', '2026-10-16')).toBe('');
    expect(deadlineHint('2026-10-15', 'CLOSED', '2026-10-16')).toBe('');
  });
});

describe('isOfferExpired', () => {
  it('is true only when the validity ended before today', () => {
    expect(isOfferExpired('2026-10-12', '2026-10-13')).toBe(true);
    expect(isOfferExpired('2026-10-13', '2026-10-13')).toBe(false);
    expect(isOfferExpired('2026-10-14', '2026-10-13')).toBe(false);
  });
});

describe('isDeliveryLate', () => {
  it('is true only when the offer delivers strictly after the tender date', () => {
    expect(isDeliveryLate('2026-10-23', '2026-10-22')).toBe(true);
    expect(isDeliveryLate('2026-10-22', '2026-10-22')).toBe(false);
    expect(isDeliveryLate('2026-10-21', '2026-10-22')).toBe(false);
  });
});

describe('isBidDeadlinePassed', () => {
  it('is true only for an open tender whose deadline is before today', () => {
    expect(isBidDeadlinePassed('2026-10-12', 'OPEN', '2026-10-13')).toBe(true);
    expect(isBidDeadlinePassed('2026-10-13', 'OPEN', '2026-10-13')).toBe(false);
    expect(isBidDeadlinePassed('2026-10-12', 'CLOSED', '2026-10-13')).toBe(false);
  });
});
