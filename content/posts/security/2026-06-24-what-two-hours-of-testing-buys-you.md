---
title: "What two hours of testing actually buys you"
date: "2026-06-24"
excerpt: "A Flash Review is not a pentest and we do not pretend otherwise. Here is what fits in two hours, what does not, and why the constraint produces better results than it sounds like it should."
meta: "A £500 Flash Review is not a pentest. Here is exactly what fits in two hours, what does not, and why the constraint produces a more honest answer."
author: "Simon Morley"
tags: ["penetration-testing", "flash-review", "methodology", "attack-surface"]
slug: "what-two-hours-of-testing-buys-you"
---

We sell a £500, two-hour security review with a refund if we find nothing worth worrying about. The reasonable first reaction is that two hours is not enough time to do anything useful. That is half right, and the half that is wrong is worth explaining.

## What two hours is not

It is not a penetration test. A real engagement against a moderately complex application is one to two weeks, because most of that time goes into understanding the system well enough to reason about its business logic — who is allowed to do what, which of those rules are enforced server-side, and where the model breaks under an unexpected sequence of requests. You cannot compress that.

It is not coverage. We are not going to touch every endpoint, every role, or every integration. Anyone offering you comprehensive assurance in two hours is selling you a scan with a nicer cover page.

It is not a compliance artefact. It will not satisfy an auditor and it is not designed to.

## What it is

Two hours is enough time to answer one specific question honestly: **if a competent attacker spent an afternoon on you, would they get somewhere?**

That question is answerable because attackers are not comprehensive either. They are opportunistic. They look at what is exposed, they look for the cheap wins, and they escalate from whatever they find first. The first two hours of a real attack and the first two hours of our review look substantially alike.

In practice that time goes into enumeration and the fast paths. What is actually exposed, versus what you think is exposed. Subdomains nobody remembers owning. Staging environments reachable from the internet. Admin interfaces at predictable paths. Object references that increment. Authentication that is checked in the UI and not on the API. Credentials and keys in places they should not be — public repositories, JavaScript bundles, error responses.

None of that is clever. That is the point. The things that get companies breached are usually not clever.

## Why the constraint helps

A fixed two hours forces prioritisation in a way an open-ended engagement does not. There is no time to write up theoretical risk, so we do not. There is no time to pad a report to justify a day rate, so we do not. You get what we actually found, what it means, and what to do about it, because that is all there is time to produce.

The refund does the same job from the other direction. If your public surface is genuinely tight, we do not get paid, which means we are not incentivised to dress up a low-severity finding as something it is not. That has happened and we refunded, and it was a better outcome than the alternative — you got a straight answer and we did not spend a client's money manufacturing concern.

## When you want the longer engagement instead

If the answer you need is "are we secure" rather than "is anything obviously wrong," you want the full engagement. Specifically, go longer when the risk is concentrated in business logic rather than configuration: multi-tenant systems where the interesting question is cross-tenant isolation, anything moving money, anything with a complex permissions model, anything where the failure mode is regulatory rather than embarrassing.

Go longer, too, when you are about to buy the company. A two-hour read on an acquisition target is a useful smoke test and a bad basis for a decision with eight figures attached.

## The honest summary

Two hours buys you a fast, real answer to a narrow question, delivered by someone who has been doing this for twenty years, with no obligation to buy anything else. It does not buy you assurance. We would rather say that plainly than let you infer otherwise and be disappointed later.
