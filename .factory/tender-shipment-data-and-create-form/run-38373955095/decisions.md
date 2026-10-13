---
schema_version: 1
story_slug: tender-shipment-data-and-create-form
stage: analysis
status: awaiting-clarification
updated: 2026-10-13T09:07:24Z
---

## Open Questions

- Should the ADR class field accept only the 13 listed values via an enum (JSON values like "4.1" need @JsonValue/@JsonCreator) or a string with @Pattern/@Size? The story says 'text', and either satisfies it.
- Should a tender with bidDeadline == pickupDate be valid? The story says 'not after pickupDate', so yes. This is confirmed as an inclusive boundary unless told otherwise.
