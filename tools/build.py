#!/usr/bin/env python3
"""Build polkaspots.com. Run from the repo root: python3 tools/build.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from engine import *  # noqa

MAKERS, SUPPLIERS = URLS["makers"], URLS["suppliers"]

STRIPE = "https://buy.stripe.com/eVq5km3u2bcEgLx77KgrS00"

sec_posts = load_posts("security")
cra_posts = load_posts("forgecra")

# Deterministic sitemap: pages inherit the newest post date rather than today,
# so two builds of the same commit are byte-identical.
import engine
engine.DEFAULT_LASTMOD = max(p["date"] for p in sec_posts + cra_posts)


def feed_head(path, title):
    return f'\n  <link rel="alternate" type="application/rss+xml" title="{title}" href="{path}">'


# ==================================================================== HOME
emit("/",
     "PolkaSpots — Offensive Security &amp; CRA Supplier Evidence",
     "Penetration testing and security due diligence for PE, VC and M&amp;A, plus ForgeCRA — neutral supplier SBOM attestation for the EU Cyber Resilience Act.",
     f"""
  <main>
    <section class="band band--home-hero">
      <div class="wrap">
        <h1 class="h1 h1--home">Offensive security &amp;<br>Supply-chain evidence for the CRA.</h1>
        <p class="lede">PolkaSpots builds and breaks systems. Three current products.</p>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
        <div class="cards">
          <article class="card card--ink">
            <div class="card-tags">
              <span class="tag tag--live">LIVE</span>
              <span class="tag-meta">OFFENSIVE SECURITY</span>
            </div>
            <div>
              <h2>Flash Review</h2>
              <p class="card-tagline">You break it, you buy it. So let us break it first.</p>
            </div>
            <p class="card-body">Fast, scoped assessment before you commit.</p>
            <div class="card-actions">
              <a class="act" href="{URLS['flash']}">FLASH REVIEW — £500</a>
            </div>
          </article>

          <article class="card">
            <div class="card-tags">
              <span class="tag">LIVE</span>
              <span class="tag-meta">OFFENSIVE SECURITY</span>
            </div>
            <div><h2>Penetration Testing</h2></div>
            <p class="card-body">Full scoped testing when you need depth, not a sample — before a deal, a release, or a board review.</p>
            <div class="card-actions">
              <a class="act act--ink" href="{URLS['pen']}">FULL PENTEST →</a>
            </div>
          </article>

          <article class="card">
            <div class="card-tags">
              <span class="tag">IN VALIDATION</span>
              <span class="tag-meta">SUPPLY-CHAIN EVIDENCE · EU CRA</span>
            </div>
            <div>
              <h2>ForgeCRA</h2>
              <p class="card-tagline">CRA makes you responsible for evidence you don't control.</p>
            </div>
            <p class="card-body">Neutral network for collecting, scoring and attesting supplier SBOMs.</p>
            <div class="card-actions">
              <a class="act act--ink" href="{URLS['forgecra']}">FOR MANUFACTURERS →</a>
              <a class="quiet" href="{SUPPLIERS}">Suppliers publish here — free →</a>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('Who we are', '01')}
        <div class="split">
          <p class="statement">PolkaSpots Ltd, London, 2005. <a href="https://simonmorley.co.uk">Simon Morley's</a> vehicle for twenty years — public WiFi, network SaaS, exchange CTO, kernel research.</p>
          <p class="body" style="padding-top: 6px;">We know where engineers cut corners because we've spent two decades running the teams working to the same deadlines.</p>
        </div>
      </div>
    </section>

    <section class="band band--end">
      <div class="wrap">
{sec_head('Get in touch', '02')}
        <div class="act-row">
          <p class="statement" style="max-width: 520px;">Security testing or a CRA supplier problem — same inbox, same day reply.</p>
          <div>
            <a class="act act--ink act--mail" href="mailto:{MAIL}">EMAIL US<span aria-hidden="true">→</span></a>
            <p class="act-note">Send us an email. We'll reply today.</p>
          </div>
        </div>
      </div>
    </section>
  </main>
