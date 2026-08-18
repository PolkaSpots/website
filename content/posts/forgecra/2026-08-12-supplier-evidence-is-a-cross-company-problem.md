---
title: "Supplier evidence is a cross-company problem"
date: "2026-08-12"
excerpt: "Binary analysis of firmware you already hold is well served by good vendors. Getting evidence out of forty companies that do not report to you is a different problem, and it is the one nobody owns."
meta: "Binary analysis of firmware you hold is solved. Getting current SBOMs out of forty companies that don't report to you is a different problem entirely."
author: "Simon Morley"
tags: ["sbom", "supply-chain", "cra", "supplier-management", "attestation"]
slug: "supplier-evidence-is-a-cross-company-problem"
---

There are two problems that get called "SBOM" and they are not the same problem.

The first is: *I have a firmware image and I want to know what is inside it.* This is a technical problem, it is well understood, and there are capable vendors solving it. Binary composition analysis works. If you hold the artefact, you can find out a great deal about it without anyone's cooperation.

The second is: *I need current, structured, trustworthy component evidence from forty companies that do not work for me.* This is not a technical problem. It is a coordination problem wearing a technical costume, and the tooling built for the first problem does not touch it.

We only work on the second one.

## Why analysis does not close the gap

Analysis tells you what is in the binary you have. It cannot tell you what changed in a supplier's next release, it cannot produce an attestation the supplier is willing to stand behind, and it cannot help at all where you never receive an artefact to analyse in the first place — which is common with subassemblies, licensed modules, and anything where the supplier ships you a black box.

More fundamentally, an inferred component list is not the same artefact as a supplier's signed statement about their own product. When the question is "what did your supplier tell you, and when," a scan result is not the answer to that question. It is a useful cross-check on the answer.

## Why the obvious solution does not scale

The obvious solution is a portal. The manufacturer stands one up, invites their suppliers, and collects.

This works at ten suppliers and degrades badly after that, for a reason that has nothing to do with the software. Every manufacturer builds their own portal. Every supplier then has an account in five portals, each with a different schema, a different questionnaire and a different review cycle. The supplier's cost scales with the number of customers, and the supplier is the party with no regulatory exposure and no incentive to absorb that cost.

What happens next is predictable. Suppliers deprioritise it. Responses get thin, then late, then stop. The manufacturer, who does carry the exposure, is left chasing.

## The shape of the answer

The pattern that resolves this is not new, and it is not ours. E-invoicing went through the same thing: many-to-many relationships, per-partner integration cost growing quadratically, and eventually a neutral network in the middle that everyone connects to once.

Applied here, it means one attestation from the supplier, published once, shared per customer under the supplier's control. The supplier's cost stops scaling with customer count. The manufacturer gets structured, scored, current evidence. Neither party has to trust a competitor with their component data, which is the reason this has to sit with someone neutral rather than inside an analysis vendor's platform.

That neutrality is load-bearing. A supplier will not attest deeply into a system owned by a company that also sells analysis to their customers, and it is not irrational of them to refuse.

## The part we do not know yet

Everything above is a thesis, not a result. The load-bearing assumption is that suppliers will publish into a neutral exchange when they will not fill in five portals. We think that is true. We have not proved it.

That is why we are running paid pilots by hand before building a platform, and why the supplier side is free permanently — charging the side that creates the network value is how you kill the network before it exists. If it turns out suppliers are content to keep emailing PDFs, we would rather learn that from thirty conversations than from a year of engineering.

If you are a supplier being asked for the same evidence by several customers, we would genuinely like to hear how you are handling it now — including if the answer is that you are not.
