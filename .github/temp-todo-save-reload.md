# Task: Save-triggered preview reload
Generated: 2026-03-24

## Tasks
[updated] Add save button wiring with tooltip matching theme
[updated] Trigger save and preview refresh only on button click or Ctrl+S
[updated] Remove auto-regeneration on every keystroke

## Progress Notes
- Created task tracker
- Wired save button + tooltip, hooked to manual save flow
- Added Ctrl+S hotkey and removed auto debounce regeneration
- Relocated Save button into layout toolbar per UI request
- Adjusted toolbar layout so Save sits on the right side of the same bar
- Enabled built-in Monaco quick suggestions (no external LSP) for faster intellisense feel
- Switched backend Markdown parsing to markdown-it-py and mapped blocks (headings, lists, code, hr) to ReportLab flowables
- Rebuilt pdf_generator to remove corrupted duplicate imports and restore PDF rendering
- Made Markdown parser resilient when optional sub/sup plugins are missing and fixed link href extraction to avoid invalid anchors
- Fixed unordered list bullet handling to avoid ReportLab int decode errors when lists contain blank items