""",
     "home", priority="1.0", changefreq="weekly",
     ld=jsonld(ORG,
               {"@type": "WebSite", "@id": f"{ORIGIN}/#website", "url": ORIGIN,
                "name": "PolkaSpots", "publisher": {"@id": f"{ORIGIN}/#org"},
                "inLanguage": "en-GB"},
               {"@type": "ProfessionalService", "name": "PolkaSpots",
                "url": ORIGIN, "email": MAIL, "parentOrganization": {"@id": f"{ORIGIN}/#org"},
                "areaServed": ["GB", "EU"],
                "serviceType": ["Penetration Testing", "Technical Security Due Diligence",
                                "Pre-deal Security Assessment", "Post-acquisition Remediation",
                                "Portfolio Security Monitoring", "SBOM Attestation"]}))


# ==================================================================== PEN TESTING
offers = [
    ("Full Pentest", "From £5,000", "",
     "Proper thorough penetration test. Infrastructure, apps, APIs, cloud, code — everything that matters. Takes one to two weeks. Fixed price, scoped upfront so there are no surprises. You get a clear report with prioritised findings, full technical detail, and a plan to fix everything. You talk to the person doing the work, not a project manager."),
    ("Remediation", "Scoped per engagement", "remediation",
     "We don't just find problems. We fix them. We work alongside your engineers to patch vulnerabilities, harden configurations, rotate credentials, sort out cloud permissions — whatever needs doing. This is what makes us different from everyone else in this space. Most security firms stop at the report. We keep going until it's actually sorted."),
    ("Ongoing Monitoring", "Monthly retainer", "monitoring",
     "For PE and VC firms with a portfolio. Continuous visibility into the security posture of your investments. We keep watching so you know when something's gone wrong before it becomes a headline. Regular testing, ongoing advice, and a direct line to someone who knows your systems."),
]
offer_cards = "\n".join(
    f'          <div class="offer"{f' id="{a}"' if a else ""}><div><h2>{n}</h2>'
    f'<div class="price">{p}</div></div><p>{b}</p></div>' for n, p, a, b in offers)

findings = [
    "Someone was about to put serious money into a SaaS company. We got into their entire customer database in four hours through a misconfigured API. Wasn't in the data room. Deal got renegotiated. We locked it down within a week of close.",
    "PE firm buying a fintech platform. Production database was sitting on the open internet with default credentials. The company had a current ISO 27001 cert. We gave the buyer a plan to fix it before close and built the cost into the deal. Sorted within the first week.",
    "Growth equity deal for an infrastructure company. Three critical unpatched holes in their customer-facing services, plus AWS keys hardcoded in a public GitHub repo. Seller had called their security posture &ldquo;mature.&rdquo; Keys rotated, services patched, proper secrets management in place within ten days.",
    "Strategic acquisition of a crypto exchange. The technical docs said hot and cold wallets were segregated. They weren't. Material misrepresentation caught before close. Wallet architecture redesigned post-acquisition.",
    "Token acquisition of a DeFi protocol. Found a reentrancy vulnerability in the core Solidity contracts that would let an attacker drain the liquidity pool. A well-known audit firm had signed off on them. Contracts rewritten and redeployed before the deal closed.",
    "PE roll-up of a healthtech platform. Chained three weaknesses together — an open endpoint leaked an internal API, which leaked staff credentials, which got us into the patient records database. None of them looked critical on their own. Together they were devastating. Full chain closed within two weeks.",
    "Late-stage VC round in a B2B SaaS company. Found an admin panel at a predictable URL with no login. Full tenant data for every customer — including the investor's own portfolio company. Found it in the first thirty minutes.",
    "Strategic investment in a smart contract platform. The deployed contracts had privileged owner functions with no timelock and no multisig. One compromised key and all user funds were gone. Governance and key management overhauled after close.",
]
finding_rows = "\n".join(
    f'          <div class="row row--num"><span class="row-n">{i:02d}</span><p>{t}</p></div>'
    for i, t in enumerate(findings, 1))

latest_sec = "".join(
    f'          <li><a href="{p["url"]}">{p["title"]}</a> <span class="post-date">{p["date"]}</span></li>'
    for p in sec_posts[:3])

emit(URLS["pen"],
     "Security Due Diligence &amp; Penetration Testing — PolkaSpots",
     "Pre-deal offensive security testing for PE, VC and M&amp;A. We break into the target, tell you what it means for the deal, then fix it with their engineers.",
     f"""
  <main>
    <section class="band band--hero">
      <div class="wrap">
        <p class="eyebrow eyebrow--violet">Penetration testing</p>
        <h1 class="h1 h1--page">You break it, you buy it. So let us break it first.</h1>
        <p class="lede lede--page">You're about to buy a company, ship a product, or answer a board. We try to break in first and tell you what we find — then work with the engineers to sort it out.</p>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('The problem', '01')}
        <div class="split">
          <p class="statement">Traditional security reviews are broken. You get a 200-page report written by someone who's never touched a terminal. It's full of risk matrices and colour-coded tables. The deal closes. The report goes in a drawer. Six months later something blows up that was buried on page 147.</p>
          <p class="body" style="padding-top: 6px;">Compliance certifications mean someone filled in a form correctly. They don't mean the production database isn't open to the internet.</p>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('What we offer', '02')}
        <div class="offer-lead">
          <div><h2>Flash Review</h2><div class="price">£500</div></div>
          <div>
            <p>Two hours, max velocity. We look at your public-facing stuff and find what's wrong. You get a plain-English report within 24 hours — what we found, how bad it is, what to do about it. If we find nothing worth worrying about, you don't pay.</p>
            <a class="act" href="{URLS['flash']}">LEARN MORE AND BUY →</a>
          </div>
        </div>
        <div class="offers">
{offer_cards}
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head("What we've found", '03')}
        <div class="rows">
{finding_rows}
        </div>
        <p class="note">These are representative. Real engagements are confidential.</p>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('Who this is for', '04')}
        <div class="split">
          <p class="statement">If you're buying a company — or investing in one — and you want to know whether the tech is actually solid before you sign, talk to us.</p>
          <div class="split-stack">
            <p class="body">We work with PE firms, VCs, M&amp;A lawyers, corporate finance advisors and insurance underwriters — anyone in a deal who'd rather find out now than later. We also work directly with companies who want to know where they stand before a launch, an audit, or a customer security review.</p>
            <div>
              <a class="act act--ink" href="{BOOK_30}" data-goal="{BOOK_GOAL}" data-goal-detail="book_pen" target="_blank" rel="noopener">BOOK A {CALL_MINS}-MINUTE CALL</a>
              <p class="act-note">Or <a href="mailto:{MAIL}">email us</a> — same-day reply with a clear scope and a fixed price.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="band band--end">
      <div class="wrap">
{sec_head('Writing', '05')}
        <div class="split">
          <p class="statement">Notes on offensive testing, deal diligence, and what a security review is actually worth.</p>
          <div class="split-stack">
            <ul class="post-mini">
{latest_sec}
            </ul>
            <p><a class="quiet" href="{URLS['sec_blog']}">All security writing →</a></p>
          </div>
        </div>
      </div>
    </section>
  </main>
