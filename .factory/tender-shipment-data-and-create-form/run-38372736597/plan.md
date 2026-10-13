---
schema_version: 1
story_slug: tender-shipment-data-and-create-form
stage: analysis
status: awaiting-clarification
updated: 2026-10-13T08:57:06Z
---

## Proposal

Replace the flat origin/destination strings with a full spot-tender model, end to end.

Backend (flat `tender/` package, English): add an embeddable `Address` (country, postalCode, city) and enums `EquipmentType`, `Currency` (plus an ADR class set). `Tender` gets all new fields (two `@Embedded` addresses with attribute overrides, dates, weight, loading meters as BigDecimal scale 1, optional palletCount, flags, nullable adrClass/temperature range, currency); the constructor/`TenderService.createTender` take the validated request. `CreateTenderRequest` becomes a record with Jakarta constraints on each field, nested `@Valid` addresses (violations such as `origin.postalCode`), and cross-field rules implemented as `@AssertTrue` methods on properties named for the field to fix (e.g. `isDeliveryDateValid` is reported under `deliveryDate`, likewise `bidDeadline`, `adrClass`, `equipmentType`, `temperatureMinC`, `temperatureMaxC`). Bean Validation reports these as field errors, which `TenderExceptionHandler` already collects. Date rules ("today or later") need an injectable `java.time.Clock` bean. Because `@Past`/`@FutureOrPresent` on a request record use the validator's own clock, use a custom `ClockProvider` for the `LocalValidatorFactoryBean`, or check the "today" rules in a small custom constraint that takes the Clock. The first is the preferred option. Extend `TenderExceptionHandler` with handlers for `HttpMessageNotReadableException` (unknown enum values, malformed dates) returning 400 in the standard shape with empty violations. Also handle the global-error case (`getGlobalErrors`) defensively. `TenderResponse` and `TenderDetailResponse` carry all fields in the same shape (nested address records), mapped in the controller. Update the controller, service, and existing tests.

Frontend: add typed `CreateTenderRequest`, `Address`, and the other model types to `tender-api.ts`, with `EQUIPMENT_LABELS`, `COUNTRY_LABELS`, and `CURRENCY` maps next to `STATUS_LABELS`. `TenderApiService.create` takes one typed object. Rebuild `tender-create` as a nested `FormBuilder.nonNullable` group with five `<fieldset>/<legend>` groups in the specified order. Validators mirror the backend, including group-level or per-control cross-field validators that put errors on the named control (deliveryDate vs pickup, bidDeadline vs pickup and today, ADR/temperature conditional controls added or removed on checkbox change, REEFER requirement on equipmentType). Show German messages under touched invalid fields, with `data-testid` attributes throughout. Disable "Erstellen" while invalid or submitting, and keep the existing error handling and navigation. Update the SCSS for side-by-side fields that stack at 600px and a wider card. Overview and detail show `origin.city` and `destination.city`, and overview sorting accessors use those. Update README.md and EXPERIENCE.md as listed.

## Subtasks

- Backend: add Address embeddable, EquipmentType, Currency enums and the ADR class allowed set in the tender package
- Backend: extend Tender entity with all new fields and update its constructor, getters and TenderService.createTender
- Backend: add a java.time.Clock bean and wire the Bean Validation ClockProvider to it so 'today or later' rules are testable
- Backend: rewrite CreateTenderRequest as a record with field constraints, nested @Valid addresses and @AssertTrue cross-field checks on properties named for the field to fix (deliveryDate, bidDeadline, adrClass, equipmentType, temperatureMinC, temperatureMaxC)
- Backend: extend TenderResponse and TenderDetailResponse with all fields (nested address records) and update the controller mapping
- Backend: add TenderExceptionHandler handling of HttpMessageNotReadableException (unknown enum, malformed date) returning the standard 400 shape, and handle global errors defensively
- Backend: update existing controller, service, persistence and repository tests to the new model and add validation tests
- Frontend: add typed models and label maps (equipment, country, currency) to tender-api.ts and change TenderApiService.create to take one typed object; update tender-api.spec.ts
- Frontend: rebuild tender-create form (ts/html/scss) with five fieldsets, conditional ADR and temperature controls, cross-field validators, German per-field messages, disabled submit while invalid or in flight, and responsive layout
- Frontend: switch overview columns, sorting and detail title to origin.city / destination.city and update their specs
- Frontend: rewrite tender-create.spec.ts for the new form behaviours
- Docs: update freight-tenders/README.md (tender description, POST /api/tenders row, /tenders/new row) and EXPERIENCE.md (IA row, Component Patterns row, Flow 2)
- Run mvn -B verify, spotless:check, spotbugs:check, npm run lint, npm run build and npm test -- --watch=false and fix findings

## Tests

- TenderControllerTest: valid full request returns 201 with every field including nested origin/destination, status OPEN; GET list and GET by id return the same data
- TenderControllerTest: a rejecting case per table rule (country not 2 uppercase letters, postalCode >10, city >100 or blank, pickupDate in the past, deliveryDate before pickupDate, bidDeadline in the past or after pickupDate, commodity >200, weightKg 0 and 40001, loadingMeters 0.0, 13.7 and two fraction digits, palletCount 0 and 67, missing required booleans) returns 400 with a violation naming the field (e.g. origin.postalCode) and nothing stored
- TenderControllerTest: adrClass present with dangerousGoods=false and absent with true are both rejected under adrClass; an invalid ADR class value is rejected
- TenderControllerTest: temperatureControlled=true with equipmentType BOX is rejected under equipmentType; temperature range present/absent mismatch and min>max rejected under temperatureMinC/temperatureMaxC; values outside -30..30 rejected
- TenderControllerTest: unknown equipmentType or currency and a malformed date return 400 in the standard {error,message,path,timestamp,violations} shape
- Date-rule tests with a fixed Clock bean so results do not depend on the day the tests run
- TenderServiceTest, TenderServicePersistenceTest and TenderRepositoryTest updated to the new Tender model, including persisting embedded addresses and nullable ADR/temperature fields
- tender-create.spec.ts: renders five fieldsets in order; defaults DE and EUR; ADR class and temperature fields render only when their checkbox is checked and are removed from the request when unchecked
- tender-create.spec.ts: German message under each invalid touched field, including 'Die Zustellung darf nicht vor der Abholung liegen.' under delivery and 'Temperaturgeführte Ladung erfordert einen Kühlauflieger.' under vehicle type
- tender-create.spec.ts: submit disabled while invalid and while in flight; success posts the full typed body and navigates to /; failure shows the submit error and keeps entered values
- tender-api.spec.ts: create posts the typed object to /api/tenders
- tender-overview.spec.ts and tender-detail.spec.ts: show origin.city / destination.city; sorting by Von/Nach still works
