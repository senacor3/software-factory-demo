---
schema_version: 1
story_slug: tender-detail-grouped-shipment-data
stage: review
status: findings-open
updated: 2026-10-13T10:21:45Z
---

## Findings

- **freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts**: The plan's Tests list was not implemented. The spec has no test for the summary line (tender-summary), the four data cards and their rows, the fallback values (Keine Angabe / Nein / Keine Vorgabe versus pallet count / Ja, ADR-Klasse 3 / 2 bis 8 °C), or the (abgelaufen) / (heute) / closed-tender deadline text. It also has no test for Angebote preceding Bemerkungen in the DOM, offer amounts in a non-EUR currency (CHF) with the currency-named amount label, or the absence of cards and summary in the loading and load-error states. No grep match in the spec for tender-summary, card-*, CHF, or Sendungsdaten. The new rendering logic (summaryLine, bidDeadlineText, palletText, dangerousGoodsText, temperatureText, formatAmount currency) is therefore unverified. The only mention of 'euro amounts' is an existing test.