""",
     "pen", priority="0.9", changefreq="weekly",
     extra_head=feed_head(URLS["sec_blog"] + "feed.xml", "PolkaSpots security writing"),
     ld=jsonld(ORG, breadcrumbs([("Home", "/"), ("Security due diligence", URLS["pen"])]),
               {"@type": "Service", "name": "Technical Security Due Diligence",
                "serviceType": "Penetration testing and pre-deal security assessment",
                "provider": {"@id": f"{ORIGIN}/#org"}, "areaServed": ["GB", "EU"],
                "url": ORIGIN + URLS["pen"],
                "description": "Pre-deal offensive security testing, remediation and portfolio monitoring for private equity, venture capital and M&A.",
                "offers": [{"@type": "Offer", "name": "Flash Review", "price": "500", "priceCurrency": "GBP"},
                           {"@type": "Offer", "name": "Full Pentest", "priceCurrency": "GBP",
                            "priceSpecification": {"@type": "PriceSpecification", "minPrice": "5000", "priceCurrency": "GBP"}}]}))


# ==================================================================== FLASH REVIEW
what_you_get = [
    ("01", "A real vulnerability", "found on your public-facing systems. Not a scanner output. Not a theoretical risk. Something an attacker could actually use."),
    ("02", "A plain-English writeup.", "What we found, how bad it is, and what to do about it. No jargon, no filler, no 50-page PDF."),
    ("03", "Recommendations for fixing.", "Clear steps to sort it out. Or we can fix it for you — separate conversation."),
    ("04", "Delivered within 24 hours.", "You'll hear from us the next day with findings or a refund."),
]
whos_it_for = [
    ("Startups", "who've never had a security review and want to know where they stand."),
    ("CTOs", "wanting an outside perspective before a board meeting or fundraise."),
    ("Companies in a deal", "wanting a quick read on a target before committing."),
    ("Anyone wondering", "&ldquo;are we actually secure?&rdquo; and wanting a straight answer."),
]
how_it_works = [
    ("01", "Pay £500 via Stripe."), ("02", "Tell us your domain and any useful context."),
    ("03", "We spend up to two hours trying to break in."),
    ("04", "Within 24 hours: a short report on what we found."),
    ("05", "Nothing found? Money back. No questions."),
]
rows_get = "\n".join(f'          <div class="row row--num"><span class="row-n">{n}</span>'
                     f'<p><strong>{l}</strong> {r}</p></div>' for n, l, r in what_you_get)
rows_for = "\n".join(f'          <div class="row"><p><strong>{l}</strong> {r}</p></div>'
                     for l, r in whos_it_for)
steps = "\n".join(f'          <div class="step"><div class="step-n">{n}</div><p>{t}</p></div>'
                  for n, t in how_it_works)

emit(URLS["flash"],
     "£500 Flash Security Review in 24 Hours — PolkaSpots",
     "A real vulnerability on your website within 24 hours for a fixed £500. Two hours, one experienced tester, plain-English report. Nothing found, you don't pay.",
     f"""
  <main>
    <section class="band band--hero">
      <div class="wrap">
        <p class="eyebrow eyebrow--violet">Flash Review — £500</p>
        <h1 class="h1 h1--page">We'll find a vulnerability on your website. Not a theoretical one. A real one.</h1>
        <p class="lede lede--page">£500. Two hours. One real person with 20+ years experience. If we can't find something worth worrying about within 24 hours, you don't pay.</p>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('What you get', '01')}
        <div class="rows">
{rows_get}
        </div>
        <a class="act act--lg" href="{STRIPE}" style="margin-top: 40px;">BUY A FLASH REVIEW — £500</a>
      </div>
    </section>

    <section class="band--ink">
      <div class="wrap">
{sec_head("What this isn't", '02')}
        <div class="cols-3">
          <p class="statement" style="font-size: 21px; line-height: 1.4;">It's not a vulnerability scan. We don't run Nessus and email you the output.</p>
          <p class="statement" style="font-size: 21px; line-height: 1.4;">It's not a full pentest. Two hours isn't enough for that — this is a fast, focused look at your attack surface.</p>
          <p class="statement" style="font-size: 21px; line-height: 1.4;">It's not a sales funnel disguised as a service. If you want a full pentest afterwards, great. If you don't, that's fine too. No follow-up calls, no &ldquo;let's schedule a demo.&rdquo;</p>
        </div>
      </div>
    </section>

    <section class="band band--pad" style="padding-bottom: 0;">
      <div class="wrap">
{sec_head("Who it's for", '03')}
        <div class="rows">
{rows_for}
        </div>
      </div>
    </section>

    <section class="band band--gap band--end">
      <div class="wrap">
{sec_head('How it works', '04')}
        <div class="cols-5">
{steps}
        </div>
        <a class="act act--lg" href="{STRIPE}" style="margin-top: 48px;">BUY A FLASH REVIEW — £500</a>
        <p class="act-note">Secure payment via Stripe. No subscription. No commitment. Questions first? <a href="mailto:{MAIL}">Email us</a>.</p>
      </div>
    </section>
  </main>
