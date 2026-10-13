# Print a tender's shipment data from its detail page

Depends on `stories/freight-tenders/tender-detail-grouped-shipment-data.md`
and `stories/freight-tenders/award-tender-to-offer.md`.

## Problem

The shipment data of a tender -- route, dates, cargo, vehicle -- is what a
dispatcher hands to the warehouse or takes into a call with a carrier. The
only way to get it on paper is the browser's print command on the detail
page, which also prints the back link, the buttons, the offers table with
its prices, the remarks and both add-forms, spread over several pages.

## What to build

A frontend-only change: a "Drucken" action on the detail page that opens a
print view of the tender's shipment data in a new browser tab. The print
view contains the "Sendungsdaten" and nothing about offers or remarks, and
fits on one A4 page. No backend change.

### Print action on the detail page

- A "Drucken" link in the header row's action group, to the left of
  "Ausschreibung schließen". It is a real
  `<a target="_blank" rel="noopener">` to the print view's route, styled as
  `btn-secondary`, `data-testid="print-tender"`.
- It is shown for every loaded tender -- open, awarded or closed -- and not
  in the loading and load-error states. When the close button is absent, the
  link stays at the right end of the header row.
- At 600px and narrower it stacks below the title and pill together with the
  close button, as the close button does today.
- The detail page itself does not change otherwise and stays open in its own
  tab, with its state (sorting, form input) untouched.

### Print view

A new route, `/tenders/:id/print`, in its own flat feature folder. It loads
the tender through `TenderApiService` like the detail page does.

```
[ Drucken ]                                         <- screen only

Hamburg → Rotterdam
Ausschreibung 42 · Offen

Sendungsdaten
┌─ Strecke ──────────────────────┐  ┌─ Termine ──────────────────────┐
│ ...                            │  │ ...                            │
└────────────────────────────────┘  └────────────────────────────────┘
┌─ Ladung ───────────────────────┐  ┌─ Fahrzeug und Konditionen ─────┐
│ ...                            │  │ ...                            │
└────────────────────────────────┘  └────────────────────────────────┘
```

- **Title**: the route, `<h1>`, same text as the detail page's title
  (`data-testid="page-title"`).
- **Identification line**: "Ausschreibung" plus the tender's id, then " · "
  and the German status label as plain text -- no pill, since background
  colors are not printed by default (`data-testid="print-meta"`).
- **Sendungsdaten**: the heading and the same four cards as on the detail
  page, with the same rows, labels, values and formats, in the same order
  (`data-testid="shipment-data"` and the existing card and row test ids).
  The bid deadline keeps its "(heute)"/"(abgelaufen)" suffix.
- **Not on the page**: back link, summary line, close and award actions,
  explanation notices, the "Angebote" section, the "Bemerkungen" section and
  both add-forms.
- **"Drucken" button**: `btn-primary`, above the title,
  `data-testid="print-button"`. Selecting it calls `window.print()`. It is
  visible on screen and hidden in print.
- The browser tab's title is "Ausschreibung" plus the route, for example
  "Ausschreibung Hamburg → Rotterdam", so the tab is distinguishable from
  the detail page and a "save as PDF" gets a meaningful file name.

### Paper layout

- `@page { size: A4 portrait; margin: 15mm; }`.
- The whole print view fits on one A4 page for any tender, including the
  longest allowed commodity text and a tender with dangerous goods and a
  temperature range.
- The cards keep their two-column grid on paper regardless of the 600px
  breakpoint, and no card is split across a page break
  (`break-inside: avoid`).
- Black text on white, the cards' 1px border kept; nothing depends on a
  background color being printed.
- On screen the view is the same content in the app's normal page container,
  so what the dispatcher sees in the tab is what the sheet will show.

### States

- Loading: "Ausschreibung wird geladen…" (`data-testid="loading"`).
- Load error or a non-numeric id: the detail page's existing German
  load-error message (`data-testid="load-error"`).
- In both states the "Drucken" button and the cards are not rendered.

### Documentation

- `freight-tenders/README.md`: the `/tenders/:id` row mentions the print
  action; the route table gains `/tenders/:id/print`.
- `EXPERIENCE.md`: an Information Architecture row for the print view
  (reached from the detail page, opens in a new tab), a Component Patterns
  row for the print action, and a note that this is the app's only link that
  opens a new tab.
- `DESIGN.md`: Components gains the print view's paper layout as written
  above.

### Clarifications

- The print dialog does not open by itself when the tab loads; the
  dispatcher starts it with the "Drucken" button or the browser's own print
  command. Both produce the same sheet.
- The print view loads its own data, so it shows the tender as stored at the
  moment the tab is opened, and it works when its URL is opened directly or
  reloaded.
- The print view is a snapshot: it does not refresh when the tender changes
  in the other tab.
- Printing the detail page itself with the browser's print command is not
  changed by this story.
- The tender id is shown as the plain number the API returns.
- The detail page and the print view must show identical card content.
  Whether that is achieved by extracting the cards into a shared component
  or otherwise is the implementer's choice, as long as the rows are not
  defined twice.

### Implementation choices

Anything this story does not specify -- class and method names, how a rule or
query is implemented, how components and styles are split, test structure --
is the implementer's choice. Follow the conventions in
`freight-tenders/backend/AGENTS.md` and `freight-tenders/frontend/AGENTS.md`
and prefer the simplest option; none of it needs a decision from the story
author.

## Why

The shipment data is the part of a tender that leaves the screen: it goes to
the loading ramp, into a folder, or to a carrier on the phone. Offers and
remarks are internal -- competing prices do not belong on a sheet that gets
passed around. A dedicated view in its own tab gives one clean page without
taking the dispatcher away from the tender they are working on.

## Acceptance

- A loaded tender's detail page shows a "Drucken" link in the header for
  open, awarded and closed tenders; it points to `/tenders/:id/print` and
  opens in a new tab (`target="_blank"`, `rel="noopener"`).
- The link is not rendered in the detail page's loading and load-error
  states.
- `/tenders/:id/print` shows the route title, the identification line with
  tender id and German status label, and the "Sendungsdaten" section with
  the four cards and the same rows and values as the detail page.
- The print view contains no offers, no remarks, no add-forms, no back link
  and no close or award action.
- Selecting the print view's "Drucken" button calls `window.print()` once;
  the print dialog is not opened on load.
- The "Drucken" button is hidden in print; the print stylesheet sets A4
  portrait and keeps the cards in two columns.
- A tender with a 200-character commodity, dangerous goods and a temperature
  range prints on a single A4 page.
- Opening `/tenders/:id/print` directly for an unknown or non-numeric id
  shows the German load-error message and no "Drucken" button.
- Existing `data-testid` values on the detail page are kept.
- All new UI text is German; assertions go through `data-testid`.
- `EXPERIENCE.md`, `DESIGN.md` and `freight-tenders/README.md` are updated as
  described.
- Existing frontend tests keep passing; the new behavior has test coverage;
  `npm run lint`, `npm run build` and `npm test -- --watch=false` pass.
