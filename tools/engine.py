#!/usr/bin/env python3
"""Static site engine for polkaspots.com (named engine.py: `site` is stdlib).

Zero runtime dependencies and no client-side JavaScript. Renders pages and
blog posts from content/, then emits sitemap.xml, RSS feeds, robots.txt and
llms.txt so search and agentic crawlers all see the same canonical facts.

Run: python3 tools/build.py   (the deploy workflow runs it before publishing)
"""
import html
import os
import pathlib
import re
import xml.sax.saxutils as sx
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ORIGIN = "https://polkaspots.com"
MAIL = "security@polkaspots.com"
COMPANY = "PolkaSpots Limited"
COMPANY_NO = "05508105"

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700"
         "&family=Geist:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap")

URLS = {
    "home":        "/",
    "flash":       "/flash-security-review/",
    "pen":         "/security-due-diligence/",
    # Keyword root: the paid-search terms are "CRA SBOM", "CRA supplier SBOM"
    # and "SBOM attestation" (Landing Page Spec §6). The brand has no search
    # volume yet, so it lives in the title and copy, not the path.
    "forgecra":    "/cra-sbom-attestation/",
    "makers":      "/cra-sbom-attestation/for-manufacturers/",
    "suppliers":   "/cra-sbom-attestation/for-suppliers/",
    "contact":     "/contact/",
    "sec_blog":    "/security-due-diligence/blog/",
    "cra_blog":    "/cra-sbom-attestation/blog/",
}

# --------------------------------------------------------------- analytics & booking
# Plausible is cookieless, so no consent wall is needed (Landing Page Spec §3).
# The account's own snippet: the site is identified by the script ID.
#
# Goals fire explicitly via plausible('name') rather than via the class-based
# "Tagged events" feature, because that feature has to be switched on in the
# dashboard and is silently inert until it is. Explicit calls work the moment
# the script loads. Booking CTAs open in a new tab so the event is not racing
# a same-tab navigation.
ANALYTICS = """
  <!-- Privacy-friendly analytics by Plausible -->
  <script async src="https://plausible.io/js/pa-DQ-Xa2vnEhrSCIogD_ro3.js"></script>
  <script>
    window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
    plausible.init()
    document.addEventListener('click',function(e){
      var el=e.target.closest('[data-goal]');
      if(el){plausible(el.getAttribute('data-goal'))}
    });
    document.addEventListener('submit',function(e){
      var f=e.target.closest('form[data-goal]');
      if(f){plausible(f.getAttribute('data-goal'))}
    },true);
  </script>"""

# Booking links. One 30-minute Cal.com event serves both sides for now. If the
# supplier conversation wants its own shorter slot, create a second event type
# and point CAL_20 at it — the supplier CTA copy is driven by CALL_MINS.
CAL_30 = "https://cal.com/simon-morley-np2it0/30min"
CAL_20 = "https://cal.com/simon-morley-np2it0/30min"
CALL_MINS = "30"

MAILTO_30 = ("mailto:security@polkaspots.com?subject=ForgeCRA%20pilot%20call%20%E2%80%94%20manufacturer"
             "&amp;body=Company%3A%20%0ARole%3A%20%0AApprox%20number%20of%20upstream%20suppliers%3A%20"
             "%0ABiggest%20supplier-evidence%20pain%3A%20%0A%0AA%20couple%20of%20times%20that%20suit"
             "%20for%20a%2030-minute%20call%3A%20%0A")
MAILTO_20 = ("mailto:security@polkaspots.com?subject=ForgeCRA%20supplier%20call"
             "&amp;body=Company%3A%20%0ARole%3A%20%0ANumber%20of%20manufacturer%20customers%3A%20"
             "%0ACurrent%20SBOM%20format%3A%20%0A%0AA%20couple%20of%20times%20that%20suit%20for%20a"
             "%2030-minute%20call%3A%20%0A")

# Fall back to the mailto if a calendar link is ever cleared, so no CTA is dead.
BOOK_30 = CAL_30 or MAILTO_30
BOOK_20 = CAL_20 or MAILTO_20