""",
     "flash", priority="0.9", changefreq="weekly",
     ld=jsonld(ORG, breadcrumbs([("Home", "/"), ("Flash Security Review", URLS["flash"])]),
               {"@type": "Service", "name": "Flash Security Review",
                "serviceType": "Security testing", "provider": {"@id": f"{ORIGIN}/#org"},
                "areaServed": ["GB", "EU"], "url": ORIGIN + URLS["flash"],
                "description": "Two-hour focused security test of public-facing systems by an experienced penetration tester, with a plain-English report within 24 hours.",
                "offers": {"@type": "Offer", "price": "500", "priceCurrency": "GBP",
                           "availability": "https://schema.org/InStock", "url": ORIGIN + URLS["flash"]}}))


# ==================================================================== FORGECRA ROUTER
# Deliberately short. This page is a router, not a marketing page: headline,
# one line, two equal-weight cards, one clarifying sentence. Nothing else.
emit(URLS["forgecra"],
     "ForgeCRA — Supplier SBOM Attestation for the EU CRA",
     "Neutral network for supplier SBOM attestation under the EU Cyber Resilience Act. One offer for manufacturers, one for suppliers.",
     f"""
  <main>
    <section class="band band--hero">
      <div class="wrap">
        <p class="eyebrow eyebrow--violet">A PolkaSpots product</p>
        <h1 class="h1 h1--page">ForgeCRA</h1>
        <p class="lede lede--page">Neutral network for supplier SBOM attestation under the EU Cyber Resilience Act.</p>
        <p class="body" style="margin-top: 24px; max-width: 74ch;">Under the CRA, the manufacturer is responsible for evidence that sits with suppliers. Existing tools analyse what a manufacturer already holds; they cannot make a supplier send anything. ForgeCRA collects, quality-scores and attests SBOMs across company boundaries — one publication from the supplier, served to every customer who needs it.</p>
      </div>
    </section>

    <section class="band band--end">
      <div class="wrap">
        <div class="cards" style="grid-template-columns: repeat(2, minmax(0, 1fr));">
          <article class="card">
            <div><h2>For manufacturers</h2></div>
            <p class="card-body">CRA makes you responsible for evidence you don't control.</p>
            <div class="card-actions">
              <a class="act act--ink" href="{MAKERS}">CONTINUE →</a>
            </div>
          </article>

          <article class="card">
            <div><h2>For suppliers</h2></div>
            <p class="card-body">Publish once. Serve every customer.</p>
            <div class="card-actions">
              <a class="act act--ink" href="{SUPPLIERS}">CONTINUE →</a>
            </div>
          </article>
        </div>
        <p class="router-note">Two different offers. Choose the one that matches your role.</p>
        <p class="router-note">Not sure which applies to you? <a href="{BOOK_30}" data-goal="{BOOK_GOAL}" data-goal-detail="book_router" target="_blank" rel="noopener">Book a {CALL_MINS}-minute call →</a></p>
        <p class="router-note"><a class="quiet" href="{URLS['cra_blog']}">Writing on the CRA, SBOM quality and supplier evidence →</a></p>
      </div>
    </section>
  </main>
