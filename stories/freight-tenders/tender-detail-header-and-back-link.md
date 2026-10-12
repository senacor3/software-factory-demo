# Give the tender detail page a back link and a clear header

## Problem

The tender detail page (`/tenders/:id`) is a dead end. Nothing on it leads back
to the overview: a dispatcher who has finished with a tender has to use the
browser's back button or edit the URL, and on a failed load ("Die Ausschreibung
wurde nicht gefunden...") there is no way out of the page at all. The create
page has "Abbrechen"; the detail page has nothing.

The top of the page is also loosely composed. Three things are stacked on three
separate rows -- the route title, the status pill under it, and the
"Ausschreibung schließen" button under that -- so the page's most important
fact (is this tender open?) and its only page-level action sit in a column of
unrelated-looking elements, and the button dangles between the header and the
first section. When the tender is closed the button's row vanishes and
everything below it jumps up.

## What to build

A frontend-only change to the detail page's top area: add a back link, and
compose title, status and close action into one header row. No backend change,
no new route, and no change to the remarks/offers sections below the header.

### Layout

Open tender, desktop:

```
← Zurück zur Übersicht

Hamburg → Rotterdam  ( Offen )                  [ Ausschreibung schließen ]

Bemerkungen
...
```

Closed tender, desktop -- the pill has not moved, only the action is gone:

```
← Zurück zur Übersicht

Hamburg → Rotterdam  ( Geschlossen )

┌──────────────────────────────────────────────────────────────────────────┐
│ Diese Ausschreibung ist geschlossen, daher können keine weiteren ...     │
└──────────────────────────────────────────────────────────────────────────┘

Bemerkungen
...
```

Loading and load-error -- the back link is the only thing above the message:

```
← Zurück zur Übersicht

          Die Ausschreibung wurde nicht gefunden oder konnte nicht
                            geladen werden.
```

At 600px and narrower (the existing breakpoint) the header stacks: title and
pill first, the close button on its own row below them, left-aligned.

### Back link

- Text "Zurück zur Übersicht", preceded by a "←" that is decorative
  (`aria-hidden="true"`). A real `<a routerLink="/">`, `data-testid="back-link"`.
- It is the first element inside `<main>` and is rendered in **every** state of
  the page: loading, load error, open tender, closed tender. It is therefore
  the first stop in the tab order.
- It is a quiet text link, not a button: `{typography.label}` (13px/600),
  `{colors.on-surface-variant}` at rest, `{colors.on-surface}` plus underline on
  hover, and the same 2px `{colors.primary}` focus ring the buttons use. It is
  never blue -- Ford Blue stays reserved for the primary action
  (`_bmad-output/initiative-demo-app/ux-freight-tenders-ui/DESIGN.md`, Do's and
  Don'ts). Give it enough vertical padding for a pointer target at least 24px
  high.
- `2 × {spacing.unit}` (16px) separates it from the header row.
- Its style is a shared class in `src/styles.scss` next to the other shared
  components, not page-local SCSS.

### Header row

One row, `<header class="page-header">`, with two groups:

- **Left: title and status together.** The `<h1>` route title, then the status
  pill immediately after it on the same line, vertically centred on the title,
  with `2 × {spacing.unit}` (16px) between them. The pill is the same
  `status-pill-open`/`status-pill-closed` component the overview uses -- same
  size, same colors, same "Offen"/"Geschlossen" labels -- so status reads
  identically on both pages. The status pill no longer sits on its own row
  under the title.
- **Right: the page-level action.** "Ausschreibung schließen" is pushed to the
  right end of the row, aligned with the title. It keeps its label, its
  `btn-secondary` (outlined) style and its standard button size: the page's one
  filled Ford-blue button stays "Angebot hinzufügen".

A long route title wraps inside the left group; the pill stays attached to the
title and the button never shrinks or wraps its label.

Because the pill belongs to the title group and not to the action, it stays in
exactly the same place when the tender is closed and the button disappears.
Nothing in the header moves except the button leaving.

`{spacing.gutter}` (24px) separates the header row from whatever follows it --
the closed explanation for a closed tender, otherwise the first section's own
`{spacing.section-gap}`.

### Close action behavior

Unchanged from today, restated so the new layout is unambiguous:

- Shown only while the tender is open. Disabled while the close request is in
  flight; the label does not change and the row does not shift.
- A failed close shows the existing German error message
  (`data-testid="close-error"`) directly below the header row, aligned under
  the button (right-aligned on desktop, left-aligned at 600px and narrower),
  with `role="alert"` so it is announced. The tender stays open and usable.
- Still no confirmation step -- the app has no modals
  (`_bmad-output/initiative-demo-app/ux-freight-tenders-ui/EXPERIENCE.md`).

One addition: today a successful close removes the focused button from the
page, so a keyboard user's focus falls back to the document. After a successful
close, focus moves to the closed-tender explanation line
(`data-testid="closed-explanation"`, made programmatically focusable with
`tabindex="-1"`). That line states what just happened and sits immediately
before the now-disabled forms, so it is the right place to resume from.

### Documentation

- `EXPERIENCE.md`: the Information Architecture table's "Reached from" for the
  overview gains the detail page's back link; Component Patterns gains a "Back
  link" row and the "Status pill" row says the detail-page pill sits beside the
  title; State Patterns → "Closed tender" notes that focus moves to the
  explanation line after an in-page close.
- `DESIGN.md`: Components gains the back link's visual spec as written above.
- `freight-tenders/README.md`: the `/tenders/:id` row of the route table
  mentions the link back to the overview.

## Why

The detail page is where a dispatcher spends the most time and it is the one
page they cannot leave from within the app. Grouping status with the title and
the page action opposite it makes the header answer "which tender, in what
state, and what can I do with it" in a single glance, and keeps that answer in
the same place whether the tender is open or closed.

## Acceptance

- The detail page shows a "Zurück zur Übersicht" link as the first element of
  the page in all four states (loading, load error, open, closed); selecting it
  navigates to `/`.
- The back link is a real anchor, reachable by Tab before anything else on the
  page, and is not styled as a button or in Ford Blue.
- For a loaded tender, the header contains -- in this DOM order -- the route
  title, the status pill, and (only while open) the close button. The status
  pill is no longer rendered on a row of its own below the title.
- Closing a tender from the page changes the pill to "Geschlossen" in place,
  removes the close button, shows the closed explanation, and moves keyboard
  focus to that explanation line.
- A failed close shows the existing German error with `role="alert"`, and the
  tender stays open with its add-forms enabled.
- At 600px and narrower the close button sits below the title and pill rather
  than beside them, with no horizontal scrolling.
- Existing `data-testid` values (`page-title`, `status`, `close-tender`,
  `close-error`, `closed-explanation`) are kept; `status` still contains exactly
  the German label and nothing else.
- All new UI text is German; assertions go through `data-testid`.
- `EXPERIENCE.md`, `DESIGN.md` and `freight-tenders/README.md` are updated as
  described.
- Existing frontend tests keep passing; the new behavior has test coverage, and
  `npm run lint`/`npm run build` pass.
