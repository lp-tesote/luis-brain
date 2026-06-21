---
title: AR Due by Status — 2026-05-12 snapshot
tags: [finance, receivables, cobros]
updated: 2026-05-12
status: draft
---

# AR Due by Status — 2026-05-12

Snapshot of accounts receivable, **excluding "Not Yet Due"**, split by collection status.

Source: AR aging sheet ([Google Sheet, gid 1571527824](https://docs.google.com/spreadsheets/d/1SYYywD-bMDcMOSPnnt-B_d9sI7IE1i2n3ofTiHjPnbw/edit?gid=1571527824)).

## Summary

| Status | # | Due (USD) | % of due |
|---|---:|---:|---:|
| Current | 46 | $86,090.98 | 67.1% |
| Doubtful | 4 | $19,885.00 | 15.5% |
| Pending confirmation | 7 | $18,168.58 | 14.2% |
| Uncollectible | 4 | $4,092.00 | 3.2% |
| **TOTAL DUE** | **61** | **$128,236.56** | 100% |

Reconciles to sheet: $166,600.56 grand total − $38,364.00 not-yet-due = **$128,236.56**.

Logic: "Doubtful", "Pending confirmation", and "Uncollectible" rows are 100% overdue by definition (a not-yet-due invoice can't already be doubtful/uncollectible), so all $38,364 NYD sits under Current rows.

## Read

- **Current ≠ healthy.** 46 customers carrying $86k of *overdue* invoices labeled Current. Biggest concentrations:
  - ROCKENBAUGH — $20,992 GT (with $12,996 in 91–120 bucket)
  - MOCASA — $12,499.98
  - La Innovación SAS — $8,500
  - Industria Láctea Torondoy — $6,000 (all Over 120)
- **Doubtful ($19,885)** is FORUM-heavy: $14,394 of the $19,885 sits with one customer. If FORUM slips to Uncollectible, bad-debt picture changes meaningfully.
- **Pending confirmation ($18,169)** is sales/CX hygiene — GRUPO UP ($5,395) + DIMASSI ($4,500) are the chunks; closing those moves dollars into a real bucket.
- **Uncollectible ($4,092)** is small but spread across 4 names. Candidate for batch write-off rather than continued carry.

## Status definitions (working assumption)

- **Current** — overdue but no collection issues flagged; standard cobros workflow applies
- **Doubtful** — collection at risk, not yet given up
- **Pending confirmation** — waiting on customer or internal confirmation (likely amount disputes or reconciliation gaps)
- **Uncollectible** — written-off candidates

## Next cuts worth doing

- Break Current down by aging bucket (1–30 / 31–60 / 61–90 / 91–120 / Over 120) to separate hygiene from at-risk
- Per-customer worst-offenders shortlist for cobros team
- Owner split (RDB vs LP) on Current to see workload distribution

## Related

- [[ar-and-cobros-2026-05]]
- [[ar-and-cobros-2026-05-team]]
- [[analysis-may-2026]]
