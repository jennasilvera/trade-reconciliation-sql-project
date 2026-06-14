# Reconciliation Tolerance Policy

This document explains how tolerance rules could be applied to reconciliation breaks in the Trade Reconciliation SQL Project.

All data is simulated.

---

## Purpose

Not every difference between internal and broker records has the same operational impact.

Some breaks require immediate escalation, while others may be caused by rounding, fee calculation differences, or timing differences.

This tolerance policy explains how reconciliation exceptions could be prioritized.

---

## Exact Match Fields

The following fields should generally match exactly:

| Field | Reason |
|---|---|
| execution_id | Primary reconciliation key |
| symbol | Identifies the traded instrument |
| side | Determines buy/sell direction |
| trade_date | Determines execution date |
| account_id | Determines allocation account |

Breaks in these fields are usually higher priority because they can affect positions, exposure, or account-level accuracy.

---

## Tolerance-Based Fields

The following fields may use tolerance thresholds:

| Field | Example Tolerance | Reason |
|---|---:|---|
| price | 0.01 | Small price differences may be rounding or average price differences |
| fees | 0.05 | Small fee differences may come from rounding or broker fee adjustments |
| commission | 0.05 | Commission differences may be due to calculation timing |
| gross_amount | 1.00 | Small notional differences may be rounding-related |
| allocation_pct | 0.0001 | Allocation percentage may have decimal precision differences |

---

## Suggested Severity Rules

| Break Type | Suggested Severity |
|---|---|
| Missing broker trade | High |
| Missing internal booking | High |
| Side mismatch | High |
| Symbol mismatch | High |
| Quantity mismatch | Medium to High |
| Price mismatch above tolerance | Medium |
| Fee mismatch above tolerance | Low to Medium |
| Settlement date mismatch | Medium |
| Allocation account mismatch | Medium |
| Duplicate trade | Medium |

---

## Example Price Tolerance Logic

A price break could be classified only when the absolute price difference exceeds a threshold.

Example:

```sql
WHERE ABS(internal_price - broker_price) > 0.01
