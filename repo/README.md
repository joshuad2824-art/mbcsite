# Memorial Baptist Church — Website

Static site for Memorial Baptist Church (2800 S. Yale Ave., Tulsa, OK 74114).
No build step, no server, no dependencies to install. Every file here is deployable as-is.

## What's in here

| Path | What it is |
| --- | --- |
| `index.html` | The full website — ten screens (Home, I'm New, About & Beliefs, Our Team, Sermons, Events, Connect, Ministries, Giving, Member Hub). Self-contained: images and code are inlined, so it works offline. |
| `brand-guide.html` | The brand guide — logo usage, color palette, typography, signage and social templates. Also self-contained. |
| `assets/` | Original logo files (mark and primary lockup) at full resolution. |
| `source/` | Editable source of both pages. See "Editing the design" below. |
| `netlify.toml` | Netlify deploy config — no build command, publish from the repo root. |

## Put it online — Netlify

This repo is configured for Netlify (`netlify.toml`). There is no build step.

1. Push this folder to `github.com/joshuad2824-art/mbcsite` (branch `main`).
2. In Netlify: **Add new site → Import an existing project → GitHub → mbcsite**.
3. Leave the settings as Netlify proposes them — build command empty, publish directory `.` (`netlify.toml` already says so). Click **Deploy**.
4. Every push to `main` redeploys automatically. Pull requests get their own preview URL.

The site goes live at a `*.netlify.app` address immediately; rename it under **Site configuration → Site details**.

### Custom domain
**Domain management → Add a domain**, enter the domain, and follow Netlify's DNS instructions (either point the registrar's nameservers at Netlify DNS, or add the CNAME/A records Netlify shows). HTTPS is issued automatically once DNS resolves.

Before pointing the church's live domain at it, deploy to the `*.netlify.app` URL first and review every page there.

### GitHub Pages instead
A workflow is included at `.github/workflows/deploy.yml` if you ever want Pages: enable **Settings → Pages → Source: GitHub Actions**. It is inert until you do — safe to delete if you stay on Netlify.

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

After changing a source file, regenerate the deployed page by inlining it into a single file (the versions at the repo root are generated this way). Until that regeneration happens, `index.html` and the source can drift — treat `index.html` as the published artifact.

## Content still to replace

- Sermon titles, dates, and series art are placeholders.
- Event details and dates are placeholders.
- Staff bios are short drafts.
- Every striped panel is a photo slot awaiting real photography (foyer, congregation singing, pastor preaching, staff portraits at 4:5, ministry photos at 3:2, event images at 16:9).

## Brand quick reference

- **Colors:** Lamplight terracotta `#A8613F`, Yale Sage `#4F7A5A`, Bark `#3A322B`, Cream `#F8F3EB`, Parchment `#FFFDF9`, Rule `#E7DCC9`
- **Type:** Lora (headings, serif) + Lato (body, sans) — both from Google Fonts
- **Signature device:** the arch crop on photography, taken from the steeple in the church mark

---

© 2026 Memorial Baptist Church. Logo and photography are the property of the church.
