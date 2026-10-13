---
schema_version: 1
story_slug: tender-shipment-data-and-create-form
stage: analysis
status: ready-for-review
updated: 2026-10-13T09:18:08Z
---

## Proposal

Replace the two free-text tender strings with a full spot-tender model for one European road shipment, changing backend and frontend together so the app keeps working end to end.

Backend (flat `tender/` package, records for DTOs, constructor injection):
- Add an embeddable `Address` (country, postalCode, city), used twice on `Tender` with `@AttributeOverrides` for origin_* and destination_* columns. Add `EquipmentType`, `Currency` enums, and keep `adrClass` as a String. Extend `Tender` with all the new fields and replace `Tender(String, String)` with a constructor or builder taking them.
- Rewrite `CreateTenderRequest` as a record with nested `AddressRequest`, using `@Valid` and field-level Bean Validation: `@Pattern("[A-Z]{2}")` on country, `@Size` on postalCode, city and commodity, `@NotNull` / `@Min` / `@Max` on weightKg, `@DecimalMin` / `@DecimalMax` plus `@Digits(integer=2, fraction=1)` on loadingMeters, the 1–66 range on palletCount, and the -30..30 range on both temperatures.
- Enforce the cross-field rules and clock-based date rules with per-field `@AssertTrue` methods on the record, so each violation is reported on the correct field (`deliveryDate`, `bidDeadline`, `adrClass`, `equipmentType`, `temperatureMinC`, `temperatureMaxC`). The `isXxxValid` naming makes the property name equal the field name, and `TenderExceptionHandler` already reports field errors. Because the "today" rules need a `Clock`, either use a custom constraint validator that gets the `Clock` injected (Spring's `SpringConstraintValidatorFactory` supports this), or check the date rules in the service and raise a `MethodArgumentNotValidException`-style failure. I prefer the custom class-level validator, which adds violations via `addPropertyNode(...).addConstraintViolation()`. Class-level constraints with property nodes surface as field errors in the binding result, so they will not be dropped.
- Add a production `Clock` bean in a small config class in the `tender` package, fixed to `Clock.system(ZoneId.of("Europe/Berlin"))`. Tests inject a fixed clock.
- Extend `TenderExceptionHandler` with handlers for `HttpMessageNotReadableException` (unknown enum, malformed date, bad JSON) that return 400 in the standard shape with empty `violations`. Make sure nested paths such as `origin.postalCode` come through as the field name. Also make sure any global errors from class-level constraints still end up as violations.
- Update `TenderService.createTender` to accept the request, or a command object, and build the entity. Update `TenderResponse` and `TenderDetailResponse` to return all fields, with a nested address record and the same shape in create, list, close and detail.

Frontend:
- In `tender-api.ts`, add types `Address`, `EquipmentType`, `Currency` and `CreateTenderRequest`. Add `EQUIPMENT_LABELS` next to `STATUS_LABELS`, and change `create(request)` to take one typed object. Update `TenderSummary` and `TenderDetail` to the new shape.
- Rebuild `tender-create` with nested `FormBuilder.nonNullable` groups (origin and destination groups, with defaults DE and EUR). Use five `<fieldset>` / `<legend>` groups in the specified order, a country select with German names, and `type="date"` inputs. Use `@if` to render ADR-Klasse and the two temperature fields only while their checkboxes are checked. Toggle validators and values in a `valueChanges` or effect, so unchecking removes the values from the request.
- Add cross-field validators (delivery ≥ pickup, deadline between today and pickup, temperature min ≤ max, temperature-controlled requires REEFER) that set errors on the named controls, with German messages shown under touched and invalid fields in the error colour. Keep "Erstellen" disabled while the form is invalid or a request is in flight. Keep the existing submit-error handling and navigation. Widen the form card and add a responsive grid that stacks at 600px and narrower.
- Overview and detail: show `origin.city` and `destination.city` in the columns and title, and keep the sort accessors working on those nested values.

Docs: update `freight-tenders/README.md` (tender description, `POST /api/tenders` row, `/tenders/new` row) and `EXPERIENCE.md` (Information Architecture row, Component Patterns row, Flow 2).

Existing tests (controller, service, repository, persistence, and the frontend api, create, overview and detail specs) are migrated to the new model. The H2 in-memory database with `ddl-auto: update` means no migration is needed.

## Subtasks

- Backend: add Address embeddable, EquipmentType and Currency enums, and extend Tender with all new fields, replacing the origin/destination strings
- Backend: add a production Clock bean fixed to Europe/Berlin (config class in the tender package)
- Backend: rewrite CreateTenderRequest with nested address record and Bean Validation constraints for every table rule
- Backend: implement cross-field and clock-dependent rules (delivery/pickup/bidDeadline dates, adrClass, temperature range, REEFER requirement) so violations are named by the field to fix, and make sure they are not dropped by the handler
- Backend: extend TenderExceptionHandler to return the standard 400 error shape for unreadable bodies (unknown enum, malformed date) and for nested paths like origin.postalCode
- Backend: update TenderService.createTender and TenderController to take the new request; update TenderResponse and TenderDetailResponse to return all fields with nested addresses
- Backend: update existing tests (controller, service, repository, persistence) to the new model and add the new validation tests
- Frontend: update tender-api.ts types, add EQUIPMENT_LABELS and CURRENCY/country option lists next to STATUS_LABELS, and change create() to take one typed request object
- Frontend: rebuild the tender-create component, template and scss with five fieldset groups, nested form groups, conditional ADR and temperature fields, cross-field validators and German error messages under touched invalid fields, and a responsive layout
- Frontend: update the overview and detail to show origin.city and destination.city and keep column sorting working
- Frontend: update the api, create, overview, detail and app specs to the new model and add create-form tests
- Update freight-tenders/README.md and EXPERIENCE.md (IA row, component patterns row, Flow 2)
- Run mvn -B verify, spotless:check, spotbugs:check, npm run lint, npm run build and npm test -- --watch=false

## Tests

- TenderControllerTest: a valid request, including the example from the story, returns 201 with every field, and GET list and GET by id return the same data
- TenderControllerTest: a parameterized rejection case for each table rule (country not two uppercase letters, over-long postalCode or city, missing address parts, pickup in the past, delivery before pickup, deadline in the past or after pickup, commodity over 200 characters, weightKg 0 or 40001, loadingMeters 0.0, 13.7 or two fraction digits, palletCount 0 or 67, invalid adrClass, temperature out of range, missing currency) returns 400 with a violation naming the field, and nothing is stored
- TenderControllerTest: boundary cases are accepted (pickup and deadline equal to today, delivery equal to pickup, deadline equal to pickup, weight 40000, loadingMeters 13.6, palletCount 66, 3011 AA postal code)
- TenderControllerTest: adrClass is rejected when dangerousGoods is false and required when true; the same pairing applies to the temperature fields and temperatureControlled; min above max is reported on the temperature fields
- TenderControllerTest: temperatureControlled true with a non-REEFER equipmentType returns a violation on equipmentType
- TenderControllerTest: an unknown equipmentType or currency, a malformed date and a malformed JSON body return 400 in the standard error shape, not Spring's default body
- TenderControllerTest: nested violations appear as origin.postalCode and destination.city; a fixed Clock makes the date tests independent of the run date
- Clock configuration test: the production bean is in the Europe/Berlin zone
- TenderRepositoryTest and TenderServicePersistenceTest: a tender with embedded addresses and all new fields round-trips through H2
- tender-api.spec.ts: create() posts the full typed object to /api/tenders, and the label maps have entries for each enum value
- tender-create.spec.ts: five fieldsets in order; defaults DE and EUR; ADR-Klasse and temperature fields render only when their checkboxes are checked, and unchecking removes their values from the request; German error messages appear below touched invalid fields, including delivery-before-pickup and non-REEFER with temperature control; the submit button is disabled while invalid or submitting; success navigates to /; a failed request shows the submit error and keeps values
- tender-overview.spec.ts and tender-detail.spec.ts: the city is shown for origin and destination, and sorting by Von and Nach still works
- Full gates: mvn -B verify, mvn spotless:check, mvn spotbugs:check, npm run lint, npm run build, npm test -- --watch=false