""",
     "forgecra", priority="0.9", changefreq="monthly", forgecra=True,
     ld=jsonld(ORG, breadcrumbs([("Home", "/"), ("ForgeCRA", URLS["forgecra"])]),
               {"@type": "Product", "name": "ForgeCRA", "url": ORIGIN + URLS["forgecra"],
                "brand": {"@id": f"{ORIGIN}/#org"},
                "category": "Supply chain security evidence",
                "description": "Neutral supplier SBOM attestation network for the EU Cyber Resilience Act. In Phase 0 validation; paid design-partner pilots for manufacturers, free for suppliers."}))


# ==================================================================== FORGECRA — MANUFACTURERS
fc_problems = [
    "Suppliers send incomplete, outdated, or unusable SBOMs — when they send anything.",
    "Full CRA obligations land 11 December 2027: SBOM, vulnerability handling, technical documentation. No size exemption.",
    "The tools you may already own analyse what's on your network. They can't make a supplier send you evidence.",
]
fc_stages = [
    ("01", "Collect", "We request structured SBOMs from your suppliers and chase them so you don't.",
     "Structured requests to your suppliers, chased for you"),
    ("02", "Attest", "Every submission is quality-scored against CRA / CISA minimum elements and signed as a supplier attestation.",
     "Quality-scored against CRA / CISA minimum elements, signed and dated"),
    ("03", "Share", "Evidence stays current as components change — audit-ready when customers, auditors, or market surveillance ask.",
     "Audit-ready evidence pack whenever it's asked for"),
]
fc_faq = [
    ("We're building our own supplier portal.",
     "Then each supplier does the work once for you, and again for every other customer with a portal. Suppliers comply badly with work that does not compound — that is the pattern behind the SBOMs you are getting today. A neutral exchange lets a supplier publish once and share with all of you, which is the only version they have a reason to keep current."),
    ("We already use ONEKEY / Finite State / similar.",
     "They analyse what you already hold. We get you what you don't hold. We complement them — several design partners will run both."),
    ("Email works fine.",
     "At 20+ suppliers with a 24-hour reporting clock, email has no quality scoring, no attestation trail, and no update propagation. The pilot measures whether that's true for you."),
    ("We're waiting for the harmonised standards.",
     "As of 19 August 2026, no CRA harmonised standard has been ratified or cited in the Official Journal, so no product category has a presumption of conformity. We map Annex I now and re-map automatically when they land. Supplier collection takes months — waiting is the expensive option."),
]
prob_cols = "\n".join(f'          <p class="claim">{t}</p>' for t in fc_problems)
stage_cols = "\n".join(
    f'          <div>\n            <div class="stage-n">{n}</div>\n'
    f'            <div class="stage-title">{t}</div>\n'
    f'            <p class="stage-step">{s}</p>\n'
    f'            <p class="stage-body">{b}</p>\n          </div>' for n, t, s, b in fc_stages)
DECAY_NOTE = ("""<!-- DECAYING CLAIM: verify monthly against
     https://www.cyberresilienceact.eu/state-of-play.html
     Last verified 2026-08-19. Update the date in the visible copy each time. -->
          """)
faq_cols = "\n".join(
    '          '
    + (DECAY_NOTE if "harmonised standards" in q else "")
    + f'<div class="faq"><h3>&ldquo;{q}&rdquo;</h3><p>{a}</p></div>' for q, a in fc_faq)

emit(MAKERS,
     "CRA Supplier SBOM Attestation for Manufacturers — ForgeCRA",
     "The CRA makes you responsible for evidence you don't control. ForgeCRA collects, scores and attests supplier SBOMs. Paid 90-day design-partner pilots.",
     f"""
  <main>
    <section class="band band--hero">
      <div class="wrap">
        <p class="eyebrow eyebrow--violet">ForgeCRA · For manufacturers</p>
        <h1 class="h1 h1--page">CRA makes you responsible for evidence you don't control.</h1>
        <div class="act-row" style="margin-top: 32px;">
          <p class="lede lede--page" style="margin: 0;">ForgeCRA collects, quality-scores, and attests SBOMs from your suppliers — so your Cyber Resilience Act evidence chain doesn't live in your inbox.</p>
          <p class="hero-credibility">Built by Simon Morley — repeat founder, infrastructure and security — inside PolkaSpots Ltd, which has been doing network and security work since 2005.</p>
          <!-- CALENDAR-SWAP: replace href with the Cal.com/Calendly booking link. -->
          <a class="act act--ink act--lg" href="{BOOK_30}" data-goal="{BOOK_GOAL}" data-goal-detail="book_mfr_hero" target="_blank" rel="noopener">BOOK A 30-MINUTE PILOT CALL</a>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('The problem', '01')}
        <div class="cols-3">
{prob_cols}
        </div>
        <p class="body" style="margin-top: 36px; max-width: 74ch;">CRA penalties reach €15 million or 2.5% of worldwide annual turnover. That is why this has a budget line. It is not the reason to move now. The reason to move now is that supplier collection takes months, and December 2027 does not move.</p>
      </div>
    </section>

    <section class="band--ink">
      <div class="wrap">
{sec_head('How it works', '02')}
        <div class="cols-3">
{stage_cols}
        </div>
        <p class="note">Illustrative only. During pilots this workflow is run for you by hand — there is no self-serve platform yet.</p>
      </div>
    </section>

    <section class="band band--pad">
      <div class="wrap">
{sec_head('Why your suppliers will actually respond', '03')}
        <div class="split">
          <p class="statement">ForgeCRA does not sell analysis, is not owned by anyone who does, and never resells supplier data.</p>
          <p class="body" style="padding-top: 6px;">That matters to you, not only to them. A supplier will not hand component detail to a vendor that also sells competitive analysis to their customers — which is why supplier data collection stalls when it is run by an analysis vendor or by a manufacturer directly. Neutrality is what makes the ask answerable.</p>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('This shape has worked before', '04')}
        <div class="split">
          <p class="statement">E-invoicing had the same problem: every buyer wanted a different portal, and suppliers complied badly with all of them. Peppol solved it with one connection to many counterparties instead of bilateral integrations.</p>
          <p class="body" style="padding-top: 6px;">Peppol had a government mandate behind it. The CRA creates the same pressure on evidence without specifying the plumbing. That gap is what ForgeCRA is built for — and it is also the honest risk: nobody is mandating the network, so it has to earn its density.</p>
        </div>
      </div>
    </section>

    <section class="band band--pad">
      <div class="wrap">
{sec_head('The offer', '05')}
        <div class="offer-box">
          <div>
            <div class="kicker">DESIGN PARTNERS — PAID 90-DAY PILOT</div>
            <h2>We're selecting three design partners for a paid 90-day pilot (£5–15k depending on supplier count).</h2>
          </div>
          <div>
            <p>You get the full attestation workflow run for you; you shape the product; founding pricing locked for year one.</p>
            <!-- CALENDAR-SWAP -->
            <a class="act act--lg" href="{BOOK_30}" data-goal="{BOOK_GOAL}" data-goal-detail="book_mfr_offer" target="_blank" rel="noopener">BOOK A 30-MINUTE PILOT CALL</a>
          </div>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('Questions we get', '06')}
        <div class="cols-3">
{faq_cols}
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('How we will know if this failed', '07')}
        <div class="split">
          <p class="statement">At pilot start we record your current supplier response rate. That is the control.</p>
          <p class="body" style="padding-top: 6px;">If our collection does not beat it, the pilot has not worked, and we will say so in the readout rather than hand you a dashboard. This is a joint experiment with a paid delivery floor, not a licence.</p>
        </div>
      </div>
    </section>

    <section class="band band--end">
      <div class="wrap">
{sec_head('Or send us the details', '08')}
        <div class="split split--form">
          <p class="statement statement--sm">If a call is easier later, tell us where you stand and we'll come back to you.</p>
          <div>
            <!-- FORM-SWAP: posts via mailto so it works with JS disabled and needs no backend
                 (Spec §3 sanctions the mailto fallback). For notification + spreadsheet set
                 action="https://formspree.io/f/YOUR_ID" method="POST" and delete enctype.
                 Field names are the Spec §4.5 set. -->
            <form action="mailto:{MAIL}?subject=ForgeCRA%20enquiry%20%E2%80%94%20manufacturer" method="post" enctype="text/plain"
                  data-goal="form_submit" data-form="mfr" data-endpoint="/api/submit" data-subject="ForgeCRA enquiry — manufacturer">
              <p hidden aria-hidden="true"><label>Leave this empty<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
              <div class="fields">
                <label class="field"><span>Name</span><input type="text" name="name" required></label>
                <label class="field"><span>Work email</span><input type="email" name="email" required></label>
                <label class="field"><span>Company</span><input type="text" name="company" required></label>
                <label class="field"><span>Role</span><input type="text" name="role" required></label>
                <label class="field"><span>Upstream suppliers</span>
                  <select name="suppliers" required>
                    <option value="">Select…</option>
                    <option value="&lt;10">Fewer than 10</option>
                    <option value="10-50">10–50</option>
                    <option value="50-200">50–200</option>
                    <option value="200+">200+</option>
                  </select>
                </label>
                <label class="field"><span>Biggest supplier-evidence pain</span><input type="text" name="pain" placeholder="One line is plenty" required></label>
              </div>
              <button type="submit" class="act act--ink act--lg" style="margin-top: 32px;">SEND THE DETAILS</button>
            </form>
            <p class="form-note">You're a supplier, not a manufacturer? <a href="{SUPPLIERS}">This is your page →</a></p>
          </div>
        </div>
      </div>
    </section>
  </main>
