---
schema_version: 1
story_slug: tender-detail-header-and-back-link
stage: analysis
status: ready-for-review
updated: 2026-10-13T06:04:38Z
---

## Proposal

Frontend-only change to the tender detail page (freight-tenders/frontend/src/app/tender-detail/) plus shared styles and docs.

Template: add `<a class="back-link" routerLink="/" data-testid="back-link"><span aria-hidden="true">←</span> Zurück zur Übersicht</a>` as the first child of `<main>`, outside the loading/error/loaded `@if` chain, so it renders in every state. TenderDetail gains `RouterLink` in its `imports`. In the loaded branch, replace the separate header, pill and `.page-actions` blocks with one `<header class="page-header">` holding a left group (`<h1 data-testid="page-title">` followed by the status pill, with `data-testid="status"` unchanged) and, only while open, the `btn-secondary` close button on the right. The close error moves out of the removed `.page-actions` wrapper to directly below the header row, with `role="alert"` and `data-testid="close-error"`. It is right-aligned on desktop and left-aligned at 600px and narrower. The closed explanation gets `tabindex="-1"` and is exposed as a `viewChild`/template ref.

Styles: in `src/styles.scss`, add a shared `.back-link` class next to the other shared components. It uses 13px/600 text, `--color-on-surface-variant` at rest, `--color-on-surface` plus underline on hover, the 2px primary focus ring (added to the existing focus-visible selector list), vertical padding for a pointer target of at least 24px, and 16px below it. Replace the obsolete "pill directly under the title" `.page-header h1` rule with a flex row (`justify-content: space-between`, `align-items: center`, `gap`). The title group is `display: flex; align-items: center; gap: 16px; flex-wrap: wrap` with the h1 margin reset. The button gets `flex-shrink: 0; white-space: nowrap`. Add 24px below the header, which the `.notice` margin already provides. Inside the existing `@media (max-width: 600px)` block, make the header wrap or stack with the button on its own left-aligned row. Delete the now-unused `tender-detail.scss` `.page-actions` rule, or reduce it to the close-error alignment.

Focus: after a successful close in `onClose()`, move focus to the closed-explanation element. The element only exists after change detection, so use a `viewChild` ElementRef plus an `afterNextRender` call or a microtask after the `tender.update`, then call `.focus()`.

Docs: update EXPERIENCE.md (IA "Reached from", Component Patterns "Back link" row and "Status pill" row, State Patterns "Closed tender" focus note), DESIGN.md (Components: back link spec), and the `/tenders/:id` row of the README route table.

Note: the story calls the pill classes `status-pill-open`/`status-pill-closed`, but the code and overview use `pill-open`/`pill-closed`. Keep the existing classes, since the intent is to reuse the same component.

## Subtasks

- Add RouterLink to TenderDetail imports and render the back-link anchor (aria-hidden arrow, data-testid=back-link) as the first element in <main>, outside the loading/error/loaded branches
- Restructure the loaded-state template into a single <header class="page-header"> with a title+pill group and, only while open, the close button; keep data-testids page-title, status, close-tender
- Move the close-error paragraph directly below the header row with role="alert" and data-testid=close-error; remove the .page-actions wrapper
- Add tabindex="-1" to the closed-explanation element and focus it after a successful close in onClose() (viewChild + afterNextRender or equivalent)
- Add the shared .back-link class to styles.scss (typography, colors, hover underline, focus ring, 24px+ target, 16px spacing) and include it in the focus-visible rule
- Replace the .page-header h1 rule in styles.scss with the flex header layout, no-shrink/no-wrap button, and 600px stacking with left-aligned button and close error
- Remove or trim the obsolete .page-actions rule in tender-detail.scss and keep close-error alignment styles
- Update EXPERIENCE.md, DESIGN.md and freight-tenders/README.md as described in the story
- Add and adjust Vitest tests in tender-detail.spec.ts, then run npm test -- --watch=false, npm run lint, npm run static-analysis and npm run build

## Tests

- Back link is present with href "/" and the text 'Zurück zur Übersicht' in the loading state (before the HTTP response is flushed)
- Back link is present in the load-error state (detail request fails with 404) and in the invalid-id state
- Back link is present for an open tender and for a closed tender, and is the first element in main in each state
- Clicking the back link navigates to '/' (Router URL assertion using provideRouter routes)
- Open tender: the header contains page-title, status and close-tender in that DOM order, and the status text is exactly 'Offen'
- Closed tender: the header contains page-title and status 'Geschlossen', there is no close-tender button, and closed-explanation is shown
- Successful close: status becomes 'Geschlossen' in place, close-tender is removed, closed-explanation is shown and document.activeElement is the closed-explanation element
- Failed close (500): close-error shows the German message with role="alert", the tender stays open, and the remark and offer forms stay enabled
- Close button is disabled while the close request is in flight and its label is unchanged
- The existing detail, overview, create and app specs still pass; npm run lint, static-analysis and build succeed
