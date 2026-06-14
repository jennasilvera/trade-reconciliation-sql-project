# Break Investigation Runbook

This runbook explains how to investigate each simulated reconciliation break in the Trade Reconciliation SQL Project.

The goal is to model how a trading operations analyst might review daily exceptions, determine the likely cause, and decide the next operational action.

All data in this project is simulated.

---

## 1. Missing Broker Trade

### Definition

A trade exists in the internal trade booking file but does not appear in the broker trade file.

### Possible Causes

- Broker file was delayed or incomplete
- Trade was booked internally but not confirmed by broker
- Execution ID mismatch between systems
- Trade was cancelled externally but not updated internally
- Internal system created a booking before broker confirmation arrived

### Investigation Steps

1. Search for the internal `execution_id`.
2. Confirm that the trade exists in `internal_trades`.
3. Search for the same `execution_id` in `broker_trades`.
4. Check whether symbol, trade date, side, and quantity suggest a near match under a different execution ID.
5. Review whether the trade should be escalated as a missing broker confirmation.

### Example SQL

```sql
SELECT *
FROM internal_trades
WHERE execution_id = 'EXEC_ID_HERE';

SELECT *
FROM broker_trades
WHERE execution_id = 'EXEC_ID_HERE';