""",
     "forgecra", priority="0.9", changefreq="weekly", forgecra=True,
     ld=jsonld(ORG,
               breadcrumbs([("Home", "/"), ("ForgeCRA", URLS["forgecra"]), ("For manufacturers", MAKERS)]),
               {"@type": "FAQPage", "mainEntity": [
                   {"@type": "Question", "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in fc_faq]},
               {"@type": "Service", "name": "ForgeCRA supplier SBOM attestation",
                "serviceType": "Supplier SBOM collection, quality scoring and attestation",
                "provider": {"@id": f"{ORIGIN}/#org"}, "areaServed": ["GB", "EU"],
                "url": ORIGIN + MAKERS,
                "description": "Collects, quality-scores and attests SBOMs from a manufacturer's suppliers against CRA and CISA minimum elements. Delivered as a paid 90-day design-partner pilot."}))


# ==================================================================== FORGECRA — SUPPLIERS
sup_problems = [
    "CRA pushes your customers to demand component evidence from you — repeatedly, per customer, per product.",
    "Answering five portals and fifty questionnaires doesn't scale.",
    "Your SBOM is commercially sensitive. You need to control who sees what.",
]
sup_stages = [
    ("01", "Publish", "Upload or generate your SBOM (CycloneDX / SPDX).", "One file, the format you already produce"),
    ("02", "Attest", "Attest it once — signed, dated, quality-scored.", "Signed, dated and quality-scored"),
    ("03", "Share", "Share per-customer with one click. Updates propagate to everyone you've shared with.", "Per customer, your call — updates propagate"),
]
sup_prob_cols = "\n".join(f'          <p class="claim">{t}</p>' for t in sup_problems)
sup_stage_cols = "\n".join(
    f'          <div>\n            <div class="stage-n">{n}</div>\n'
    f'            <div class="stage-title">{t}</div>\n'
    f'            <p class="stage-step">{s}</p>\n'
    f'            <p class="stage-body">{b}</p>\n          </div>' for n, t, s, b in sup_stages)

emit(SUPPLIERS,
     "Publish Your SBOM Once, Serve Every Customer — ForgeCRA",
     "Every customer wants your SBOM in their own portal. Attest once on a neutral exchange, share per customer, control who sees what. Free for suppliers.",
     f"""
  <main>
    <section class="band band--hero">
      <div class="wrap">
        <p class="eyebrow eyebrow--violet">ForgeCRA · For suppliers</p>
        <h1 class="h1 h1--page">Publish once. Serve every customer.</h1>
        <div class="act-row" style="margin-top: 32px;">
          <p class="lede lede--page" style="margin: 0;">A customer of yours is collecting component evidence for the Cyber Resilience Act, and pointed you here. ForgeCRA is the neutral exchange: attest once, share with that customer and every other one, under your control. Free for suppliers, permanently.</p>
          <a class="act act--ink act--lg" href="#cohort-form" data-goal="cta_click" data-goal-detail="cta_sup_hero">JOIN THE FIRST SUPPLIER COHORT</a>
        </div>
      </div>
    </section>

    <section class="band">
      <div class="wrap">
{sec_head('The problem', '01')}
        <div class="cols-3">
{sup_prob_cols}
        </div>
      </div>
    </section>

    <section class="band--ink">
      <div class="wrap">
{sec_head('How it works', '02')}
        <div class="cols-3">
{sup_stage_cols}
        </div>
        <p class="stage-step" style="margin-top: 32px; max-width: 74ch;">If a customer sent you here, step three is already half done — they are waiting on the share, and you keep control of what they see.</p>
        <p class="note">Illustrative only. The first cohort is run with us directly — there is no self-serve platform yet.</p>
      </div>
    </section>

    <section class="band band--pad">
      <div class="wrap">
{sec_head('Neutral by design', '03')}
        <div class="split">
          <p class="statement">ForgeCRA is not a competing analysis vendor, not owned by one, and never resells your data.</p>
          <p class="body" style="padding-top: 6px;">You choose exactly which customers see which products' SBOMs. Free for suppliers, permanently — we charge the side with the regulatory liability, never the side that creates the network.</p>
        </div>
      </div>
    </section>

    <section class="band band--end" id="cohort-form">
      <div class="wrap">
{sec_head('The offer', '04')}
        <div class="offer-box">
          <div>
            <div class="kicker">FIRST SUPPLIER COHORT — FREE, PERMANENTLY</div>
            <h2>We're onboarding a first cohort of suppliers now — tell us your formats and your customers, and help set the standard everyone else will have to follow.</h2>
          </div>
          <div>
            <p>Free for suppliers, permanently. You control who sees what, and updates propagate to every customer you've shared with.</p>
            <a class="act act--lg" href="#cohort-form" data-goal="cta_click" data-goal-detail="cta_sup_offer">JOIN THE FIRST SUPPLIER COHORT</a>
            <p style="margin: 16px 0 0;"><a class="quiet" href="{BOOK_20}" data-goal="{BOOK_GOAL}" data-goal-detail="book_sup_offer" target="_blank" rel="noopener">Or book a {CALL_MINS}-minute call →</a></p>
          </div>
        </div>

        <div class="split split--form" style="margin-top: 56px;">
          <p class="statement statement--sm">Tell us your formats and your customers.</p>
          <div>
            <!-- FORM-SWAP: see the manufacturers page. Field names are the Spec §5.5 set. -->
            <form action="mailto:{MAIL}?subject=ForgeCRA%20supplier%20cohort" method="post" enctype="text/plain"
                  data-goal="form_submit" data-form="sup" data-endpoint="/api/submit" data-subject="ForgeCRA supplier cohort">
              <p hidden aria-hidden="true"><label>Leave this empty<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
              <div class="fields">
                <label class="field"><span>Name</span><input type="text" name="name" required></label>
                <label class="field"><span>Work email</span><input type="email" name="email" required></label>
                <label class="field"><span>Company</span><input type="text" name="company" required></label>
                <label class="field"><span>Role</span><input type="text" name="role" required></label>
                <label class="field"><span>Manufacturer customers</span>
                  <select name="customers" required>
                    <option value="">Select…</option>
                    <option value="1-4">1–4</option><option value="5-9">5–9</option>
                    <option value="10-24">10–24</option><option value="25+">25+</option>
                  </select>
                </label>
                <label class="field"><span>Current SBOM format</span>
                  <select name="format" required>
                    <option value="">Select…</option>
                    <option value="CycloneDX">CycloneDX</option><option value="SPDX">SPDX</option>
                    <option value="Spreadsheet">Spreadsheet</option><option value="None">None</option>
                  </select>
                </label>
                <label class="field field--wide"><span>Which customer sent you?</span>
                  <input type="text" name="referred_by" placeholder="Optional">
                </label>
                <label class="field field--wide"><span>Other manufacturer customers who will ask for this</span>
                  <input type="text" name="other_customers" placeholder="Optional">
                  <small class="field-help">Names help us bring them onto the same exchange so you only publish once.</small>
                </label>
              </div>
              <button type="submit" class="act act--ink act--lg" style="margin-top: 32px;">JOIN THE FIRST SUPPLIER COHORT</button>
            </form>
            <p class="form-note">Nobody sent you and you want to get ahead of this? Same form — tell us who is likely to ask.</p>
            <p class="form-note">You're a manufacturer collecting evidence, not supplying it? <a href="{MAKERS}">This is your page →</a></p>
          </div>
        </div>
      </div>
    </section>
  </main>
