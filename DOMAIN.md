# Domain decision record — ForgeCRA

**Status:** decided, 19 August 2026. Review at the trigger below, not before.

## Decision

ForgeCRA lives at `polkaspots.com/cra-sbom-attestation/`. `forgecra.com` is owned and
parked. Nothing is being migrated.

## Why

**Deliverability.** The Phase 0 motion is ~30 outbound conversations sent from
`polkaspots.com` mailboxes. That domain was registered in 2005 and has two decades of
sending reputation. A domain registered this year, mailing cold prospects about a
regulatory deadline, is close to the textbook profile of a phishing campaign — the
filtering outcome is predictable and it would be self-inflicted.

**Reputation transfer.** ForgeCRA is pre-product and has no track record of its own. Sitting
under a company that has been doing network and security work since 2005 is the only
credibility available at this stage. A standalone domain with a new product on it discards
that and starts from zero.

**Search.** The existing domain has accumulated authority. A new domain would spend the
whole validation window earning the right to be indexed at all.

**Cost of being wrong is asymmetric.** Staying is reversible with a redirect map. Launching
on a cold domain, discovering deliverability is poor, and moving back is not.

## Trigger for moving to forgecra.com

Move when **either**:

1. A paying pilot converts to a platform contract — the product then has its own revenue and
   its own reference customers, and no longer needs to borrow credibility; or
2. The entity is spun out, or takes outside investment that requires a separate cap table.

Do not move for aesthetic reasons, and do not move mid-campaign. Warm the new domain for at
least 30 days of sending before any cold outbound goes from it.

## Consequence to manage now

Every URL published under `/cra-sbom-attestation/` becomes a redirect liability the moment a
move happens. Every outbound link, every LinkedIn ad, every citation in a blog post is a
301 that has to be maintained indefinitely.

Mitigations already in place, and worth preserving:

- **The path structure is shallow and stable.** Four URLs, one level deep:
  ```
  /cra-sbom-attestation/
  /cra-sbom-attestation/for-manufacturers/
  /cra-sbom-attestation/for-suppliers/
  /cra-sbom-attestation/blog/<slug>/
  ```
  A future migration is a clean prefix swap, not a per-page mapping exercise.

- **Do not deepen it.** No `/cra-sbom-attestation/2026/q3/campaign-b/`. Every extra level is
  another redirect rule and another chance to lose a link.

- **`_redirects` already carries the history.** `/forgecra/*` still 301s to the current
  paths. When the move happens, the same file gains a prefix rule and the old paths keep
  working. Do not delete historical redirect rules — they are cheap and links live forever.

- **Canonicals are absolute** (`https://polkaspots.com/...`), so a migration means changing
  `ORIGIN` in `tools/engine.py` and rebuilding. One constant, not a find-and-replace.
