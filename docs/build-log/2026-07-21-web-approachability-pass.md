# 2026-07-21 — Web approachability pass (public web surfaces)

## What changed

Interface-only work on the public web app. No cell, ranking group, eligibility
constant, feed, or method rule changed; no claim changed strength. Everything
here is presentation, plus three defects found while verifying it.

### Defects fixed

Three faults in the design-system wiring were live, all of which
failed silently rather than erroring:

- `@theme` mapped `--font-display` to `var(--font-display)`, a self-reference
  that resolved to nothing, so the `font-display` utility emitted no rule.
- The type ramp was mapped under `--font-size-*`, but Tailwind v4's font-size
  namespace is `--text-*`. Every `text-display` heading, including the homepage
  `h1`, rendered at the inherited 16px instead of its intended 44-68px clamp.
- The theme toggle initialized to `dark` and wrote `data-theme` plus
  `localStorage` from a mount effect, so a first-time visitor on a light-mode OS
  was forced to dark and had that persisted before the correcting effect ran.
  It also read React state that had not re-rendered, so consecutive clicks never
  advanced past the first step.

### Presentation

- Type is now Geist with Geist Mono for evidence figures, replacing the
  Space Grotesk / IBM Plex pair.
- Theme is a three-way preference (system, light, dark) applied by a pre-paint
  inline script, so there is no flash and the OS stays authoritative until the
  user chooses. Theme flips are instant rather than cross-fading every surface.
- The hub led with all 28 capability cells as one undifferentiated grid. In
  the shipped view 21 are unavailable and none are active, so the first screen was a
  wall of dead ends. Coverage now leads with the cells that can answer a
  question today and collapses the rest behind one disclosure reading
  "N more kinds of work, not ranked yet".
- Copy moved from insider vocabulary to plain language across the hub, decision
  workspace, coverage, and leaderboard header. Status `Unavailable` reads
  "Not ranked yet"; the objective choices read "Best at the job" and
  "Cheapest of the best".
- Detail that a careful reader still needs moved into an info tip built on the
  native popover API rather than being deleted. The unavailable-is-not-dead
  disclosure, the ranking-group comparability rule, and the binding-and-
  abstention mechanism all live there.
- The leaderboard header no longer prints the raw `cell_id`.
- Scroll reveal is CSS-only (`animation-timeline: view()`), gated behind
  `prefers-reduced-motion`, with content visible by default. The unused `motion`
  package was removed.

## Catalog-breadth policy

Nothing was deleted from the catalog to make the page look better. All 28 cells
stay rendered with their real status, and the disclosure states plainly that
EvalRank understands these questions but lacks the independent evidence to rank
them. Honest abstention and catalog breadth are both preserved; only the
ordering changed, so the first screen leads with what is actually answerable.

## Verification

- 367/368 unit tests pass. The one failure,
  `__tests__/lib/contract-deploy-artifact.test.ts`, fails identically on `main`
  and is untouched contract-materialization work.
- 36/36 Playwright tests pass against a production build, including all 18 axe
  scans across light, dark, and RTL, with zero violations.
- Contrast measured from rendered pixels in both themes. One pair
  (`text-tertiary` on `surface-sunken`) came to 4.47:1, just under AA, and was
  moved to `text-secondary`; all remaining pairs pass (light 5.18-13.43,
  dark 6.45-17).
- Two faults were found and fixed by that verification rather than by review: an
  info tip nested inside a heading was absorbed into the heading's accessible
  name, and the a11y helper awaited every animation's `finished` promise, which
  a scroll-driven `ViewTimeline` never resolves.

## Provenance

- Public EvalRank: this commit.
- Runtime persistence and hosted operation are maintained in a separate private
  system; the paired private-side change is recorded there.
