# Reconciliation Controls Matrix

This document maps each reconciliation control to the break it detects, the expected severity, the output report, and the likely operational follow-up.

All controls use simulated data.

---

## Controls Overview

| Control ID | Control Name | Break Type Detected | Severity | Output Report | Follow-Up Action |
|---|---|---|---|---|---|
| CTRL-001 | Missing Broker Trade Check | Missing broker trade | High | `trade_exceptions.csv` | Confirm broker file completeness and escalate missing confirmation |
| CTRL-002 | Missing Internal Booking Check | Missing internal booking | High | `trade_exceptions.csv` | Review trade capture process and determine whether manual booking is needed |
| CTRL-003 | Quantity Reconciliation Check | Quantity mismatch | Medium | `trade_exceptions.csv` | Compare internal and broker quantities; validate source of truth |
| CTRL-004 | Price Reconciliation Check | Price mismatch | Medium | `trade_exceptions.csv` | Check execution price, average price, and notional impact |
| CTRL-005 | Side Reconciliation Check | Side mismatch | High | `trade_exceptions.csv` | Escalate quickly due to position and exposure impact |
| CTRL-006 | Symbol Reconciliation Check | Symbol mismatch | High | `trade_exceptions.csv` | Validate security mapping and correct symbol discrepancy |
| CTRL-007 | Fee Reconciliation Check | Fee mismatch | Low to Medium | `trade_exceptions.csv` | Review commission, exchange fee, and net amount impact |
| CTRL-008 | Settlement Date Check | Settlement date mismatch | Medium | `trade_exceptions.csv` | Validate settlement convention and correct downstream records |
| CTRL-009 | Duplicate Internal Trade Check | Duplicate internal trade | Medium | `duplicate_trade_exceptions.csv` | Check for duplicate ingestion or duplicate manual booking |
| CTRL-010 | Duplicate Broker Trade Check | Duplicate broker trade | Medium | `duplicate_trade_exceptions.csv` | Check for duplicate broker file records |
| CTRL-011 | Allocation Account Check | Allocation account mismatch | Medium | `allocation_exceptions.csv` | Validate account-level allocation records |
| CTRL-012 | Reconciliation Summary Check | Exception aggregation | Informational | `reconciliation_summary.csv` | Summarize daily exception volume by break type |

---

## Control Design Principles

The reconciliation controls are designed to be:

- Repeatable
- SQL-driven
- Easy to review
- Easy to export into CSV reports
- Clear enough for operational follow-up
- Based on simulated but realistic trade lifecycle issues

---

## Severity Framework

| Severity | Meaning |
|---|---|
| High | Could materially affect position, exposure, settlement, or trade capture accuracy |
| Medium | Requires review and correction but may not immediately block trade processing |
| Low | Usually fee, rounding, or minor reporting discrepancy |
| Informational | Used for monitoring and summary reporting |

---

## How This Supports Trading Operations

This control matrix shows how the project maps technical SQL logic to operational risk management.

A trading operations analyst does not only need to find mismatches. They also need to understand:

- Why the break matters
- How urgent the break is
- Which report shows the break
- What investigation step should follow
- Whether the issue should be escalated

---

## Interview Explanation

A concise way to explain this document:

> I added a reconciliation controls matrix to connect each SQL check to an operational control. It shows the break type, severity, report output, and likely follow-up action. This helped me frame the project as a trading operations control process rather than only a data analysis script.
