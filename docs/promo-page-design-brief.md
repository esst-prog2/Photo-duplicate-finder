# Design brief: promo page, The Contact Sheet

Shaped with the Impeccable `shape` command on 2026-11-13. Content is fixed in `docs/promo-page.md`. Product context is in `PRODUCT.md`. No code is described here, only intent.

## 1. Job and audience
Classmates and the teacher arrive from a link or the repo with about a minute. Visitor mode: Persuade. They should understand what the tool does, how well it performs, and how to try it.

## 2. Outcome and proof
- The action: run `find-duplicates` on their own photos. The command is the primary call to action, set as selectable text.
- Proof comes from the approved copy. The headline keeps "about three quarters of the look-alikes, and every group it makes is right". The exact figures (414, 89, 41, 30, 14 families) appear in one scoped line about the one real-folder run.
- No count is promised for a reader's folder.

## 3. Selected direction: The Contact Sheet
The page is one proof sheet of a folder.
- Palette: film-strip black (`#0e0e0e`), pale lightbox ground (`#e9eef2`), grease-pencil red (`#d9342b`), amber edge print (`#f2a900`).
- Materials: 35mm film strip, grease pencil on glassine.
- A red loop means "the tool grouped this". Loops mark only real groups.
- The strip of frames is the page's one ruled axis. Frame numbers run through every section.
- Raises, each named for its donor:
  - one ruled axis governs the copy (Mesophotic Deep Dive);
  - every annotation names the measurement and the run it came from (Daylight Section);
  - thumbnails scale by whole steps only (Sixteen-Color Field);
  - the strip survives any crop at phone width (Polish Film Poster).
- Seed: seed:51f372693bf14ec8. Assigned by the roll, chosen by the user. Build path: code-led.

## 4. Scope and boundaries
One page in plain static HTML and CSS, no script. Desktop and phone widths. The approved copy stays as written. The page links to the spec, planning log and process log without reproducing them.

## 5. Anti-goals
- No SaaS row of feature cards.
- No photo-app skin where loops are decoration.
- No invented testimonials or customers.
- No promised counts for a reader's folder.

## 6. Layout and interaction (intent)
- First viewport: headline, then a full-width strip of frames with one loop around a twin pair, then the command as edge print.
- Below: the result, the proof, a limits sheet giving the full picture of performance, then "Try it".
- Phone: the strip becomes a vertical roll.
- No script. Group highlight on hover and focus may use CSS alone. Reduced motion shows the still page.

## 7. Constraints and decisions
Settled by the user:
- Frames use the author's benchmark photos. Not used: `p19` (a licence plate is legible).
- No script, so no copy button.

Still open:
- No screenshot of the Excel report exists. None appears unless one is made.
- Keep-rule wording: the copy says "largest file size, then larger resolution, then first by name"; README section 1 says resolution only breaks ties between equal sizes.
- Contrast: amber and red text on black must pass accessibility contrast.
- Hosting is undecided. The page loads photos from `../benchmark/data` and assumes the repo root is served.
