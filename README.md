# polkaspots.com

Static site, generated. No client-side framework, no runtime dependencies.

```
python3 tools/build.py      # rebuild everything
```

The deploy workflow runs the build and **fails if a fresh build differs from what is
committed**, so generated output can never drift from source. Always commit the build.

## Layout

| Path | What it is |
|---|---|
| `tools/engine.py` | Templates, chrome, analytics, sitemap/robots/llms/RSS writers, shared constants |
| `tools/build.py` | Page content and the blog loop |
| `content/posts/<section>/*.md` | Blog posts, frontmatter + markdown |
| `functions/api/submit.js` | Cloudflare Pages Function handling form delivery |
| `style.css` | Hand-written, no preprocessor |
| `DOMAIN.md` | Why ForgeCRA is on this domain and what would move it |

Generated and committed: `index.html`, every `*/index.html`, `sitemap.xml`, `robots.txt`,
`llms.txt`, `llms-full.txt`, both `feed.xml`. Do not hand-edit them — edit the source and rebuild.

## Form delivery

Forms POST JSON to `/api/submit`, which fans out to every destination configured as a Pages
environment variable and succeeds if any of them does:

| Variable | Effect |
|---|---|
| `FORM_WEBHOOK` | POSTs to a webhook. Payload carries a Slack-shaped `text` plus flat fields. |
| `RESEND_API_KEY` | Emails via Resend. `reply_to` is set to the submitter. |
| `FORM_TO` / `FORM_FROM` | Override the email addresses. |

If every destination fails, the browser falls back to the form's `mailto:` action, so a
submission cannot be silently lost. `GET /api/submit` reports which destinations are visible
(booleans only, never values).

**Pages binds environment variables when a deployment is created.** Adding a variable does
nothing until you redeploy.

## Analytics

Plausible, cookieless, no consent banner. Goals fire from explicit `plausible()` calls rather
than the dashboard's tagged-events feature, so they work without any dashboard configuration.

Every tracked element fires **two** events: a rollup and a specific one.

| Rollup | Specific | Fired by |
|---|---|---|
| `cta_click` | `cta_sup_hero`, `cta_sup_offer` | In-page CTAs |
| `call_booked` | `book_mfr_hero`, `book_mfr_offer`, `book_sup_offer`, `book_router`, `book_pen`, `book_contact` | Cal.com CTAs |
| `outbound_cal` | — | Any click to `cal.com`, fired alongside the above |
| `form_submit` | — | Any form submit attempt |
| `form_submit_ok` | `form_ok_mfr`, `form_ok_sup`, `form_ok_contact` | Delivery confirmed |
| `form_submit_fail` | `form_fail_mfr`, `form_fail_sup`, `form_fail_contact` | Delivery failed, mailto fallback used |

To add tracking: put `data-goal="<rollup>"` and `data-goal-detail="<specific>"` on the element.
Forms additionally need `data-form="<slug>"`.

Create goals in Plausible only for the ones you want to read; unmatched events are ignored.

## UTM convention

One scheme, used on every outbound link so campaigns are attributable. Lower case, no spaces.

```
?utm_source=<where>&utm_medium=<how>&utm_campaign=<what>&utm_content=<variant>
```

| Parameter | Values | Notes |
|---|---|---|
| `utm_source` | `linkedin`, `google`, `bing`, `outbound`, `newsletter`, `partner` | The platform, not the audience |
| `utm_medium` | `cpc`, `email`, `social`, `referral` | Paid is always `cpc` |
| `utm_campaign` | `cra-mfr`, `cra-sup`, `flash`, `pentest` | Audience and product, not the date |
| `utm_content` | free, e.g. `hero-a`, `hero-b`, `subject-1` | The A/B variant only |

Examples:

```
https://polkaspots.com/cra-sbom-attestation/for-manufacturers/?utm_source=linkedin&utm_medium=cpc&utm_campaign=cra-mfr&utm_content=hero-a
https://polkaspots.com/cra-sbom-attestation/for-suppliers/?utm_source=outbound&utm_medium=email&utm_campaign=cra-sup&utm_content=subject-1
https://polkaspots.com/security-due-diligence/?utm_source=google&utm_medium=cpc&utm_campaign=pentest&utm_content=due-diligence
```

Rules that keep the data usable:

- **Never tag internal links.** It restarts the session and destroys the referrer.
- **`utm_campaign` names the audience, never the month.** `cra-sup` stays `cra-sup` forever;
  use `utm_content` for anything that varies per run.
- **Supplier traffic is scarce — always tag it.** Page B conversion is the metric the Phase 0
  kill/proceed decision turns on, and untagged supplier traffic is unattributable and therefore
  worthless for that decision.
