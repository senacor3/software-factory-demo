# Show the shipment data in groups on the tender detail page

Depends on `stories/freight-tenders/tender-shipment-data-and-create-form.md`.

## Problem

The detail page shows a tender's two city names, its status, its remarks and
its offers. Everything a carrier's price depends on -- dates, cargo, vehicle,
bid deadline -- is stored but not visible anywhere in the app after creation.
The page also puts remarks above offers, although the offers are what the
dispatcher comes to this page to compare.

## What to build

A frontend-only change to the detail page: a summary line under the title, a
"Sendungsdaten" section with four grouped cards, and offers moved above
remarks. No backend change. The header row (back link, title, status pill,
close button) keeps its layout and behavior.

### Layout

```
← Zurück zur Übersicht

Hamburg → Rotterdam  ( Offen )                      [ Ausschreibung schließen ]
Abholung 20.10.2026 · Zustellung 22.10.2026 · Planenauflieger · 18.500 kg

Sendungsdaten
┌─ Strecke ──────────────────────┐  ┌─ Termine ──────────────────────┐
│ Von    20457 Hamburg           │  │ Abholung       20.10.2026      │
│        Deutschland             │  │ Zustellung     22.10.2026      │
│ Nach   3011 AA Rotterdam       │  │ Angebotsfrist  16.10.2026      │
│        Niederlande             │  │                                │
└────────────────────────────────┘  └────────────────────────────────┘
┌─ Ladung ───────────────────────┐  ┌─ Fahrzeug und Konditionen ─────┐
│ Ware          Maschinenteile … │  │ Fahrzeugtyp  Planenauflieger   │
│ Gewicht       18.500 kg        │  │ Währung      EUR               │
│ Lademeter     13,6 ldm         │  │                                │
│ Paletten      33               │  │                                │
│ Gefahrgut     Nein             │  │                                │
│ Temperatur    Keine Vorgabe    │  │                                │
└────────────────────────────────┘  └────────────────────────────────┘

Angebote
...
Bemerkungen
...
```

### Summary line

Directly under the header row, one line in `{typography.body}` and
`{colors.on-surface-variant}` with the four facts that identify the job at a
glance: pickup date, delivery date, vehicle type and weight, joined by " · ".
It wraps on narrow screens. `data-testid="tender-summary"`.

### Sendungsdaten

A section with heading "Sendungsdaten" and four cards. Each card is a titled
group (`<h3>` in `{typography.title}`) holding a description list (`<dl>`):
the label in `{typography.label}` and `{colors.on-surface-variant}`, the value
in `{typography.body}`.

| Card | Rows |
|---|---|
| Strecke | "Von" and "Nach": postal code and city on one line, the German country name below |
| Termine | "Abholung", "Zustellung", "Angebotsfrist" |
| Ladung | "Ware", "Gewicht", "Lademeter", "Paletten", "Gefahrgut", "Temperatur" |
| Fahrzeug und Konditionen | "Fahrzeugtyp", "Währung" |

- Cards use the existing flat style: a 1px `{colors.outline-variant}` border,
  `{spacing.gutter}` padding, no shadow. Two columns on desktop with
  `{spacing.gutter}` between cards, one column at 600px and narrower. The card
  style is a shared class in `src/styles.scss`.
- Every row is always rendered, so the cards do not change shape between
  tenders. Values that do not apply are spelled out: "Paletten" shows "Keine
  Angabe" without a pallet count, "Gefahrgut" shows "Nein" or "Ja, ADR-Klasse
  3", "Temperatur" shows "Keine Vorgabe" or "2 bis 8 °C".
- When the bid deadline has passed on an open tender, the "Angebotsfrist" value
  is followed by "(abgelaufen)", and by "(heute)" when it is today.
- Dates, numbers, vehicle type and country names use the same formats and
  label maps as the overview and the create form.

### Section order and offer amounts

- "Angebote" now comes before "Bemerkungen". Each section keeps its table, its
  add-form and its behavior. The closed-tender explanation still sits above
  both sections.
- Offer amounts are shown in the tender's currency instead of a fixed one, and
  the amount field's label names it, for example "Betrag (EUR)".

### Documentation

- `EXPERIENCE.md`: the detail page's Information Architecture row, a
  Component Patterns row for the data cards, Interaction Primitives' tab order,
  and Flow 1 steps 3-5 (offers now sit above remarks).
- `DESIGN.md`: Components gains the data card and the summary line.
- `freight-tenders/README.md`: the `/tenders/:id` row.
- `mockups/tender-detail.html` is updated to the new layout.

## Why

The detail page is where a dispatcher decides between offers, and they can
only judge a price against the job it is for. Grouping the data by the
questions it answers -- where, when, what, with which vehicle -- keeps a page
with sixteen facts readable, and putting offers first puts the page's main
task directly under the data it depends on.

## Acceptance

- A loaded tender shows the summary line with pickup date, delivery date,
  vehicle type and weight.
- The "Sendungsdaten" section shows the four cards with the rows listed above,
  in that order, for every tender.
- A tender without pallet count, dangerous goods or temperature control shows
  "Keine Angabe", "Nein" and "Keine Vorgabe"; a tender with them shows the
  pallet count, "Ja, ADR-Klasse" plus the class, and the temperature range.
- An open tender past its bid deadline shows "(abgelaufen)" next to the
  deadline; a closed tender does not.
- The "Angebote" section precedes the "Bemerkungen" section in the DOM, and
  both keep working as before for open and closed tenders.
- Offer amounts are formatted in the tender's currency.
- At 600px and narrower the cards stack in one column with no horizontal
  scrolling.
- The data cards are not rendered in the loading and load-error states.
- Existing `data-testid` values on the page are kept.
- All new UI text is German; assertions go through `data-testid`.
- Existing frontend tests keep passing; the new behavior has test coverage;
  `npm run lint`, `npm run build` and `npm test -- --watch=false` pass.
