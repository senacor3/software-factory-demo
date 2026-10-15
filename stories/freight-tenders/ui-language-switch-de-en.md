# Switch the UI language between German and English

Covers every page and every piece of UI text that exists in the frontend when
this story is implemented, including those added by earlier stories in
`stories/freight-tenders/`.

## Problem

The UI is German only. Every label, heading, button, message and status pill
is hardcoded German text, and dates, numbers and amounts are always formatted
as `de-DE`. Carriers' contacts, colleagues from other sites and anyone else
who does not read German cannot use the app without guessing.

## What to build

A frontend-only change: the UI is available in German and English, German is
the default, and a language switch that is visible on every page changes the
language immediately. No backend change -- the API, domain values and field
names stay English as today.

### Language switch

```
                                                         [ DE | EN ]   <- app bar, every page
← Zurück zur Übersicht

Hamburg → Rotterdam
...
```

- A slim app bar across the top of every route, rendered once in the app
  shell (`app.html`) above the `<router-outlet />`, so no page has to add it.
  It contains only the switch, right-aligned within the app's page container
  width.
- The bar is `position: sticky; top: 0`, so the switch stays visible while the
  page scrolls, in every state of every page (loading, load error, empty,
  loaded, form failure). It stays on the right at 600px and narrower and does
  not cover page content.
- The switch is a segmented control with two buttons, "DE" and "EN"
  (`data-testid="language-de"`, `data-testid="language-en"`), wrapped in an
  element with `role="group"` and an accessible name ("Sprache" in German,
  "Language" in English; `data-testid="language-switch"`).
- The active language's button has `aria-pressed="true"` and the
  `btn-primary` look; the other has `aria-pressed="false"` and the
  `btn-secondary` look. Selecting the active language does nothing.
- Each button carries its own `lang` attribute (`lang="de"` / `lang="en"`) and
  a full-name `title`/accessible name ("Deutsch", "English"), so screen
  readers announce it correctly regardless of the current UI language.
- The switch is keyboard-operable with the app's existing focus style.
- On the print view (`/tenders/:id/print`), if present, the app bar is shown
  on screen and hidden in print, like the print view's "Drucken" button.

### Switching behavior

- Selecting a language changes all UI text on the current page at once,
  without a page reload and without a navigation. The current route, form
  input, validation state, table sorting and loaded data are kept; no request
  is sent to the backend.
- The choice is stored in `localStorage` (key `freight-tenders.language`,
  value `de` or `en`) and applied on the next visit, on reload, in new tabs
  (including the print view's new tab) and when a URL is opened directly.
- With no stored value, or an unreadable or unknown one, the UI is German.
  The browser's language setting is not used. If `localStorage` is not
  available, switching still works for the current page session and the next
  load starts in German.
- `<html lang>` follows the active language (`de` / `en`).
- The browser tab title follows the active language: "Frachtausschreibungen" /
  "Freight tenders", and on the print view "Ausschreibung <route>" /
  "Tender <route>".

### What is translated

- Every piece of text the frontend itself renders: page headings, section
  headings, field labels and legends, placeholders, button and link text,
  table headers, captions and hints ("heute", "abgelaufen",
  "nach Wunschtermin", "Zuschlag", ...), notices, empty states, loading and
  error messages, validation messages, confirmation texts, `aria-label`s and
  `title`s, and the status labels.
- Values that come from the backend as English codes keep being mapped at
  render time, now to the active language: status `OPEN`/`AWARDED`/`CLOSED`
  is "Offen"/"Vergeben"/"Geschlossen" or "Open"/"Awarded"/"Closed", and the
  same applies to every other enum the UI shows a label for (vehicle type,
  ADR class captions, currency names if shown, ...).
- **Not translated**: data a user typed in -- route places, addresses,
  commodity, remarks, supplier names, offer notes. It is shown as stored.

### Formats per language

| | DE (`de-DE`) | EN (`en-GB`) |
|---|---|---|
| Date | `20.10.2026` | `20/10/2026` |
| Number | `12.500 kg` | `12,500 kg` |
| Loading meters | `13,6 ldm` | `13.6 ldm` |
| Amount | `1.250,00 €` | `€1,250.00` |
| Temperature range | `2 bis 8 °C` | `2 to 8 °C` |

- Dates stay formatted from the ISO string as today, so no time zone can shift
  the day.
- Units (`kg`, `ldm`, `°C`) and the ADR class values are the same in both
  languages.
- Form inputs keep accepting what they accept today; number inputs and native
  date pickers follow the browser, not the switch.

### English terminology

The English text uses these terms consistently:

| German | English |
|---|---|
| Ausschreibung | Tender |
| Angebot / Angebote | Offer / Offers |
| Anbieter | Supplier |
| Zuschlag / vergeben | Award / awarded |
| Angebotsfrist | Bid deadline |
| Sendungsdaten | Shipment data |
| Strecke | Route |
| Termine | Dates |
| Ladung | Cargo |
| Fahrzeug und Konditionen | Vehicle and terms |
| Abholung / Zustellung | Pickup / Delivery |
| Gefahrgut (ADR) | Dangerous goods (ADR) |
| Temperaturgeführt | Temperature-controlled |
| Lademeter | Loading meters |
| Bemerkungen | Remarks |
| Offen / Vergeben / Geschlossen | Open / Awarded / Closed |
| Gültig bis | Valid until |
| Ausschreibung schließen | Close tender |
| Zurück zur Übersicht | Back to overview |
| Drucken / Bearbeiten / Speichern / Abbrechen | Print / Edit / Save / Cancel |

Anything not in the table is translated in plain British English in the same
direct, factual tone as the German copy (`EXPERIENCE.md`, brand posture).

### Documentation

- `freight-tenders/frontend/AGENTS.md`: the Policy line "All user-facing text
  ... is German" becomes: all user-facing text exists in German and English
  through the translation mechanism this story introduces, German is the
  default, no UI string is hardcoded in a template or component, and new UI
  text needs both languages. Add where the translations live under "Where
  things are". (The file's content sits in a `bmad:context` block; update it
  in place.)
