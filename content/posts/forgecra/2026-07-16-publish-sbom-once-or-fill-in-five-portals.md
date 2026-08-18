---
title: "Publish once, or fill in five portals"
seo_title: "Publish Your SBOM Once, or Fill In Five Portals"
meta: "Every manufacturer will ask suppliers for SBOMs in their own portal and format. A neutral exchange lets suppliers publish once and control who sees what."
date: "2026-07-16"
excerpt: "Suppliers are about to be asked for SBOMs by every manufacturer they sell into, each with its own format, portal and idea of complete. That does not scale on either side."
author: "Simon Morley"
tags: ["sbom", "suppliers", "cra", "neutral-exchange", "cyclonedx", "spdx", "supply-chain"]
slug: "publish-sbom-once-or-fill-in-five-portals"
key_points:
  - "Per-customer SBOM portals push integration cost onto the party with no regulatory exposure — the supplier — so they get deprioritised."
  - "Manufacturers chasing the same suppliers by email does not scale past roughly twenty upstream relationships."
  - "The pattern that resolved this elsewhere is a neutral exchange: publish once, control visibility, updates propagate. E-invoicing is the usual precedent."
  - "Whether suppliers actually prefer this is unproven. That is why there is a first cohort rather than a launch."
faq:
  - q: "Why not just use a supplier portal?"
    a: "A portal works at around ten suppliers and degrades after that. Each manufacturer builds their own, so every supplier ends up with accounts in five portals, each with a different schema and review cycle. The supplier's cost scales with customer count while their regulatory exposure stays at zero."
  - q: "Which SBOM formats does a neutral exchange need to handle?"
    a: "CycloneDX and SPDX cover essentially all real usage, and both satisfy the commonly used machine-readable requirement. Converting between them is tractable for most practical purposes, so format is rarely the real obstacle."
  - q: "Do suppliers have to pay?"
    a: "No. Suppliers are free permanently. Charging the side that creates the network value is how you kill a network before it exists, so the cost sits with manufacturers, who carry the regulatory liability."
  - q: "Who can see a supplier's SBOM?"
    a: "Only the customers that supplier chooses, per product. A neutral exchange that resold or pooled supplier data would not be neutral, and suppliers would be right not to use it."
---

Suppliers are about to be asked for SBOMs by every manufacturer they sell into. Each manufacturer will have its own preferred format, its own portal, and its own idea of what "complete" looks like.

From the supplier's point of view this does not scale.

From the manufacturer's point of view, chasing the same suppliers through email and one-off questionnaires also does not scale — especially once the number of upstream relationships moves past twenty and a 24-hour reporting clock exists for actively exploited vulnerabilities.

## Why per-customer portals fail

The failure is not technical. Any competent team can stand up a portal, define a schema and send invitations.

It fails because of where the cost lands. Every manufacturer who builds one pushes integration work onto suppliers, and the supplier's total cost grows with the number of customers who do it. The supplier carries no regulatory exposure for your product. So the work gets deprioritised, responses get thin, then late, then stop — and the party left holding the obligation is the one who built the portal.

Multiply that by every manufacturer doing the same thing and you have a system that reliably produces the outcome nobody wanted.

## The pattern that has worked elsewhere

The pattern that has worked in other regulated multi-party settings — e-invoicing is the usual example — is a neutral exchange: the supplier publishes once, controls who can see what, and updates propagate to the parties they have chosen to share with.

The economics invert. The supplier's effort becomes fixed rather than per-customer, which is the only version where doing it well is rational for them. The manufacturer gets structured, scored, current evidence instead of an inbox. And because nobody has to integrate bilaterally, adding the next relationship costs close to nothing.

## Why it has to be neutral

That is the shape [ForgeCRA](/cra-sbom-attestation/) is testing. It is not another manufacturer-owned questionnaire portal, and it is not an analysis vendor trying to become the system of record for every participant's data.

Neutrality is load-bearing rather than a positioning choice. A supplier will not attest deeply into a platform owned by a company that also sells analysis to their customers, and that caution is entirely rational — their component list is commercially sensitive, and it describes their product to people who compete with them.

So: suppliers stay in control of their own SBOMs, choosing which customers see which products. Manufacturers get a structured, attested feed instead of an inbox full of PDFs. Nobody's data is resold.

## The part we have not proved

Whether suppliers will actually prefer this to the current chaos is an open question.

The argument above is coherent and the precedent from e-invoicing is real, but neither of those is evidence about this market. It is entirely possible that suppliers are content to keep emailing PDFs and that the pain we think we see is not sharp enough to change behaviour.

That is why we are running a [first cohort](/cra-sbom-attestation/for-suppliers/) rather than assuming the answer. Suppliers are free permanently, the cohort is small, and the question we are trying to settle is behavioural rather than technical.

If you are a manufacturer on the other side of this problem, [that is a different page](/cra-sbom-attestation/for-manufacturers/).
