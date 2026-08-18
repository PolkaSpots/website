---
title: "A current ISO 27001 certificate is not evidence that you are secure"
date: "2026-07-16"
excerpt: "We have found production databases on the open internet at companies holding current certifications. The certificate was not fraudulent. It was answering a different question from the one the buyer thought it answered."
seo_title: "ISO 27001 Is Not Evidence That You Are Secure"
meta: "We have found production databases open to the internet at companies holding current ISO 27001 certificates. The certificate answers a different question."
author: "Simon Morley"
tags: ["due-diligence", "iso-27001", "compliance", "private-equity", "m-and-a"]
slug: "a-current-certificate-is-not-security"
---

A recurring moment in deal work: the data room contains a current ISO 27001 certificate, the buyer treats the security question as closed, and we find something in the first afternoon that would have failed any reasonable definition of secure.

This is not a story about fraudulent certificates. The certificates are usually real, the audits usually happened, and the auditors usually did their job. The problem is that the certificate answers a question the buyer is not asking.

## What the certificate actually attests

Management-system certifications attest that you have a system for managing information security: that policies exist, that risks have been assessed and recorded, that controls have been selected with documented justification, and that the whole thing is reviewed on a cycle.

Every one of those is about process. None of them is a statement that a specific system, on a specific day, is not exploitable.

You can hold a valid certificate with a documented risk acceptance for the exact weakness that ends up breaching you. The acceptance is part of the system working as designed. Someone identified the risk, someone with authority accepted it, and it was recorded. The auditor's job was to check that this happened, not to overrule the judgement.

Scope compounds this. Certification scope is a defined boundary, and it is often narrower than the business. A certificate covering the primary SaaS platform tells you nothing about the acquired subsidiary still running its own stack, or the internal tooling, or the staging environment that happens to hold a copy of production data.

## What we find anyway

The fintech example we describe on the services page is representative rather than unusual: current certification, production database reachable from the public internet with default credentials. Nothing about the certification process was designed to catch that. No control in the applicable annex says "someone will attempt to connect to your database from outside".

The general pattern is that certification measures whether you have a system for thinking about security, and offensive testing measures what happens when someone attacks you. Both are worth having. They are not substitutes, and the failure mode in deal work is treating the cheaper one as though it covers the other.

## What this means for diligence

If you are buying, the certificate is a useful signal about organisational maturity. A company that has been through certification usually has someone accountable, some documentation, and some cadence. That is genuinely worth knowing.

It is not a substitute for someone attempting to break in. The two questions we would want answered before signing are what the certification scope actually covers, and what a competent attacker finds in the first week — because those are the two things a certificate cannot tell you and both are cheap to establish.

The uncomfortable version, which we say to buyers regularly: if the seller's security evidence consists entirely of certificates, you have learned that they can pass an audit. You have not learned whether their production database is on the internet. Those are different findings and only one of them repriced a deal.
