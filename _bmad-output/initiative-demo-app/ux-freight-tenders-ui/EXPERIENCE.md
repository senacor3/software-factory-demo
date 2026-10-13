---
name: Freight Tenders
status: final
sources:
  - ../epic-demo-app/epic-demo-app.md
updated: 2026-10-12
---

# Freight Tenders — Experience Spine

Responsive web, desktop-primary. Angular (standalone components) on the existing `freight-tenders/frontend`. No component library — plain Angular + hand-rolled components per `DESIGN.md`. Single-tenant, no auth: anyone with the URL can create/view/extend tenders, matching the existing app's scope. `DESIGN.md` is the visual identity reference; this spine is the behavior.

## Information Architecture

| Surface | Reached from | Purpose |
|---|---|---|
| Tender overview (`/`) | App open, "Abbrechen" from either other surface | Two sortable tables — open tenders, closed tenders — each with the shipment at a glance (Von, Nach, Abholung, Ladung, Fahrzeug, Angebotsfrist, Angebote), and the entry point to create a new one |
| Create tender (`/tenders/new`) | "Neue Ausschreibung erstellen" link on overview | Form with five field groups (Strecke, Termine, Ladung, Fahrzeug, Ausschreibung) for the full shipment data → creates an open tender, returns to overview |
| Tender detail (`/tenders/:id`) | Selecting a row in either overview table; "Zurück zur Übersicht" back link returns to the overview | One tender's full picture: identity, status, a one-line summary, the shipment data in four cards (Strecke, Termine, Ladung, Fahrzeug und Konditionen), a sortable offers table with an add-form, a sortable remarks table with an add-form — both forms disabled once closed |

No surface beyond these three; this redesign changes how they look and how their lists are presented (table vs. plain list), not what they do. → Composition reference: `mockups/tender-overview.html`, `mockups/tender-detail.html`. Spine wins on conflict.

## Voice and Tone

Microcopy stays German per the epic's existing boundary (backend/API/domain/docs stay English; UI text is German). Brand posture lives in `DESIGN.md.Brand & Style` — direct and factual, matching the "confident industrial" visual language: state what happened, not how the user should feel about it.

| Do | Don't |
|---|---|
| "Keine offenen Ausschreibungen vorhanden." | "Hier gibt's leider noch nichts zu sehen! 😊" |
| "Die Ausschreibung wurde nicht gefunden oder konnte nicht geladen werden." | "Huch, da ist wohl etwas schiefgelaufen." |
| "Diese Ausschreibung ist geschlossen, daher können keine weiteren Bemerkungen oder Angebote hinzugefügt werden." | "Diese Ausschreibung ist leider zu." |
| "Erstellen" / "Bemerkung hinzufügen" / "Angebot hinzufügen" | "Los geht's!" / "Jetzt hinzufügen!" |

## Component Patterns

Behavioral. Visual specs live in `DESIGN.md.Components`.

| Component | Use | Behavioral rules |
|---|---|---|
| Sortable table | Overview (open/closed tender lists), detail page (remarks, offers) | Select a column header to sort ascending by that column; select the same header again to reverse to descending; select a different header to switch the sort column (always single-column, per the recorded decision). Default sort: newest-first by id until a user sorts, so a newly added row appears at the top. Sort state is page-local — not persisted across navigation. |
| Back link | Detail page, first element in `<main>`, in every state (loading, error, loaded) | "← Zurück zur Übersicht" navigates to `/`; the arrow is decorative (`aria-hidden`), the German text is the accessible name. |
| Data card | Detail page, "Sendungsdaten" section: Strecke, Termine, Ladung, Fahrzeug und Konditionen | Each card is an `h3` plus a label/value list; every row always renders, with "Keine Angabe" / "Nein" / "Keine Vorgabe" as fallbacks. The Angebotsfrist row adds "(abgelaufen)" or "(heute)" for an open tender. Cards sit two per row and stack at 600px and narrower. Tab order: back link, close button, offers (sort, form), remarks (sort, form). |
| Status pill | Detail-page header only; the overview rows carry no status, their table already says it (inline right of the title, on the same row as the close button) | `status-pill-open`/`status-pill-closed` per `DESIGN.md`; label is "Offen"/"Geschlossen", never the raw backend value. |
| Create-tender form | `/tenders/new` | Five `<fieldset>` groups with a `<legend>` in `{typography.title}`; fields within a group sit side by side and stack at 600px and narrower. "ADR-Klasse" and the two temperature fields appear only while "Gefahrgut (ADR)" / "Temperaturgeführt" is checked. The same rules as the backend apply: a touched, invalid field shows a German message directly below it in `{colors.error}`, cross-field messages under the field to fix; submit disabled until the form is valid. Success navigates to `/`; failure handled per State Patterns → Form submit failed, form state preserved so the user can retry without retyping. |
| Add-remark / add-offer form | Detail page, inside each table's own section | One field-set per table (remark: free text; offer: supplier + amount). Submitting adds the new row to that table without a full page reload — at the top by default, or at its sorted position when a column is active. Both forms disable (fields + submit) together when the tender is closed, replaced by one shared explanation line above both — not duplicated per form. |
| Empty state | Any table with no rows | Centered `{typography.caption}` text inside the table's body area (not a full-page takeover), for example "Keine Bemerkungen vorhanden." |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Loading | Overview, detail | A loading line in place of the table or content area, `{typography.caption}` — "Ausschreibungen werden geladen…" / "Ausschreibung wird geladen…". Never show a stale empty-state message while a request is still in flight (existing bug class this redesign must not reintroduce). |
| Empty table | Overview (one or both lists), detail (remarks/offers) | Caption-styled message inside that table's body; the table header row still renders so the user sees what *would* be sortable once rows exist. |
| Backend unreachable | Overview, detail | One caption-styled error message replacing the affected content; existing German copy is reused as-is. |
| Unknown tender id | Detail | Same error treatment as backend-unreachable, German not-found message, no crash. |
| Closed tender | Detail | Status pill shows "Geschlossen"; both add-forms disabled; one explanation line shown above them. After a successful close, focus moves to that explanation line (the close button it replaces is removed). |
| Form submit in flight | Create, add-remark, add-offer | Submit button disabled for the duration (prevents double-submit); no spinner needed at this scale — the round trip is local and fast. |
| Form submit failed | Create, add-remark, add-offer | Inline error message in `{colors.error}` directly below that form, above its submit button; fields keep their entered values. This is the canonical error-placement rule — see `DESIGN.md`'s Components → Forms for the visual spec. |