# A calendar can confirm a booking; a mailto cannot. Only claim call_booked
# when a real calendar is behind the CTA.
BOOK_GOAL = "call_booked" if CAL_30 else "cta_click"



# key, nav label — URLs come from URLS so the two can never drift apart
NAV = [
    ("home",      URLS["home"],     "Home"),
    ("flash",     URLS["flash"],    "Flash Review"),
    ("pen",       URLS["pen"],      "Pentesting"),
    ("forgecra",  URLS["forgecra"], "ForgeCRA"),
    ("contact",   URLS["contact"],  "Contact"),
]


# Registry filled by emit(); drives sitemap, llms.txt and the link audit.
PAGES = []

# Sitemap lastmod for pages that are not posts. Set by build.py from the
# newest post date. It must be derived from content, never from the clock:
# the deploy verifies a fresh build matches what was committed, so a
# date-dependent build would start failing the day after every commit.
DEFAULT_LASTMOD = None


# --------------------------------------------------------------- markdown
def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![*\w])\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    return t


def markdown(src):
    """Small, predictable subset: headings, paras, lists, quotes, fences, hr."""
    out, lines, i = [], src.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i])); i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue
        if re.match(r'^\s*(---|\*\*\*)\s*$', ln):
            out.append("<hr>"); i += 1; continue
        m = re.match(r'^(#{2,4})\s+(.*)$', ln)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{md_inline(m.group(2).strip())}</h{lvl}>"); i += 1; continue
        if re.match(r'^\s*[-*]\s+', ln):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*]\s+', lines[i]):
                items.append(md_inline(re.sub(r'^\s*[-*]\s+', '', lines[i]).strip())); i += 1
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>")
            continue
        if re.match(r'^\s*\d+\.\s+', ln):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append(md_inline(re.sub(r'^\s*\d+\.\s+', '', lines[i]).strip())); i += 1
            out.append("<ol>" + "".join(f"<li>{x}</li>" for x in items) + "</ol>")
            continue
        if ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(lines[i][2:].strip()); i += 1
            out.append("<blockquote><p>" + md_inline(" ".join(buf)) + "</p></blockquote>")
            continue
        if ln.strip() == "":
            i += 1; continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{2,4}\s|```|>\s|\s*[-*]\s|\s*\d+\.\s)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        out.append("<p>" + md_inline(" ".join(buf)) + "</p>")
    return "\n".join(out)


def frontmatter(path):
    import yaml
    raw = path.read_text()
    if not raw.startswith("---"):
        raise ValueError(f"{path}: missing frontmatter")
    _, fm, body = raw.split("---", 2)
    return yaml.safe_load(fm), body.strip()


def load_posts(section):
    """content/posts/<section>/*.md -> newest first, unlisted excluded."""
    d = CONTENT / "posts" / section
    posts = []
    if not d.exists():
        return posts
    for f in sorted(d.glob("*.md")):
        meta, body = frontmatter(f)
        if meta.get("unlisted"):
            continue
        meta["body"] = body
        meta["section"] = section
        meta["url"] = f"{URLS['sec_blog' if section == 'security' else 'cra_blog']}{meta['slug']}/"
        meta["date"] = str(meta["date"])
        posts.append(meta)
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


# --------------------------------------------------------------- chrome
def masthead(active):
    links = "\n".join(
        '        <a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if k == active else "", l)
        for k, u, l in NAV)
    return f"""
  <header class="masthead">
    <div class="masthead-inner">
      <a class="wordmark" href="/">
        <span class="dots" aria-hidden="true"><i></i><i></i><i class="v"></i><i></i></span>
        <span class="wordmark-text">POLKASPOTS</span>
      </a>
      <nav class="nav" aria-label="Primary">
{links}
      </nav>
    </div>
  </header>
"""


def footer(forgecra=False):
    extra = ""
    if forgecra:
        extra = (
            f'\n      <p>ForgeCRA is a product of PolkaSpots Ltd, est. 2005 — London. '
            f'Company number {COMPANY_NO}. <a href="mailto:{MAIL}">{MAIL}</a></p>'
            "\n      <p>No certification claims. We don't sell September-2026 panic — "
            "we build the evidence layer that outlasts it.</p>")
    return f"""
  <footer class="site-footer">
    <div class="footer-cols">
      <div class="footer-col">
        <h2>Security testing</h2>
        <div class="footer-links">
          <a href="{URLS['flash']}">Flash Review — £500</a>
          <a href="{URLS['pen']}">Penetration testing</a>
          <a href="{URLS['pen']}#remediation">Remediation</a>
          <a href="{URLS['pen']}#monitoring">Ongoing monitoring</a>
          <a href="{URLS['sec_blog']}">Security writing</a>
        </div>
      </div>
      <div class="footer-col">
        <h2>ForgeCRA</h2>
        <div class="footer-links">
          <a href="{URLS['forgecra']}">Overview</a>
          <a href="{URLS['makers']}">For manufacturers</a>
          <a href="{URLS['suppliers']}">For suppliers</a>
          <a href="{URLS['cra_blog']}">CRA writing</a>
        </div>
      </div>
      <div class="footer-col">
        <h2>Company</h2>
        <div class="footer-links">
          <a href="{URLS['contact']}">Contact</a>
          <a href="https://simonmorley.co.uk">Simon Morley</a>
        </div>
      </div>
      <div class="footer-col">
        <h2>Also building</h2>
        <div class="footer-links">
          <a href="https://nullrabbit.ai">NullRabbit</a>
          <a href="https://slashr.dev">Slashr</a>
          <a href="https://nrdax.com">NRDAX</a>
        </div>
      </div>
    </div>
    <div class="footer-base">
      <p>&copy; 2005&ndash;{(DEFAULT_LASTMOD or "2026")[:4]} {COMPANY}. Registered in England &amp; Wales, company number {COMPANY_NO}. London.</p>{extra}
    </div>
  </footer>
</body>
</html>
"""


def sec_head(label, num):
    return ('      <div class="section-head">\n'
            f'        <span class="section-label">{label}</span>\n'
            f'        <span class="section-num">{num}</span>\n'
            '      </div>')


# --------------------------------------------------------------- structured data
ORG = {
    "@type": "Organization",
    "@id": f"{ORIGIN}/#org",
    "name": "PolkaSpots",
    "legalName": COMPANY,
    "url": ORIGIN,
    "email": MAIL,
    "foundingDate": "2005",
    "areaServed": ["GB", "EU"],
    "address": {"@type": "PostalAddress", "addressLocality": "London", "addressCountry": "GB"},
    "identifier": {"@type": "PropertyValue", "name": "UK company number", "value": COMPANY_NO},
    "founder": {"@type": "Person", "name": "Simon Morley", "url": "https://simonmorley.co.uk"},
    "sameAs": ["https://simonmorley.co.uk", "https://nullrabbit.ai", "https://slashr.dev"],
}


def breadcrumbs(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": ORIGIN + u}
            for i, (n, u) in enumerate(trail, 1)
        ],
    }


def jsonld(*nodes):
    import json
    graph = [n for n in nodes if n]
    return ('  <script type="application/ld+json">\n'
            + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
            + "\n  </script>")


# --------------------------------------------------------------- emit
def emit(url, title, desc, body, active, *, ld=None, forgecra=False,
         extra_head="", changefreq="monthly", priority="0.7", lastmod=None,
         llms=None, noindex=False):
    """Write one page and register it for sitemap/llms.txt."""
    path = ROOT / (url.strip("/") + "/index.html" if url != "/" else "index.html")
    path.parent.mkdir(parents=True, exist_ok=True)
    robots = '\n  <meta name="robots" content="noindex, follow">' if noindex else \
             '\n  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">'
    doc = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{ORIGIN}{url}">{robots}

  <meta property="og:site_name" content="PolkaSpots">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{ORIGIN}{url}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_GB">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="/style.css">{ANALYTICS}{extra_head}
{ld or ''}
</head>
<body>""" + masthead(active) + body + footer(forgecra)
    path.write_text(doc)
    if not noindex:
        PAGES.append({"url": url, "title": title, "desc": desc,
                      "changefreq": changefreq, "priority": priority,
                      "lastmod": lastmod or DEFAULT_LASTMOD or "2026-08-18",
                      "llms": llms})
    return path


# --------------------------------------------------------------- generated artefacts
def write_sitemap():
    rows = "\n".join(
        f"  <url>\n    <loc>{ORIGIN}{p['url']}</loc>\n"
        f"    <lastmod>{p['lastmod']}</lastmod>\n"
        f"    <changefreq>{p['changefreq']}</changefreq>\n"
        f"    <priority>{p['priority']}</priority>\n  </url>"
        for p in sorted(PAGES, key=lambda x: (-float(x["priority"]), x["url"])))
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + "\n</urlset>\n")
    return len(PAGES)


AI_AGENTS = ["GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User",
             "Claude-SearchBot", "anthropic-ai", "Google-Extended", "Googlebot",
             "Bingbot", "PerplexityBot", "Perplexity-User", "CCBot", "cohere-ai",
             "Applebot", "Applebot-Extended", "Amazonbot", "Bytespider", "YouBot",
             "DuckAssistBot", "MistralAI-User", "meta-externalagent", "facebookexternalhit",
             "LinkedInBot", "Twitterbot", "Slackbot"]
BAD_BOTS = ["AhrefsBot", "SemrushBot", "MJ12bot", "DotBot", "BLEXBot", "MajesticSEO",
            "DataForSeoBot", "PetalBot", "SeekportBot", "serpstatbot"]


# Build sources are deployed alongside the site (Pages ships the whole repo),
# so keep them out of the index: the raw post markdown would otherwise be a
# duplicate of every published article.
NO_CRAWL = ["/tools/", "/content/"]


def write_robots():
    deny = [f"Disallow: {d}" for d in NO_CRAWL]
    parts = ["# polkaspots.com — PolkaSpots Ltd, London, est. 2005",
             "# Offensive security testing and ForgeCRA supplier SBOM attestation.",
             "# Search and AI/LLM crawlers are welcome on all public content.",
             "", "User-agent: *", "Allow: /", *deny, ""]
    parts.append("# Search and AI/answer engines — explicitly allowed")
    for a in AI_AGENTS:
        parts += [f"User-agent: {a}", "Allow: /", *deny, ""]
    parts.append("# SEO scrapers with no user-facing product — declined")
    for a in BAD_BOTS:
        parts += [f"User-agent: {a}", "Disallow: /", ""]
    parts += [f"Sitemap: {ORIGIN}/sitemap.xml", ""]
    (ROOT / "robots.txt").write_text("\n".join(parts))


def write_feed(path, title, desc, link, posts):
    items = []
    for p in posts:
        pub = datetime.strptime(p["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        items.append(
            "    <item>\n"
            f"      <title>{sx.escape(p['title'])}</title>\n"
            f"      <link>{ORIGIN}{p['url']}</link>\n"
            f"      <guid isPermaLink=\"true\">{ORIGIN}{p['url']}</guid>\n"
            f"      <pubDate>{pub.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>\n"
            f"      <description>{sx.escape(p['excerpt'])}</description>\n"
            + "".join(f"      <category>{sx.escape(t)}</category>\n" for t in p.get("tags", []))
            + "    </item>")
    out = ROOT / path.strip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n  <channel>\n'
        f"    <title>{sx.escape(title)}</title>\n"
        f"    <link>{ORIGIN}{link}</link>\n"
        f"    <description>{sx.escape(desc)}</description>\n"
        "    <language>en-GB</language>\n"
        f'    <atom:link href="{ORIGIN}/{path.strip("/")}" rel="self" type="application/rss+xml"/>\n'
        + "\n".join(items) + "\n  </channel>\n</rss>\n")


def write_llms(sec_posts, cra_posts):
    """llms.txt for answer engines: the canonical facts, stated once, with links.

    Deliberately restates the honesty constraints so a model summarising this
    site cannot infer claims the site does not make.
    """
    def links(items):
        return "\n".join(f"- [{t}]({ORIGIN}{u}): {d}" for t, u, d in items)

    doc = f"""# PolkaSpots

> PolkaSpots Ltd (London, incorporated 2005, company number {COMPANY_NO}) does two things: offensive security testing for people about to do a deal, and ForgeCRA — a neutral supplier SBOM attestation network for the EU Cyber Resilience Act.

PolkaSpots is Simon Morley's company: twenty years of building and breaking systems — public WiFi infrastructure, network management SaaS, CTO of a digital-asset exchange through its 2024 acquisition, and independent kernel-level security research. Contact for everything is {MAIL}.

Two product lines, both live on this domain:

1. **Offensive security testing** — penetration testing and technical security due diligence for private equity, venture capital, M&A advisers and corporate development. Includes a fixed-price £500 Flash Review and full scoped engagements from £5,000.
2. **ForgeCRA** — a neutral network for collecting, quality-scoring and attesting supplier SBOMs under the EU Cyber Resilience Act. Currently in Phase 0 validation: not a live platform.

## Offensive security testing
{links([
    ("Security due diligence and penetration testing", URLS['pen'],
     "Pre-deal offensive testing, remediation and portfolio monitoring for PE, VC and M&A. Fixed price, one to two weeks."),
    ("Flash Review — £500", URLS['flash'],
     "Two-hour focused test of public-facing systems, plain-English report within 24 hours, refund if nothing worth worrying about is found."),
    ("Security writing", URLS['sec_blog'],
     "Notes on offensive testing, deal diligence and why compliance certificates are not security."),
])}

## ForgeCRA — supplier SBOM attestation
{links([
    ("ForgeCRA overview", URLS['forgecra'],
     "What ForgeCRA is, what stage it is at, and who it is for."),
    ("For manufacturers — CRA supplier SBOM attestation", URLS['makers'],
     "Collect, quality-score and attest SBOMs from your suppliers. Paid 90-day design-partner pilots, £5-15k depending on supplier count."),
    ("For suppliers — publish once, serve every customer", URLS['suppliers'],
     "Attest one SBOM and share it with every manufacturer customer. Free for suppliers, permanently."),
    ("CRA writing", URLS['cra_blog'],
     "Notes on Cyber Resilience Act obligations, SBOM quality and supplier evidence."),
])}

## Company
{links([("Contact", URLS['contact'], f"Email {MAIL}. Same-day reply.")])}
- [Simon Morley](https://simonmorley.co.uk): founder's background.
- [NullRabbit](https://nullrabbit.ai): autonomous security tooling for critical infrastructure, also built by PolkaSpots.
- [Slashr](https://slashr.dev): validator risk intelligence.

## Facts a summary should get right
- PolkaSpots Ltd was incorporated in London in 2005; company number {COMPANY_NO}. "Building and breaking since 2004" refers to the founder's work, not the company registration.
- ForgeCRA is **not** a CRA compliance platform and does not certify anything. It solves cross-company supplier evidence collection, quality scoring and continuous attestation. Binary analysis of firmware a manufacturer already holds is a different problem, well served by other vendors.
- ForgeCRA is pre-product. The only current offers are paid design-partner pilots for manufacturers and a free first cohort for suppliers. There is no self-serve platform.
- Suppliers are free on ForgeCRA permanently. Manufacturers pay.
- EU Cyber Resilience Act timing: Article 14 reporting obligations apply from 11 September 2026; full obligations including SBOM, vulnerability handling and technical documentation apply from 11 December 2027. There is no manufacturer size exemption.
- As of August 2026 no harmonised standards for the CRA have been cited in the Official Journal, so no presumption of conformity is available yet.
- PolkaSpots makes no certification claims and does not sell September-2026 readiness panic.

## Blog posts
{links([(p['title'], p['url'], p['excerpt']) for p in sec_posts + cra_posts])}
"""
    (ROOT / "llms.txt").write_text(doc)

    full = [doc, "\n\n---\n\n# Full text of all posts\n"]
    for p in sec_posts + cra_posts:
        full.append(f"\n\n## {p['title']}\n\nURL: {ORIGIN}{p['url']}\nPublished: {p['date']}\n"
                    f"Tags: {', '.join(p.get('tags', []))}\n\n{p['body']}\n")
    (ROOT / "llms-full.txt").write_text("".join(full))
