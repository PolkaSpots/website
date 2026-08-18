---
title: "What security due diligence should tell an investment committee"
date: "2026-08-06"
excerpt: "Not a severity distribution. Three things: does this change the price, does this change the plan, and what does it cost to fix. If the report cannot answer those, it was written for the wrong reader."
seo_title: "What Diligence Should Tell an Investment Committee"
meta: "Security due diligence should answer three questions: does this change the price, does it change the plan, and what does remediation cost?"
author: "Simon Morley"
tags: ["due-diligence", "private-equity", "venture-capital", "m-and-a", "reporting"]
slug: "what-diligence-should-tell-an-investment-committee"
---

Most technical security due diligence reports are written for engineers and delivered to investors. The result is a document with a severity histogram, a CVSS table, and a hundred pages of appendix, handed to a committee that needs to make a decision in a meeting.

The committee is not asking what the CVSS score was. It is asking three questions, and a report that does not answer them directly has failed regardless of how good the underlying testing was.

## Does this change the price?

The only findings that belong in an executive summary are the ones with a number attached.

A finding changes the price when remediating it costs real money, when it implies a liability that has already been incurred, or when it reveals that something represented in the data room is not true. Everything else is operational detail that belongs in the technical annex and nowhere near the first page.

The difference matters because most reports invert it. Twelve medium-severity findings get equal billing with the one thing that actually matters — that the seller described an architecture they do not have, or that customer data has been accessible for long enough that notification obligations may already exist.

## Does this change the plan?

Some findings do not move the price but do change what the first hundred days look like.

If the platform cannot support the integration you have modelled without significant rework, that is a diligence finding even though nothing is exploitable. If there is exactly one person who understands the deployment pipeline and they are not staying, that is a security finding in every practical sense. If the roadmap assumes a multi-tenant capability the current isolation model cannot deliver safely, the committee needs to know before the synergy case is signed off.

These rarely appear in security reports because they are not vulnerabilities. They are the things that determine whether the plan survives contact with the asset.

## What does it cost to fix?

An estimate, in money and elapsed time, with an ordering.

This is the part most often missing and the easiest to supply. We already know what the remediation involves, because we found it and we have fixed things like it before. Withholding that and leaving the buyer to obtain a second opinion on the cost of the first opinion serves nobody.

An estimate that is wrong by thirty percent is enormously more useful than no estimate, because it lets the number be built into the deal. "Critical: unauthenticated admin access" with no cost attached becomes a negotiation about vibes. "Critical: unauthenticated admin access, roughly three engineer-weeks, can be done before close" becomes a line item.

## What the annex is for

None of this argues for less technical depth. The full detail — methodology, evidence, reproduction steps, severity reasoning — should all be there, because the target's engineers need it to act and because a serious buyer's own technical people will want to check the work.

It just should not be the first thing the committee reads. Two pages that answer the three questions, then everything else behind it for the people who need it.

## The test

Before a report goes out we ask whether a partner could read the first two pages, walk into a meeting, and defend a position on the deal. If the answer is no, the report is not finished, however thorough the testing was.