""",
     "forgecra", priority="0.9", changefreq="weekly", forgecra=True,
     ld=jsonld(ORG,
               breadcrumbs([("Home", "/"), ("ForgeCRA", URLS["forgecra"]), ("For suppliers", SUPPLIERS)]),
               {"@type": "Service", "name": "ForgeCRA supplier SBOM publishing",
                "serviceType": "SBOM attestation and controlled sharing",
                "provider": {"@id": f"{ORIGIN}/#org"}, "areaServed": ["GB", "EU"],
                "url": ORIGIN + SUPPLIERS,
                "description": "Suppliers attest one SBOM (CycloneDX or SPDX), then share it per customer with updates propagating automatically. Free for suppliers, permanently.",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP",
                           "description": "Free for suppliers, permanently."}}))


# ==================================================================== CONTACT
emit(URLS["contact"],
     "Contact PolkaSpots — Security Testing &amp; CRA Evidence",
     "Email PolkaSpots about penetration testing, security due diligence, or a CRA supplier evidence problem. Same-day reply, usually within the hour.",
     f"""
  <main>
    <section class="band band--pad band--end">
      <div class="wrap">
        <div class="split" style="margin-top: 0; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 72px;">
          <div>
            <h1 class="h1 h1--contact">Get in touch.</h1>
            <p class="lede lede--page" style="margin-top: 26px;">We reply the same day. Usually within the hour.</p>
            <a class="email-link" href="mailto:{MAIL}">{MAIL}</a>
            <p style="margin-top: 28px;"><a class="act act--ink" href="{BOOK_30}" data-goal="{BOOK_GOAL}" data-goal-detail="book_contact" target="_blank" rel="noopener">BOOK A {CALL_MINS}-MINUTE CALL</a></p>
            <p class="act-note">Prefer to talk it through? Grab a slot directly.</p>
          </div>
          <div class="panel">
            <!-- Posts via mailto + enctype="text/plain": no backend, works with JS disabled.
                 For a hosted handler set action="https://formspree.io/f/YOUR_ID" method="POST"
                 and delete enctype — the field names already match. -->
            <form action="mailto:{MAIL}?subject=Enquiry%20via%20polkaspots.com" method="post" enctype="text/plain"
                  data-goal="form_submit" data-form="contact" data-endpoint="/api/submit" data-subject="Enquiry via polkaspots.com">
              <p hidden aria-hidden="true"><label>Leave this empty<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
              <label class="field"><span>Name</span><input type="text" name="name" required></label>
              <label class="field" style="margin-top: 24px;"><span>Email</span><input type="email" name="email" required></label>
              <label class="field" style="margin-top: 24px;"><span>Message</span><textarea name="message" rows="6" required></textarea></label>
              <button type="submit" class="act">SEND</button>
            </form>
            <p class="panel-note">This opens your email client. Prefer to <a href="mailto:{MAIL}">write directly</a>?</p>
          </div>
        </div>
      </div>
    </section>
  </main>
""",
     "contact", priority="0.6",
     ld=jsonld(ORG, breadcrumbs([("Home", "/"), ("Contact", URLS["contact"])]),
               {"@type": "ContactPage", "url": ORIGIN + URLS["contact"],
                "mainEntity": {"@id": f"{ORIGIN}/#org"}}))


# ==================================================================== BLOGS
BLOGS = {
    "security": {
        "url": URLS["sec_blog"], "active": "pen", "parent": ("Security due diligence", URLS["pen"]),
        "eyebrow": "Security writing",
        "h1": "Notes from breaking into things.",
        "lede": "What we find, how we find it, and what a security review is actually worth to someone about to sign a deal.",
        "title": "Security Testing &amp; Due Diligence Blog — PolkaSpots",
        "desc": "Writing on offensive security testing, technical due diligence for investors, and why compliance certificates are not evidence of security.",
        "feed_title": "PolkaSpots security writing", "forgecra": False,
    },
    "forgecra": {
        "url": URLS["cra_blog"], "active": "forgecra", "parent": ("ForgeCRA", URLS["forgecra"]),
        "eyebrow": "ForgeCRA writing",
        "h1": "Notes on the CRA and supplier evidence.",
        "lede": "What the Cyber Resilience Act actually requires, what makes an SBOM usable, and why supplier evidence is a cross-company problem.",
        "title": "EU Cyber Resilience Act &amp; SBOM Blog — ForgeCRA",
        "desc": "Writing on EU Cyber Resilience Act obligations and timing, SBOM quality, CycloneDX and SPDX, and the supplier evidence problem.",
        "feed_title": "ForgeCRA writing", "forgecra": True,
    },
}

for section, cfg in BLOGS.items():
    posts = sec_posts if section == "security" else cra_posts

    rows = "\n".join(
        f'''          <a class="post-row" href="{p['url']}">
            <span class="post-row-date">{p['date']}</span>
            <span class="post-row-main">
              <span class="post-row-title">{p['title']}</span>
              <span class="post-row-excerpt">{p['excerpt']}</span>
              <span class="post-row-tags">{' · '.join(p.get('tags', [])[:5])}</span>
            </span>
          </a>''' for p in posts)

    emit(cfg["url"], cfg["title"], cfg["desc"],
         f"""
  <main>
    <section class="band band--hero">
      <div class="wrap">
        <p class="eyebrow eyebrow--violet">{cfg['eyebrow']}</p>
        <h1 class="h1 h1--page">{cfg['h1']}</h1>
        <p class="lede lede--page">{cfg['lede']}</p>
      </div>
    </section>

    <section class="band band--end">
      <div class="wrap">
{sec_head('All posts', '01')}
        <div class="post-list">
{rows}
        </div>
        <p class="act-note" style="margin-top: 32px;"><a class="quiet" href="{cfg['url']}feed.xml">RSS feed →</a></p>
      </div>
    </section>
  </main>
