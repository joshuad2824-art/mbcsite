# Source files

Authoring versions of the two pages. Each is a complete HTML document — open it in a browser to preview, edit it in any text editor.

- `Memorial Baptist Church.dc.html` — the website
- `MBC Brand Guide.dc.html` — the brand guide
- `support.js` — the runtime both files load; keep it in this folder
- `assets/` — logo files referenced by the sources

Structure of each file: markup first, then a `<script type="text/x-dc">` block holding a `class Component` with the page's data (staff list, sermons, events, ministries, beliefs) in its `renderVals()` method. Most content changes are one-line edits to those arrays.

The published files at the repo root are single-file bundles generated from these — edit here, then regenerate.
