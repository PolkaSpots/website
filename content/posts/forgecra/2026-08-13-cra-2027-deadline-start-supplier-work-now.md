---
title: "Full CRA obligations are still 2027 — start the supplier work anyway"
seo_title: "CRA 2027 Deadline: Start Supplier SBOM Work Now"
meta: "CRA reporting starts 11 September 2026; full obligations land 11 December 2027. Supplier SBOM collection takes months — waiting compresses the timeline."
date: "2026-08-13"
excerpt: "Reporting obligations begin September 2026 and are event-triggered. The expensive problem sits under the December 2027 date and continues after it."
author: "Simon Morley"
tags: ["cra", "cyber-resilience-act", "cra-deadline", "harmonised-standards", "sbom", "annex-i"]
slug: "cra-2027-deadline-start-supplier-work-now"
key_points:
  - "11 September 2026: reporting obligations for actively exploited vulnerabilities and severe incidents begin. Event-triggered, not a filing deadline."
  - "11 December 2027: full obligations apply — SBOM, vulnerability handling, technical documentation. No manufacturer size exemption."
  - "No harmonised standards have been cited in the Official Journal as of August 2026, so no presumption of conformity is available yet."
  - "Supplier evidence collection takes months. Waiting for standards before starting compresses the only part of the work you do not control."
faq:
  - q: "When does the Cyber Resilience Act actually apply?"
    a: "Article 14 reporting obligations apply from 11 September 2026. The full set of obligations, including SBOM, vulnerability handling and technical documentation, applies from 11 December 2027."
  - q: "Is there a size exemption for small manufacturers?"
    a: "No. Microenterprises and SMEs get some procedural relief in places, but the essential requirements in Annex I apply regardless of company size."
  - q: "Should we wait for the harmonised standards before starting?"
    a: "For finalising a conformity assessment route, waiting is reasonable. For supplier evidence collection it is expensive, because that work takes months regardless of what the standards eventually say and depends on companies you do not control."
  - q: "What happens to our mapping when the standards are cited?"
    a: "Work mapped against Annex I today gets re-mapped when harmonised standards appear. The underlying evidence — which supplier said what, when, and how good it was — does not change because a standard was published."
---

Two dates matter.

**11 September 2026:** reporting obligations for actively exploited vulnerabilities and serious incidents begin. These are event-triggered. A spreadsheet and a process can satisfy the minimum for many organisations.

**11 December 2027:** the full set of obligations applies — SBOM, vulnerability handling processes, technical documentation, and the rest.

A lot of the current noise is about the first date. The more expensive problem sits under the second date and continues after it.

## Why the September date is not the hard one

The reporting obligation is real and worth preparing for, but preparing for it is largely organisational. You need someone who owns the 24-hour clock, a decision path for what counts as reportable, and a route to submit.

Crucially, nothing happens on that date unless something happens to you. There is no filing, no submission, no certificate. If nothing in your products is actively exploited, the date passes without incident.

That is why we do not sell readiness for it. It is being harvested commercially at the moment because it is the nearest date and fear converts, but buying tooling in a scramble to satisfy an event-triggered reporting duty tends to produce something that does not help at all with the December 2027 requirement to evidence what is actually inside your products.

## Why supply-chain work is measured in months

Collecting usable SBOMs from a multi-tier supply chain takes months, not weeks.

Suppliers need time to produce something decent — for many that means changing their build pipeline, not just exporting a file. Manufacturers need time to quality-check what comes back, and to work out which suppliers are producing evidence they can act on and which are producing files that will not help when an advisory lands. And both sides need a way to keep the information current when components change, because a bill of materials produced once describes a moment that has already passed.

None of those steps compress well. They involve other companies, on their schedules, with their priorities.

## The harmonised standards question

Waiting until the harmonised standards are cited — still expected late 2026 to mid-2027 — before starting that work simply compresses the timeline.

It is worth being precise about what the wait buys. As of August 2026 no harmonised standards for the CRA have been cited in the Official Journal, which means no presumption of conformity is available to anyone yet. Everyone is interpreting Annex I directly and documenting their reasoning.

For some decisions that argues for patience. Finalising your conformity assessment route before the standards land risks rework.

For supplier evidence it argues the opposite way. The identity of your suppliers, the quality of what they send you and the cadence on which they send it are not going to be changed by a standards citation. That work is the same work either way, and it is the part of the programme whose timeline you least control.

[ForgeCRA](/cra-sbom-attestation/) maps to the Annex I requirements that exist today and will re-map when the harmonised standards appear. The point of starting now is not to claim early compliance — we make no certification claims of any kind. It is to stop treating supplier evidence as something that can be fixed in a scramble at the end of 2027.

## If you already have tooling

If you already have a working relationship with a binary analysis platform, keep it. It answers a question well, and [that question is not this one](/cra-sbom-attestation/blog/cra-sbom-generation-is-not-the-hard-part/).

The missing piece for most mid-market manufacturers is still the upstream collection and attestation layer. That is the only part we are focused on, and if you want to test whether it is the missing piece for you, the [design-partner pilot](/cra-sbom-attestation/for-manufacturers/) is ninety days and deliberately small.
