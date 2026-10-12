# Close a tender from its detail page

## Problem

A tender can only be closed by calling `POST /api/tenders/{id}/close` directly --
the Angular frontend has no way to do it. `freight-tenders/README.md` says so
itself ("Closing a tender has no UI; call the API directly"). A dispatcher who
has accepted an offer has to leave the app to finish the job, and the
closed-tender state the detail page already knows how to show (grey
"Geschlossen" pill, disabled add-forms, explanation line) can only be reached by
`curl`.

## What to build

On the tender detail page (`/tenders/:id`), an open tender gets a
"Ausschreibung schließen" action.

- Selecting it calls the existing close endpoint through `TenderApiService`
  (add a `close(id)` method there; components never use `HttpClient` directly).
- On success the page switches to the closed state without a reload or
  navigation: the status pill reads "Geschlossen", both add-forms are disabled,
  and the existing closed-tender explanation appears above them. The action
  itself disappears.
- While the request is in flight the action is disabled, so it cannot be sent
  twice.
- If the request fails, a German error message appears next to the action and
  the tender stays open and fully usable.
- A tender that is already closed when the page loads never shows the action.

The action is a secondary (outlined) button: the detail page's one filled
Ford-blue button stays "Angebot hinzufügen"
(`_bmad-output/initiative-demo-app/ux-freight-tenders-ui/DESIGN.md`). There is
no confirmation dialog -- the app has no modals
(`_bmad-output/initiative-demo-app/ux-freight-tenders-ui/EXPERIENCE.md`).

The backend endpoint already exists and returns the closed tender; no backend
behavior changes. Update `freight-tenders/README.md` so it no longer says
closing is API-only.

## Why

Closing is the other half of the app's one real business rule -- remarks and
offers can only be added while a tender is open -- and it is the only step of
the tender lifecycle the UI cannot perform.

## Acceptance

- On an open tender's detail page, selecting "Ausschreibung schließen" closes
  the tender: the pill shows "Geschlossen", both add-forms are disabled with the
  existing explanation, and the action is gone -- all without a page reload.
- Back on the overview, that tender is listed under "Geschlossene
  Ausschreibungen".
- A closed tender's detail page shows no close action.
- A failed close request shows a German error message and leaves the tender
  open, with its add-forms still enabled.
- All new UI text is German; assertions go through `data-testid`.
- Existing frontend and backend tests keep passing; the new behavior has test
  coverage, and `npm run lint`/`npm run build` pass.
