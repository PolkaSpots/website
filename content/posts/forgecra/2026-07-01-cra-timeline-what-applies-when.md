---
title: "The CRA timeline: what actually applies, and when"
date: "2026-07-01"
excerpt: "Article 14 reporting starts 11 September 2026. Everything else — SBOM, vulnerability handling, technical documentation — lands 11 December 2027. The gap between those two dates is where most of the confusion lives."
meta: "CRA Article 14 reporting starts 11 September 2026; SBOM, vulnerability handling and technical documentation land 11 December 2027. No size exemption."
author: "Simon Morley"
tags: ["cra", "cyber-resilience-act", "sbom", "compliance-timing", "eu"]
slug: "cra-timeline-what-applies-when"
---

The Cyber Resilience Act (Regulation (EU) 2024/2847) entered into force in December 2024, and its obligations arrive in stages. Most of the confusion we hear in conversations comes from collapsing those stages into a single deadline. They are not the same, they do not require the same work, and conflating them is how you end up buying the wrong thing.

Here is the sequence as we read it. This is our reading for planning purposes, not legal advice.

## 11 September 2026 — reporting obligations

Article 14 reporting applies from this date. If you become aware of an actively exploited vulnerability in your product, or a severe incident affecting its security, you notify. The clocks are short: an early warning within 24 hours, a fuller notification within 72 hours, and a final report within 14 days.

Two things follow from that.

First, this obligation is **event-triggered**. Nothing happens on 11 September 2026 unless something happens to you. There is no filing, no submission, no certificate. If you ship nothing and nothing is exploited, the date passes without incident.

Second, satisfying it is largely an operational and organisational problem, not a tooling one. You need someone who owns the clock, a decision path for what counts as reportable, and a route to submit. A spreadsheet and a named person will get most mid-market manufacturers through it.

This is why we do not sell readiness for this date. It is a real obligation, it is worth preparing for, and it is not where the hard work is.

## Late 2026 to mid 2027 — harmonised standards

As of August 2026, **no harmonised standards for the CRA have been cited in the Official Journal**. That matters more than it sounds.

Until standards are cited, there is no presumption of conformity. You cannot point at a standard, demonstrate you followed it, and be presumed compliant with the corresponding essential requirement. You are left interpreting Annex I directly and documenting your reasoning.

The practical consequence is that "we're waiting for the standards" is a coherent position for some decisions and an expensive one for others. Waiting to finalise your conformity assessment route is reasonable. Waiting to start collecting component evidence from forty suppliers is not, because that work takes months regardless of what the standards eventually say.

## 11 December 2027 — full obligations

This is the date that actually changes what you have to build.

From here, products with digital elements placed on the EU market have to meet the essential requirements in Annex I. That includes the security properties themselves, and — the part most people underestimate — the vulnerability handling requirements in Annex I Part II. Those require, among other things, that manufacturers identify and document the components in their products, including by drawing up a software bill of materials in a commonly used machine-readable format covering at the very least the top-level dependencies.

You also need technical documentation that demonstrates conformity, and you need to keep it current for the support period.

There is **no size exemption**. Microenterprises and SMEs get some procedural relief in places, but the essential requirements apply to a fifteen-person hardware company the same way they apply to a large one.

## 2028 and beyond

Support-period duties continue, market surveillance authorities become active, and the question stops being "did you produce the documentation" and becomes "is it still true". Continuous evidence is a different operational problem from one-time documentation, and most of the tooling conversation today has not caught up with it.

## Why we describe it this way

The commercial temptation is to point at September 2026, describe it as a cliff, and sell against the fear. We are not going to do that, for two reasons.

The first is that it is not accurate. It is an event-triggered reporting duty, not a filing deadline.

The second is that it produces bad decisions. If you buy tooling in a panic in August 2026 to satisfy a reporting obligation, you will very likely buy something that does not help you at all with the December 2027 requirement to evidence what is actually inside your products — which is the harder problem, takes longer, and depends on companies you do not control.

Start on the supplier evidence now. Not because a deadline is close, but because the work is slow and the deadline is fixed in law.
