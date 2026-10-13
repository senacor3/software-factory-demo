---
schema_version: 1
story_slug: tender-shipment-data-and-create-form
stage: analysis
status: awaiting-clarification
updated: 2026-10-13T08:57:06Z
---

## Open Questions

- Should the date rules compare 'today' in a specific zone (e.g. Europe/Berlin) or the Clock's default zone? The story only says an injectable Clock, so I assume the Clock bean's own zone (system default in production).
- The sample request uses postalCode '3011 AA' with a space, and the rules specify only a max length of 10. I assume no country-specific postal code format validation is wanted.
- The frontend country list has 13 countries, but the backend only requires two uppercase letters. I assume the backend does not restrict to that list.