- `EXPERIENCE.md`: the microcopy paragraph (German only) is replaced by the
  two-language rule above; a Component Patterns row for the language switch
  (app bar, every page, sticky, persisted); a State Patterns row for the
  default language and the `localStorage` fallback.
- `DESIGN.md`: Components gains the app bar and the segmented language switch.
- `freight-tenders/README.md`: one line that the UI is available in German
  (default) and English, switchable on every page.

### Clarifications

- The mechanism must switch at runtime. Angular's build-time
  `@angular/localize` with one build per locale does not meet this story,
  since it needs a reload and a separate bundle per language. A small
  signal-based translation service with one dictionary per language, or a
  runtime library, is the implementer's choice; prefer no new dependency.
- Both dictionaries have exactly the same keys; a test fails when a key is
  missing in either language.
- `tender-format.ts`'s fixed `de-DE` locale is replaced by the active
  language's locale; the formatting functions keep their behavior for German.
- The backend's error and validation messages are not shown in the UI today
  and stay English; the frontend keeps showing its own messages, now in the
  active language.
- The language is a per-browser preference, not a user setting on the
  server; there are no user accounts.
- Text that is generated from several parts (e.g. "Ausschreibung 42 ·
  Offen") is built per language, not by translating fragments and
  concatenating them in German word order.
- No URL parameter or route prefix for the language; URLs stay as they are.

### Implementation choices

Anything this story does not specify -- class and method names, how the
dictionaries are structured and keyed, how components and styles are split,
test structure -- is the implementer's choice. Follow the conventions in
`freight-tenders/frontend/AGENTS.md` and prefer the simplest option; none of
it needs a decision from the story author.

## Why

The dispatchers work in German, so German stays the default and nothing
changes for them. But tenders go out to carriers across Europe and are
discussed with colleagues who do not read German; an English UI lets them
read a tender, its offers and its status without a translator. Keeping the
switch on every page and remembering the choice means the language is set
once, not hunted for on each screen.

## Acceptance

- Opening any route with an empty `localStorage` shows the UI in German,
  `<html lang="de">`, and the switch with "DE" pressed -- regardless of the
  browser's language.
- The switch is rendered on every route and in every page state (loading,
  load error, empty, loaded), including `/tenders/:id/print` and
  `/tenders/:id/edit` if those routes exist; on the print view it is hidden in
  print.
- The switch stays visible after scrolling to the bottom of a long detail
  page.
- Selecting "EN" on any page shows that page's headings, labels, buttons,
  table headers, status labels, hints, empty states and messages in English,
  sets `<html lang="en">` and the English tab title, presses "EN", and sends
  no HTTP request; selecting "DE" switches back.
- Switching language while a form has input and validation errors keeps the
  input and shows the validation messages in the new language.
- Switching language keeps the current route and the current table sorting.
- After selecting "EN", reloading the page, opening a URL directly and opening
  the print view in a new tab all show English; `localStorage` holds
  `freight-tenders.language` = `en`.
- An unknown stored value, or `localStorage` throwing, results in German
  without an error.
- Dates, numbers, loading meters, amounts and temperature ranges are formatted
  as in the formats table for each language.
- User-entered data (route places, commodity, remarks, supplier names, offer
  notes) is shown unchanged in both languages.
- The switch buttons carry `aria-pressed`, `lang` and an accessible name, and
  the group has an accessible name in the active language.
- No UI text is hardcoded in a template or component outside the
  translation dictionaries; both dictionaries have the same keys, enforced by
  a test.
- Existing `data-testid` values are kept; assertions go through `data-testid`.
- `freight-tenders/frontend/AGENTS.md`, `EXPERIENCE.md`, `DESIGN.md` and
  `freight-tenders/README.md` are updated as described.
- Existing frontend tests keep passing or are updated to run in German (the
  default); the new behavior has test coverage; `npm run lint`,
  `npm run build` and `npm test -- --watch=false` pass.