""",
         cfg["active"], priority="0.8", changefreq="weekly", forgecra=cfg["forgecra"],
         extra_head=feed_head(cfg["url"] + "feed.xml", cfg["feed_title"]),
         ld=jsonld(ORG,
                   breadcrumbs([("Home", "/"), cfg["parent"], ("Blog", cfg["url"])]),
                   {"@type": "Blog", "url": ORIGIN + cfg["url"], "name": cfg["feed_title"],
                    "description": cfg["desc"], "publisher": {"@id": f"{ORIGIN}/#org"},
                    "inLanguage": "en-GB",
                    "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                                  "url": ORIGIN + p["url"], "datePublished": p["date"],
                                  "description": p["excerpt"]} for p in posts]}))

    for idx, p in enumerate(posts):
        prev_p = posts[idx + 1] if idx + 1 < len(posts) else None
        next_p = posts[idx - 1] if idx > 0 else None
        nav_more = ""
        if prev_p or next_p:
            bits = []
            if next_p:
                bits.append(f'<a class="quiet" href="{next_p["url"]}">← {next_p["title"]}</a>')
            if prev_p:
                bits.append(f'<a class="quiet" href="{prev_p["url"]}">{prev_p["title"]} →</a>')
            nav_more = ('        <div class="post-nav">' + "".join(bits) + "</div>")

        # Extractable summary: gives answer engines a clean set of claims to
        # lift, and gives readers the argument before the argument.
        key_points = ""
        if p.get("key_points"):
            items = "".join(f"<li>{md_inline(k)}</li>" for k in p["key_points"])
            key_points = ('        <aside class="keypoints">\n'
                          '          <p class="keypoints-label">In short</p>\n'
                          f'          <ul>{items}</ul>\n'
                          '        </aside>')

        faq_block = ""
        if p.get("faq"):
            qs = "\n".join(
                f'            <div class="faq"><h3>{md_inline(q["q"])}</h3>'
                f'<p>{md_inline(q["a"])}</p></div>' for q in p["faq"])
            faq_block = (f'        <section class="post-faq">\n{sec_head("Questions", "FAQ")}\n'
                         f'          <div class="cols-2" style="margin-top: 28px; gap: 32px;">\n{qs}\n'
                         '          </div>\n        </section>')

        seo_t = p.get("seo_title") or p["title"]
        if len(seo_t) <= 47:
            seo_t += " — PolkaSpots"
        emit(p["url"], seo_t, p.get("meta") or p["excerpt"],
             f"""
  <main>
    <article class="band band--hero">
      <div class="wrap">
        <p class="eyebrow eyebrow--violet"><a href="{cfg['url']}">{cfg['eyebrow']}</a></p>
        <h1 class="h1 h1--page">{p['title']}</h1>
        <p class="post-meta"><time datetime="{p['date']}">{p['date']}</time> · {p.get('author', 'Simon Morley')} · {' · '.join(p.get('tags', [])[:6])}</p>
      </div>
    </article>

    <section class="band band--end">
      <div class="wrap">
{key_points}
        <div class="prose">
{markdown(p['body'])}
        </div>
{faq_block}
{nav_more}
      </div>
    </section>
  </main>
""",
             cfg["active"], priority="0.7", changefreq="monthly", lastmod=p["date"],
             forgecra=cfg["forgecra"],
             extra_head=feed_head(cfg["url"] + "feed.xml", cfg["feed_title"]),
             llms=p["excerpt"],
             ld=jsonld(ORG,
                       breadcrumbs([("Home", "/"), cfg["parent"], ("Blog", cfg["url"]), (p["title"], p["url"])]),
                       {"@type": "BlogPosting", "headline": p["title"],
                        "url": ORIGIN + p["url"],
                        "mainEntityOfPage": {"@type": "WebPage", "@id": ORIGIN + p["url"]},
                        "datePublished": p["date"], "dateModified": p["date"],
                        "description": p["excerpt"], "keywords": ", ".join(p.get("tags", [])),
                        "inLanguage": "en-GB",
                        "author": {"@type": "Person", "name": p.get("author", "Simon Morley"),
                                   "url": "https://simonmorley.co.uk"},
                        "publisher": {"@id": f"{ORIGIN}/#org"},
                        "isPartOf": {"@type": "Blog", "@id": ORIGIN + cfg["url"]}},
                       ({"@type": "FAQPage", "mainEntity": [
                           {"@type": "Question", "name": q["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                           for q in p["faq"]]} if p.get("faq") else None)))

    write_feed(cfg["url"] + "feed.xml", cfg["feed_title"], cfg["desc"], cfg["url"], posts)


# ==================================================================== ARTEFACTS
n = write_sitemap()
write_robots()
write_llms(sec_posts, cra_posts)

print(f"  {n} pages  ·  {len(sec_posts)} security posts  ·  {len(cra_posts)} ForgeCRA posts")
print("  sitemap.xml, robots.txt, llms.txt, llms-full.txt, 2 RSS feeds")
