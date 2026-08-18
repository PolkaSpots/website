---
title: "Why the hard part of CRA is not generating an SBOM"
seo_title: "Generating an SBOM Is the Easy Part of the CRA"
meta: "CRA SBOM tooling generates bills of materials well. It cannot make a reluctant supplier send better data, and it produces no supplier attestation trail."
date: "2026-06-18"
excerpt: "Binary analysis turns a firmware image into an SBOM, and does it well. It cannot make a reluctant supplier send you better data next month, and it cannot produce an attestation that the supplier stands behind."
author: "Simon Morley"
tags: ["cra", "sbom", "cyber-resilience-act", "supplier-sbom", "binary-analysis", "supply-chain-security"]
slug: "cra-sbom-generation-is-not-the-hard-part"
key_points:
  - "SBOM *generation* from a binary or a build is largely a solved problem, with capable vendors serving it."
  - "SBOM *collection* from suppliers who do not report to you is not solved, and it is the obligation the CRA actually places on you."
  - "Under the Cyber Resilience Act the manufacturer placing the product on the EU market owns the evidence chain, including the parts written by someone else."
  - "Analysis of a binary you hold produces no supplier attestation, so it cannot show who asserted what, or when."
faq:
  - q: "Does the CRA require an SBOM?"
    a: "Yes. Annex I Part II requires manufacturers to identify and document components, including by drawing up a software bill of materials in a commonly used machine-readable format covering at the very least the top-level dependencies. Those obligations apply from 11 December 2027."
  - q: "Can I satisfy the CRA by scanning my own firmware?"
    a: "Scanning tells you what is in an artefact you already hold, which is genuinely useful. It does not produce evidence that a supplier attested to the accuracy of their own component data, and it cannot cover components where you never receive an analysable artefact."
  - q: "Who is responsible under the CRA when the software comes from a supplier?"
    a: "The manufacturer placing the product on the EU market carries the obligation. Responsibility for the evidence chain does not transfer upstream, even when most of the software originates there."
  - q: "Do I still need a binary analysis platform?"
    a: "If you already have one, keep it. It answers a different question well. The gap for most mid-market manufacturers is upstream collection and attestation, not analysis of what they already hold."
---

Most of the tools in this space are very good at one thing: turning a firmware image or a build into a software bill of materials. That problem is largely solved.

The problem that is not solved is getting trustworthy SBOMs from the people who actually supply the components.

## The obligation does not move upstream

Under the [Cyber Resilience Act](/cra-sbom-attestation/), the manufacturer who places the product on the EU market carries the obligation. That manufacturer is responsible for the evidence chain even when large parts of the software come from upstream suppliers.

There is no mechanism by which that responsibility transfers to the company that wrote the code. You can contract for cooperation, and you should, but the regulator's counterparty is you.

## What that looks like in practice

Ask twenty suppliers for a bill of materials and the responses sort themselves into a familiar pattern:

- Some suppliers send nothing.
- Some send a spreadsheet from two years ago.
- Some send a partial SBOM that is missing versions, hashes, or vulnerability context.
- Almost none of them want to fill in a different questionnaire for every customer.

None of these are unreasonable behaviours on the supplier's part. They carry no regulatory exposure for your product, and each additional customer format is pure cost to them. The incentive gradient runs against you, and no amount of chasing changes that.

## What binary analysis does and does not do

Binary analysis platforms — ONEKEY, Finite State and others — can generate an SBOM from the binary you already hold. That is useful, they do it well, and if you have one we would not suggest replacing it.

What it does not do is make a reluctant supplier send you better data next month. And it does not create an audit trail showing that the supplier attested to the accuracy of what they provided.

That second point is the one that gets underestimated. An inferred component list and a signed supplier statement are different artefacts answering different questions. When a customer, auditor or market surveillance authority asks *what did your supplier tell you, and when*, a scan result is a cross-check on the answer, not the answer itself.

There is also a coverage limit. Analysis needs an artefact. Subassemblies, licensed modules and anything delivered as a black box produce nothing to analyse, and those are exactly the relationships where you have least visibility already.

## The durable work

The durable work under the CRA is therefore less about "can we generate an SBOM" and more about "can we systematically collect, quality-score, and keep current the evidence that sits outside our own organisation."

Each of those three verbs is doing work:

**Collect** — structured requests to suppliers who have no obligation to you, chased on a cadence, tracked so you know who has not replied.

**Quality-score** — because a response is not the same as usable evidence. A file that arrives without precise versions or unique identifiers cannot answer the question you will eventually need to ask of it.

**Keep current** — component sets change with every release. A bill of materials produced once decays from the day it is written, and the CRA support-period duties run for years.

That is a network and workflow problem, not a scanning problem. It is the only part [ForgeCRA](/cra-sbom-attestation/) is focused on, and it is why we describe ourselves as complementary to the analysis vendors rather than competitive with them.

If you are on the other side of this — a supplier being asked for the same evidence by several customers in several formats — [that problem has its own page](/cra-sbom-attestation/for-suppliers/).
