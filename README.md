# Memorial Baptist Church — Website

Static site for Memorial Baptist Church (2800 S. Yale Ave., Tulsa, OK 74114).
No build step, no server, no dependencies to install. Every file here is deployable as-is.

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | The full website — ten screens (Home, I'm New, About & Beliefs, Our Team, Sermons, Events, Connect, Ministries, Giving, Member Hub). Self-contained: images, fonts, and code are inlined, so it works offline. |
| `brand-guide.html` | The brand guide — logo usage, color palette, typography, signage and social templates. Also self-contained, and marked `noindex` so it never outranks the site itself. |
| `assets/` | Logo files at full resolution, plus the generated favicons and social card. |
| `source/` | Editable source of both pages. See "Editing the design" below. |
| `tools/` | Helper scripts. See "Regenerating brand assets". |
| `netlify.toml` | Netlify deploy config — no build command, publish from the repo root. |
| `robots.txt`, `site.webmanifest`, `favicon.ico` | Crawler rules, the PWA/home-screen manifest, and the root favicon. |

## Put it online — Netlify

This repo is configured for Netlify (`netlify.toml`). There is no build step.

1. Push to `github.com/joshuad2824-art/mbcsite` (branch `main`).
2. In Netlify: **Add new site → Import an existing project → GitHub → mbcsite**.
3. Leave the settings as Netlify proposes them — build command empty, publish directory `.` (`netlify.toml` already says so). Click **Deploy**.
4. Every push to `main` redeploys automatically. Pull requests get their own preview URL.

The site goes live at a `*.netlify.app` address immediately; rename it under **Site configuration → Site details**.

### Custom domain
**Domain management → Add a domain**, enter the domain, and follow Netlify's DNS instructions (either point the registrar's nameservers at Netlify DNS, or add the CNAME/A records Netlify shows). HTTPS is issued automatically once DNS resolves.

Before pointing the church's live domain at it, deploy to the `*.netlify.app` URL first and review every page there.

## Status: pre-launch

The site is live at **https://mbctulsa.netlify.app** for staff review. It is
deliberately **not indexable** yet — `netlify.toml` sets
`X-Robots-Tag: noindex, nofollow` on every path.

That is on purpose. The sermons, events, and staff bios are still
placeholders, and letting Google index placeholder text under the church's
name — competing with the current site at memorialbaptist.com — is a mess to
undo later. Link previews still work, so sharing the URL with staff shows the
proper card.

### Launch checklist

When the real content is in and the custom domain is ready:

1. Delete the `X-Robots-Tag` line from `netlify.toml` (it is marked
   `PRE-LAUNCH ONLY`).
2. Attach the custom domain in Netlify and set it as the **primary domain**,
   so the `*.netlify.app` address redirects to it instead of competing.
3. Add absolute `og:url` and `<link rel="canonical">` tags pointing at the
   real domain, in **both** heads of `index.html` (see "Editing the design"
   below for why there are two) and in the `<helmet>` of the matching source.
4. Add a `Sitemap:` line to `robots.txt`.
5. Redirect or retire the old site so the two do not compete in search.

Steps 3 and 4 are held until then on purpose: a canonical URL pointing at the
wrong host is worse for search than no canonical at all. `og:image` stays
relative, which every real scraper resolves against the page URL.

## Admin content editing

The site has a built-in editor so staff can change copy and photos without touching code.

1. Scroll to the very bottom of any page and click **Admin sign in**.
2. Passcode: `memorial2026`
3. An admin bar appears at the bottom. Choose a page, click **Edit page**, then:
   - click any text to rewrite it
   - click any photo (including the striped placeholders) to upload a replacement from your computer
4. Changes save automatically as you type.

**Important:** edits are stored in the browser they were made in — this is a static site with no database. To move a set of edits to another computer, or to make them permanent for all visitors, use **Export** in the admin bar to download `mbc-site-content.json`, then **Import** it on the target machine. Commit that JSON file here if you want a backup of the church's real copy.

To change the passcode, open `source/Memorial Baptist Church.dc.html`, search for `memorial2026`, and replace both occurrences (the check and the on-screen hint). Then re-export per below. This is a convenience lock, not real security — anything typed into a static page can be read by a determined visitor.

### Making edits permanent for everyone
Two options:
- **Simple:** make the edits in the browser, Export the JSON, and commit it — then a future developer can bake it into the page.
- **Proper:** put the content behind a small CMS or headless backend (Netlify CMS, Sanity, Airtable + a function). This requires a developer and a hosting plan that runs code.

## Editing the design

`source/` holds the authoring format for both pages — a single HTML file per page with the markup at the top and its logic class in the `<script type="text/x-dc">` block at the bottom. `support.js` is the small runtime both files load; it must sit next to them.

Open `source/Memorial Baptist Church.dc.html` directly in a browser to preview. Any text editor works; there is nothing to compile.

Most content changes are one-line edits to the arrays in `renderVals()` — `times`, `staff`, `allSermons`, `allEvents`, `allGroups`, `hubCards`.

> **Known gap:** there is no script in this repo that turns `source/` back into the bundled `index.html` / `brand-guide.html` at the root. Those bundles were produced by the Claude Design canvas exporter. Until that regeneration path exists, **`index.html` is the published artifact** and the two can drift. Edits made only in `source/` will not appear on the live site.

Page metadata (title, description, favicons, Open Graph tags) lives in the `<helmet>` block of each source file *and* in the generated bundles, so it survives a future regeneration either way.

## Regenerating brand assets

`favicon.ico` (repo root — the well-known path browsers probe) and `assets/apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `og-image.png` are generated:

```sh
pip install Pillow fonttools brotli
python3 tools/make-brand-assets.py
```

The script draws a simplified mark — a solid house silhouette with the cross knocked out, because the full line-art logo turns to mush below about 48px. Lora and Lato are recovered straight out of `index.html`'s bundle manifest, so no font files need tracking and there is no network call.

`assets/favicon.svg` is hand-maintained; keep it in sync with the `HOUSE`/`CROSS` coordinates in the script if the glyph changes.

## Content still to replace

- Sermon titles, dates, and series art are placeholders.
- Event details and dates are placeholders.
- Staff bios are short drafts.
- Every striped panel is a photo slot awaiting real photography (foyer, congregation singing, pastor preaching, staff portraits at 4:5, ministry photos at 3:2, event images at 16:9).
- There is no phone number anywhere on the site or in the structured data.

## Brand quick reference

- **Colors:** Lamplight terracotta `#A8613F`, Yale Sage `#4F7A5A`, Bark `#3A322B`, Cream `#F8F3EB`, Parchment `#FFFDF9`, Rule `#E7DCC9`
- **Type:** Lora (headings, serif) + Lato (body, sans) — both inlined into the bundles as woff2 subsets
- **Signature device:** the arch crop on photography, taken from the steeple in the church mark

---

© 2026 Memorial Baptist Church. Logo and photography are the property of the church.
