# Exception Lifecycle and SLA Guide

This document explains how reconciliation breaks are converted into an operational exception queue.

All data is simulated.

---

## Purpose

The exception lifecycle report turns raw reconciliation breaks into a review queue with:

- Exception ID
- Source report
- Execution ID
- Exception type
- Severity
- Owner queue
- SLA hours
- Status
- Age in days
- Generated timestamp
- Resolution notes

The output file is:

    data/reports/exception_lifecycle_report.csv

---

## Why This Matters

In a trading operations or production support workflow, identifying a break is only the first step.

The team also needs to know:

- How urgent the break is
- Which team should review it
- Whether it is open or resolved
- Whether it is approaching SLA breach
- What notes were added during investigation

---

## Severity Rules

| Severity | SLA Hours | Example Break Types |
|---|---:|---|
| HIGH | 4 | Missing internal booking, missing broker trade, side mismatch, symbol mismatch |
| MEDIUM | 24 | Quantity mismatch, price mismatch, settlement date mismatch, allocation mismatch, duplicate trade |
| LOW | 48 | Fee mismatch |

---

## Owner Queue Rules

| Exception Type | Owner Queue |
|---|---|
| MISSING_BROKER_TRADE | Broker Operations |
| MISSING_INTERNAL_BOOKING | Trade Support |
| SIDE_MISMATCH | Trade Support |
| SYMBOL_MISMATCH | Security Master / Trade Support |
| QUANTITY_MISMATCH | Trade Support |
| PRICE_MISMATCH | Trade Support |
| SETTLEMENT_DATE_MISMATCH | Settlements |
| ALLOCATION_ACCOUNT_MISSING_AT_BROKER | Allocations |
| ALLOCATION_ACCOUNT_MISSING_INTERNALLY | Allocations |
| DUPLICATE_INTERNAL_TRADE | Data Operations |
| DUPLICATE_BROKER_TRADE | Broker Operations |
| FEE_MISMATCH | Fees / Commissions |

---

## Lifecycle Status

The current simulated lifecycle report defaults all exceptions to:

    OPEN

In a future version, possible statuses could include:

| Status | Meaning |
|---|---|
| OPEN | Break has been detected and needs review |
| IN_REVIEW | Analyst is investigating the break |
| ESCALATED | Break has been escalated to another team |
| RESOLVED | Break has been corrected or explained |
| CLOSED_NO_ACTION | Break was reviewed and no action was required |

---

## How to Generate the Report

Run:

    make lifecycle

Or run the full workflow:

    make check

---

## Interview Explanation

A concise way to explain this feature:

I added an exception lifecycle report to make the reconciliation workflow more operational. Instead of only exporting raw breaks, the project now classifies each exception by severity, assigns an owner queue, adds SLA hours, and tracks status fields. This models how reconciliation exceptions could become a daily operations review queue.
