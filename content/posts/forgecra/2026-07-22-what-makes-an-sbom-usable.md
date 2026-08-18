---
title: "Most SBOMs we see are not usable. Here is what is missing."
date: "2026-07-22"
excerpt: "A file that parses is not the same as evidence you can rely on. The common failures are missing version precision, no unique identifiers, no dependency relationships, and no statement of who produced it or when."
seo_title: "Most SBOMs Are Not Usable. Here Is What Is Missing."
meta: "An SBOM that parses is not evidence. The usual failures: imprecise versions, no purls or CPEs, no dependency relationships, no author or timestamp."
author: "Simon Morley"
tags: ["sbom", "cyclonedx", "spdx", "cisa-minimum-elements", "supply-chain", "cra"]
slug: "what-makes-an-sbom-usable"
---

There is a gap between having an SBOM and having evidence. Plenty of organisations have crossed the first line and think they have crossed the second.

The test we apply is simple. If a customer, an auditor, or a market surveillance authority asked you a specific question about a component in a product you shipped eighteen months ago, could you answer it from what you hold? Most of the SBOMs we look at fail that test, and they fail it in a small number of repeated ways.

## The baseline: CISA minimum elements

The US CISA minimum elements remain the most widely used shared floor, and they are a reasonable scoring baseline even for EU work. They ask for supplier name, component name, version of the component, other unique identifiers, dependency relationship, author of the SBOM data, and a timestamp.

That list looks unambitious until you check real files against it.

## Where they actually fail

**Version precision.** "1.2" is not a version. "1.2.x", "latest", and "current release" are not versions. If the string does not resolve to exactly one artefact, you cannot answer whether you are affected when an advisory lands, which is the entire point.

**No unique identifiers.** A component name and a version, with no purl and no CPE, means matching against vulnerability data is string comparison and guesswork. This is the single highest-value field to fix and the most commonly absent.

**Flat component lists with no relationships.** A list tells you what is present. It does not tell you what depends on what, which means it cannot tell you whether a vulnerable library is reachable, bundled, or vendored three levels down. The CRA language about top-level dependencies is a floor, not a target.

**No author or timestamp.** An SBOM with no statement of who generated it and when is not evidence of anything. It cannot be shown to correspond to a particular build, and it cannot be shown to be current.

**Generated once, at the wrong time.** An SBOM produced by hand at the point someone asked for it describes a moment that has already passed. Component sets change. If the document is not regenerated when the build changes, it decays from the day it is written.

## Format is the easy part

CycloneDX and SPDX are both fine. They are both commonly used and machine-readable, which is what the regulation asks for, and converting between them for most practical purposes is tractable.

We mention this because format is where conversations often start and it is rarely where the problem is. A well-populated CycloneDX file and a well-populated SPDX file are both useful. A sparse one in either format is not. Arguing about the container while the contents are thin is a way of feeling productive.

## Scoring, not pass or fail

We score submissions rather than accepting or rejecting them, because a binary gate produces the wrong behaviour on both sides. A supplier who fails a gate stops engaging. A manufacturer with a stack of "pass" results learns nothing about which of their suppliers are actually reliable.

A score tells a manufacturer where to spend attention: these four suppliers are producing evidence you can act on, these eleven are producing files that will not help you when an advisory lands. That is a workable prioritisation. "Fourteen of fifteen suppliers responded" is not.

## What this means if you are a supplier

The good news is that most of the failures above are cheap to fix once, in your build pipeline, and then they stay fixed. Generating from the build rather than by hand solves the timestamp, author and precision problems simultaneously. Adding purls is usually a configuration change rather than a project.

The reason this is worth doing is not that a regulator will ask you directly. In many cases they will not — your customers will, repeatedly, in their own formats, and the quality of what you send determines how many follow-up questionnaires you receive.