## Interaction Primitives

- **Select a column header** — the only sort interaction.
- **Select a table row (overview)** — navigates to that tender's detail page. The whole row is selectable, not just a link inside it, so scanning stays fast on a dense table.
- **Tab order** follows visual order: table headers (sort controls) → table rows → add-form fields → submit button, top to bottom on every surface.
- **Keyboard:** Enter submits the focused form; sortable headers are reachable and triggerable via Tab + Enter/Space, not mouse-only.

## Accessibility Floor

Behavioral; visual contrast lives in `DESIGN.md` (palette chosen for WCAG AA text contrast against its surfaces).

- WCAG 2.2 AA as the floor — this is an internal demo app, not a full audit target, but contrast and keyboard operability are not optional.
- Every sortable column header is a real button (or has `role="button"` + `tabindex`) with an `aria-sort` attribute reflecting its current state (`ascending`/`descending`/`none`), so a screen reader announces sort state, not just a visual triangle.
- Status pills carry the German text as real text content, never as color-only meaning (a color-blind user still reads "Offen"/"Geschlossen").
- Disabled form controls use `disabled` (not just visual dimming) so assistive tech announces them correctly; the shared explanation line sits immediately before the forms in DOM order, so it's read before a screen-reader user reaches the disabled fields.
- Focus is never trapped; `Escape` is not required anywhere since there are no modals in this app's surface set.

## Key Flows

### Flow 1 — Lena checks and closes out a tender (Lena, Dispositionsmitarbeiterin, Tuesday morning)

1. Lena opens the app and lands on the overview. Two tables: "Offene Ausschreibungen" above "Geschlossene Ausschreibungen", each with seven columns — Von, Nach, Abholung, Ladung, Fahrzeug, Angebotsfrist, Angebote — all but Fahrzeug sortable, so she sees route, dates, load and offer count without opening a tender.
2. She selects the "Nach" header on the open-tenders table to sort by destination — she's looking for everything headed to Rotterdam today.
3. She finds the Hamburg → Rotterdam row, checks its pickup date, load and lowest offer in the row itself, and selects it, landing on its detail page: status pill "Offen", a summary line, the four shipment-data cards, two offers in a sortable table, one existing remark.
4. She selects the offers table's "Betrag (EUR)" header to sort by amount, confirms the lowest offer is reasonable, and adds a remark noting she's accepted it.
5. **Climax:** the remark appears in the table instantly — no reload, no navigation away — and she can see her note sitting right below the offer she referenced, both still visible, before she moves to the next tender in her queue.

Failure: the remark submission fails (backend hiccup) — inline error appears below the remark form, her typed text stays in the field, she selects "Bemerkung hinzufügen" again without retyping.

### Flow 2 — Creating a new tender and watching it land (Lena, later that morning)

1. From the overview, Lena selects "Neue Ausschreibung erstellen".
2. She fills the five groups: "Strecke" with Bremen (DE) as "Von" and Antwerpen (BE) as "Nach", "Termine" with pickup and delivery dates, "Ladung" with the commodity, weight and loading meters, "Fahrzeug" with a vehicle type, and "Ausschreibung" with the bid deadline and currency. Then she selects "Erstellen".
3. **Climax:** she's returned to the overview, and the new Bremen → Antwerpen tender is already sitting at the top of the open-tenders table — in the default newest-first order, since sort state is page-local and resets on every visit — so she sees her own action land without having to look for it.

Failure: she sets the delivery date before the pickup date — "Die Zustellung darf nicht vor der Abholung liegen." appears under "Zustellung bis" and "Erstellen" stays disabled until she corrects it, so there's no failed request to recover from in the first place.

## Inspiration & Anti-patterns

- **Lifted from ford.de:** one saturated brand color reserved for primary action, everything else neutral; bold single-typeface hierarchy over mixed fonts; flat surfaces with a single border-based depth cue instead of shadows.
- **Rejected — card-grid layout for the tender lists:** ford.de's model carousels are built for browsing a handful of hero products; a dispatcher scanning dozens of tenders needs a table's density and sortability, not cards. The "card" idea from the source site doesn't survive contact with this app's actual task.
- **Rejected — hero imagery/video:** nothing in this app's data (origin/destination strings, remarks, offer amounts) benefits from photography; the confident-automotive feeling here comes from typography and color discipline alone.
- **Rejected — multi-column/shift-click sort:** per the recorded decision, single-column click-to-sort only — simpler to build and test, and this app's lists are small enough that one sort key is always enough to find what you need.
