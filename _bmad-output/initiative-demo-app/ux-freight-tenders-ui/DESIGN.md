---
name: Freight Tenders Blue Oval
description: A confident, automotive-industrial look for the freight-tenders back-office app, inspired by ford.de's blue/black/white brand language.
status: final
updated: 2026-10-12
colors:
  primary: '#003478'
  primary-container: '#D6E2F0'
  on-primary: '#FFFFFF'
  on-primary-container: '#00264F'
  surface: '#FFFFFF'
  surface-dim: '#F2F2F2'
  surface-container: '#F7F8FA'
  surface-container-high: '#E9ECF1'
  on-surface: '#1A1A1A'
  on-surface-variant: '#4A4A4A'
  outline: '#C7CCD4'
  outline-variant: '#E0E3E8'
  status-open: '#1E7A34'
  status-open-container: '#E3F3E6'
  status-closed: '#6B6B6B'
  status-closed-container: '#EDEDED'
  error: '#B3261E'
  error-container: '#FBE9E7'
typography:
  display:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '700'
    lineHeight: '1.3'
  title:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.4'
  body:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.5'
  label:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0.02em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.4'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  full: 9999px
spacing:
  unit: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  section-gap: 40px
components:
  button-primary:
    background: '{colors.primary}'
    color: '{colors.on-primary}'
    radius: '{rounded.sm}'
    padding: '12px 24px'
  button-secondary:
    background: 'transparent'
    color: '{colors.primary}'
    border: '1px solid {colors.primary}'
    radius: '{rounded.sm}'
  table:
    headerBackground: '{colors.surface-container-high}'
    headerText: '{colors.on-surface}'
    rowBorder: '{colors.outline-variant}'
    rowHoverBackground: '{colors.surface-dim}'
    sortIndicatorColor: '{colors.primary}'
  status-pill-open:
    background: '{colors.status-open-container}'
    color: '{colors.status-open}'
    radius: '{rounded.full}'
  status-pill-closed:
    background: '{colors.status-closed-container}'
    color: '{colors.status-closed}'
    radius: '{rounded.full}'
---

## Brand & Style

**Confident Industrial.** The look of a company that moves heavy things on a schedule and wants you to trust the paperwork. Borrowed from ford.de: deep blue as the one color that carries authority, black/near-black for text, everything else neutral so data reads cleanly. No decoration for its own sake — a tender list is not a product showcase, so the "hero banner" energy of the automotive site translates here as bold section headings and a strong primary-action color, not large imagery.

Flat, not glossy. Sharp-but-softened corners (small radii, never pill-shaped except status badges). Generous whitespace between sections, tighter spacing inside working areas like tables and forms, so the app feels composed rather than cramped, without wasting space a back-office user needs for scanning rows quickly.

## Colors

- **Ford Blue (`{colors.primary}`)** is the one saturated color in the system — reserved for primary actions and active/selected states, for example an active sort column's indicator. It never appears as decoration.
- **Near-black (`{colors.on-surface}`)** carries all body text and headings — high contrast, no brand color used for text at small sizes.
- **Surfaces** (`{colors.surface}`, `{colors.surface-dim}`, `{colors.surface-container}`) stay white-to-light-grey; depth comes from one shade step, not shadows.
- **Status colors** are semantic, not decorative: `{colors.status-open}` (green) and `{colors.status-closed}` (grey) back the tender-status pill and are the *only* two colors besides blue allowed to carry meaning — never reused for anything else, so a user never has to wonder whether a color means status or something else.
- **Error (`{colors.error}`)** is reserved for form validation and failed-load messages — never for anything that isn't actually an error.

## Typography

Inter throughout — one typeface, weight and size carry the whole hierarchy, matching ford.de's single-sans-family discipline. `{typography.display}` is for a page's own title ("Neue Ausschreibung erstellen"); `{typography.headline}` for section headers ("Offene Ausschreibungen", "Bemerkungen"); `{typography.title}` for table column headers and form field groups; `{typography.body}` for everything a user reads as content; `{typography.label}` (tracked out slightly, all-caps optional) for form labels and table header cells; `{typography.caption}` for secondary/meta text (empty-state notes, helper text).

## Layout & Spacing

A single-column content area, max-width constrained on desktop (not full-bleed) so tables and forms don't stretch into unreadable widths — matches ford.de's centered content rhythm even though this app has no hero imagery. `{spacing.section-gap}` (40px) separates major page sections, for example the open-tenders table from the closed-tenders table; `{spacing.gutter}` (24px) is the standard internal padding for cards, table cells, and form groups. Desktop margins `{spacing.margin-desktop}` (48px); mobile `{spacing.margin-mobile}` (16px).

## Elevation & Depth

Flat by default. The only elevation is a 1px `{colors.outline-variant}` border delineating tables, cards, and form groups from the page background — no drop shadows. A hovered table row gets `{colors.surface-dim}` background, not a shadow lift.

## Shapes

Small, consistent corner radius (`{rounded.sm}`, 2px) on buttons, inputs, and table containers — sharp enough to feel industrial/technical, not so sharp it feels harsh. The one exception: status pills use `{rounded.full}` (fully rounded) so they're instantly recognizable as a status token, not a button.

## Components

- **Buttons:** `button-primary` is a solid Ford Blue fill with white text, used for exactly one primary action per view (copy owned by EXPERIENCE.md's Voice and Tone). `button-secondary` is an outlined blue-on-white button, used for any non-primary action. Disabled buttons drop to `{colors.outline}` fill/border with `{colors.on-surface-variant}` text — never just lowered opacity, which reads poorly at this palette's contrast.
- **Tables:** Header row uses `{components.table.headerBackground}` with `{typography.label}` column headers; each sortable header shows a small triangle indicator (`{components.table.sortIndicatorColor}`) pointing up or down for the active sort, absent on unsorted columns. Rows separated by a 1px `{components.table.rowBorder}`, hover state `{components.table.rowHoverBackground}`. Numeric columns, for example offer amount, right-align; text columns left-align.
- **Status pill:** A small rounded badge — `status-pill-open` or `status-pill-closed` — using `{rounded.full}` and the status colors from above. Placement and copy rules live in EXPERIENCE.md's Component Patterns.
- **Forms:** Label above input, `{typography.label}` style. Input border `{colors.outline}`, focus ring `{colors.primary}`. Error text in `{colors.error}`: directly below the specific field for a field-level validation error, or directly below the form (above its submit button) for a submission-level failure — see EXPERIENCE.md's State Patterns for which applies where. Never a top-of-form summary alone.
- **Empty/loading/error states:** `{typography.caption}` text, centered within the section it replaces (a table's body, a form's results area) — never a full-page takeover for a section-level state.

## Do's and Don'ts

- **Do** use Ford Blue for exactly the primary action on a view. **Don't** use it for anything else — not links, not decoration, not a second button.
- **Do** keep status color meaning fixed (green = open, grey = closed). **Don't** reuse green/grey for anything unrelated to tender status.
- **Do** right-align numeric table columns. **Don't** center them — centering makes columns of numbers hard to scan.
- **Do** show the sort indicator only on the active sort column. **Don't** show idle sort affordances on every header at once — it's visual noise on a page whose job is fast scanning.
- **Don't** add imagery, gradients, or shadows chasing the "automotive hero" look — the industry's visual confidence comes from typography, color discipline, and layout here, not photography.
