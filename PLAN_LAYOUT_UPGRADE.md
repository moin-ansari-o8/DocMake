# Layout + PDF System Upgrade

This document captures the implementation plan to harden markdown-to-PDF rendering, add robust theming/templates, and support user-customizable layouts (including assets and multi-column support).

## Goals
- Zero-crash parsing/rendering for messy markdown (blank list items, missing plugins, invalid links).
- Schema-driven layouts with defaults plus user clones; immutable defaults remain intact.
- Support headers/footers, top/bottom bars, backgrounds, logos, and two-column layouts.
- Safe asset handling (uploads, validation, sandboxed paths).
- Regression tests to keep the pipeline stable.

## Current Pain Points
- Renderer crashes on malformed lists or missing link schemes.
- Layouts limited to margins/fonts/colors; no header/footer/background controls.
- No validation on layout JSON or asset references.
- No automated tests for parser+PDF pipeline.

## Layout Schema (draft)
Use pydantic to validate on create/update. Example payload (user layouts):

```json
{
  "id": "user-abc123",
  "name": "My Layout",
  "description": "Custom copy of academic",
  "version": 1,
  "base": "academic",             // optional: cloned from a default
  "config": {
    "margins": {"left": 14, "right": 14, "top": 18, "bottom": 18},
    "fonts": {
      "body": {"name": "Helvetica", "size": 11},
      "heading": {"name": "Helvetica-Bold", "size": 14},
      "code": {"name": "Courier", "size": 9.5}
    },
    "colors": {"body": "#222222", "heading": "#111111", "border": "#9ca3af"},
    "palette": {"primary": "#111111", "muted": "#4b5563", "surface": "#ffffff"},
    "title": {"align": "center", "color": "#111111"},
    "subtitle": {"align": "center", "color": "#4b5563"},
    "body": {
      "paragraph": {"space_after": 6},
      "list": {"indent": 10, "item_spacing": 2, "bullet": "disc"},
      "code": {"padding": 6, "bg": "#f3f4f6", "border": "#e5e7eb"},
      "hr": {"thickness": 1, "color": "#9ca3af"},
      "layout": {"columns": 1, "gutter": 12}
    },
    "header": {
      "height": 24,
      "padding": 6,
      "text": "",
      "logo": "assets/user123/logo.png",
      "align": "center",
      "color": "#111111"
    },
    "footer": {
      "height": 24,
      "padding": 6,
      "text": "",
      "logo": "",
      "align": "center",
      "color": "#4b5563"
    },
    "bars": {
      "top": {"height": 6, "color": "#111111"},
      "bottom": {"height": 6, "color": "#9ca3af"}
    },
    "background": {
      "color": "#ffffff",
      "image": "assets/user123/bg.jpg",
      "mode": "cover"   // cover|contain|tile
    }
  }
}
```

## API Surface (planned)
- `GET /api/layouts` list defaults + user layouts (defaults flagged immutable).
- `POST /api/layouts/clone` with `source_id` (default) -> returns editable user copy.
- `POST /api/layouts` create user layout (validated by schema).
- `PUT /api/layouts/{id}` update user layout (defaults rejected).
- `DELETE /api/layouts/{id}` delete user layout (not allowed for defaults).
- `POST /api/assets/upload` (logo/background), validates mime, extension, size, and stores under assets/{user}/.
- `POST /api/pdf/preflight` returns parsed blocks + validation result (no PDF build) for debugging.
- `POST /api/pdf/generate` unchanged contract, but now uses validated layout and hardened pipeline.

## Parser Hardening
- Trim/drop empty list items; normalize whitespace.
- Safe links: require scheme; otherwise render as plain text.
- Optional rules (sub/sup) enabled best-effort; never crash if absent.
- Unknown tokens -> paragraph fallback.
- Preflight validator to surface issues before render.

## Renderer Hardening
- Lists: only ordered lists set numeric `value`; unordered bullets configured with bullet font/size; spacing/indent from layout.
- Paragraph/list spacing configurable; code blocks get padding/background/border from layout.
- HR styling (color/thickness/inset) from layout.
- Defensive try/except around `doc.build` to return structured error payloads.
- Two-column support: use BaseDocTemplate with two frames and page templates; single-column default.

## Assets & Safety
- Asset upload endpoint: whitelist extensions (png/jpg/svg for logos; png/jpg for backgrounds), size cap, mime sniffing.
- Store under a dedicated assets root per user/tenant; reject paths escaping the root.
- On layout save, verify asset existence and allowed path; reject invalid references.

## Headers/Footers/Bars/Backgrounds
- Render header/footer per page template using configured height/padding/text/logo.
- Bars: draw rectangles at top/bottom with configured colors/heights.
- Background: solid color fill; optional image drawn with cover/contain/tile mode.

## Defaults and Versioning
- Keep three default layouts immutable; expose "clone default" for user edits.
- Add `version` to layout; on schema changes, migrate or reject with guidance.

## Testing Plan
- Unit tests for parser+generator on fixtures: blank list items, mixed ordered/unordered, links with/without scheme, code blocks, hr, two-column, header/footer/logo, background.
- Layout schema validation tests (pydantic).
- Smoke test: iterate defaults and a sample user layout, run parse+generate, assert build succeeds.
- Consider a fast integration test that hits `/api/pdf/preflight` and `/api/pdf/generate` with canned markdown.

## Migration Steps
1) Implement layout schema (pydantic) and validation in create/update endpoints.
2) Add assets upload endpoint with safe storage and reference checks.
3) Extend generator to consume new layout fields (header/footer/bars/background/columns).
4) Add parser/render hardening (list cleanup, link safety, guarded doc.build).
5) Add tests and preflight route.
6) Document cloning flow and immutability of defaults.

## Cherry on Top (optional nice-to-haves)
- Per-layout typography presets (line-height, letter-spacing for titles).
- Page numbering and date stamp options in footer.
- Small caps option for headings; pull-quote style for blockquotes.
- Theme tokens for code syntax colors (lightweight mapping, not full syntax highlighting).
- Caching fonts and backgrounds to reduce render time for repeated layouts.
- Webhook or event log entry on PDF generation errors with truncated markdown snippet for diagnostics.
