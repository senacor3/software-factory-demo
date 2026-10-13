---
schema_version: 1
story_slug: tender-shipment-data-and-create-form
stage: analysis
status: awaiting-clarification
updated: 2026-10-13T09:07:24Z
---

## Proposal

Replace the two free-text origin/destination strings with a full spot-tender model for one European road shipment, changing backend and frontend together.

Backend (flat `tender/` package, English). Add an embeddable `Address` (country, postalCode, city) and enums `EquipmentType`, `Currency` and `AdrClass` (or a validated string). `Tender` is extended with `@Embedded` origin/destination, using `@AttributeOverrides` for distinct columns, plus the dates, commodity, weightKg, loadingMeters (BigDecimal, scale 1), palletCount (nullable), equipmentType, dangerousGoods, adrClass, temperatureControlled, temperatureMinC/MaxC and currency. The old `Tender(String, String)` constructor is replaced. `CreateTenderRequest` becomes a record with Bean Validation annotations: `@Valid` on the nested `AddressRequest` record, `@Pattern("[A-Z]{2}")`, `@Size`, `@Min`/`@Max`, `@DecimalMin`/`@DecimalMax` with `@Digits(integer=2, fraction=1)`, and `@NotNull` on the required fields. The date and cross-field rules (pickup today or later, delivery not before pickup, bidDeadline today or later and not after pickup, ADR present only when dangerous, reefer required when temperature-controlled, temperature range both-or-neither and min <= max) are enforced by field-targeted constraints. Preferred approach: a class-level constraint validator that builds a `ConstraintViolation` with `addPropertyNode(...)` for the field the user must fix, since the handler reads field errors and would otherwise drop a global error. Alternatively, use `@AssertTrue` on a property named like the field. The validator needs the current date. Add a `Clock` bean (`Clock.system(ZoneId.of("Europe/Berlin"))`) and inject it into the validator through Spring's `SpringConstraintValidatorFactory`, so tests can override the Clock bean.

`TenderExceptionHandler` keeps reporting field errors, with nested paths such as `origin.postalCode` coming from the binding result. It also gains handlers for `HttpMessageNotReadableException`, which covers unknown enums and malformed dates, returning 400 in the standard shape with empty `violations`. `TenderResponse` and `TenderDetailResponse` gain all the new fields, with a nested `AddressResponse`. `TenderService.createTender` takes the request or its values, and the controller passes it through.

Frontend. `tender-api.ts` gets `TenderAddress`, `CreateTenderRequest` and the extended `Tender`/`TenderDetail` types, plus `EQUIPMENT_TYPE_LABELS`, `COUNTRY_LABELS` (13 countries), `CURRENCY` and `ADR_CLASSES` next to `STATUS_LABELS`. `create()` takes one typed object. The `tender-create` form is rebuilt as a nested reactive `FormBuilder.nonNullable.group` of five `<fieldset>`/`<legend>` groups in the specified order, with defaults DE and EUR. Validators mirror the backend: a custom cross-field validator on the group, or per-control validators that set errors on the named controls. `adrClass` and the temperature fields are rendered with `@if` only while their checkbox is checked, and the corresponding controls are disabled, so the values are dropped from `getRawValue`-based request building. Show German messages under touched, invalid fields via `data-testid` hooks in `{colors.error}`. "Erstellen" is disabled while the form is invalid or submitting. The scss gets a responsive layout that is side-by-side on desktop and stacked at 600px and narrower, with a wider card. The overview and detail templates switch to `origin.city`/`destination.city`, and the overview's column sort accessors are updated for the nested city.

Docs: update `freight-tenders/README.md` (tender description, POST row, /tenders/new row) and `EXPERIENCE.md` (IA row, Component Patterns row, Flow 2). Update the existing backend and frontend tests and fixtures to the new model.

## Subtasks

- Backend: add Address embeddable, AddressRequest/AddressResponse records, and EquipmentType, Currency enums (plus ADR class representation)
- Backend: extend Tender entity with all new fields (embedded origin/destination with attribute overrides) and replace the old constructor
- Backend: rewrite CreateTenderRequest with Bean Validation for every table rule, including field-targeted cross-field constraints (deliveryDate, bidDeadline, adrClass, equipmentType, temperatureMinC, temperatureMaxC)
- Backend: add a Clock bean fixed to Europe/Berlin and use it in the date validators so tests can override it
- Backend: extend TenderExceptionHandler with HttpMessageNotReadableException (unknown enum / malformed date) -> 400 in standard shape; verify nested paths like origin.postalCode are reported
- Backend: extend TenderResponse and TenderDetailResponse with all fields; update TenderService.createTender and TenderController
- Backend: update existing tests/fixtures (controller, service, persistence, repository) and add new validation tests
- Frontend: update tender-api.ts types, add label maps next to STATUS_LABELS, change create() to take one typed object
- Frontend: rebuild tender-create form (ts/html/scss) with five fieldset groups, conditional fields, cross-field validation, German messages under touched invalid fields, responsive layout
- Frontend: update overview and detail templates/sort accessors to use origin.city and destination.city
- Frontend: update existing specs and add form, api and conditional-field specs
- Update freight-tenders/README.md and EXPERIENCE.md
- Run mvn -B verify, mvn spotless:check, mvn spotbugs:check, npm run lint, npm run build, npm test -- --watch=false

## Tests

- Backend controller test: a valid payload returns 201 with every field, and GET list and GET by id return the same data
- Backend parametrized controller tests: one rejecting case per table rule returns 400 with a violations entry naming the field (e.g. origin.postalCode, weightKg, loadingMeters 13.7 or 3 decimals), and the repository count stays 0
- Backend: dangerousGoods=false with adrClass is rejected; dangerousGoods=true without adrClass is rejected; same for temperatureControlled and the min/max pair; min > max rejected on temperatureMinC
- Backend: temperatureControlled=true with equipmentType BOX is rejected with a violation on equipmentType
- Backend: unknown equipmentType/currency value and malformed date return 400 in the {error,message,path,timestamp,violations} shape
- Backend: date rules with a fixed test Clock (pickup yesterday, delivery before pickup, bidDeadline after pickup, bidDeadline today accepted at the boundary)
- Backend: persistence test that the embedded addresses and all new fields round-trip through H2
- Frontend tender-create spec: renders the five fieldsets in order, ADR-Klasse and the temperature fields appear only when their checkbox is checked, and unchecking removes the values from the POST body
- Frontend tender-create spec: German error message appears under a touched invalid field, the cross-field message appears under Zustellung bis and Fahrzeugtyp, and Erstellen is disabled while invalid or in flight
- Frontend tender-create spec: a successful submit sends the full typed request and navigates to /; a failed request shows the submit error and keeps the entered values
- Frontend tender-api and overview/detail specs: updated fixtures; the overview shows origin.city/destination.city and sorting by Von/Nach still works
