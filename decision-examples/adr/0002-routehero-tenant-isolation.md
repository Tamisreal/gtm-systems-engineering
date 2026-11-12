# ADR 0002: Tenant isolation in depth

- **Status:** accepted
- **Date:** 2026-09 (Phase 1 architecture)
- **Evidence status:** Design decision in a live application

## Context

RouteHero stores four classes of data with different sharing rules: public business facts (shared, free), licensed contact data (shared storage, gated by entitlement), tenant-private data (status, notes, scores) and, later, network-shared data. Two hood cleaners in the same city are competitors. One seeing the other's notes or won accounts would end the product.

## Business objective

Zero cross-tenant data exposure, while still buying each public record once.

## Options considered

| Option | Isolation | Cost to run | Weakness |
|---|---|---|---|
| Database per tenant | Strong | High, and the shared graph is lost | Re-buys every overlapping record |
| Application checks only | One layer | Low | One missed `WHERE tenant_id` leaks data |
| Shared database, three independent layers | Strong | Low | More care in every query path |

## Chosen approach

Three layers, any one of which failing must not cause a leak:

1. **Application:** every request resolves a tenant context; every repository function takes `tenantId` as a required first argument with no default.
2. **Postgres row-level security** with `FORCE` on every tenant-scoped table, compared against a per-transaction setting. The app connects as a role that cannot bypass RLS.
3. **Transaction-scoped setting** (`set_local`, not `set`). With a pooler in transaction mode, a session-level setting outlives the request and the next tenant inherits it.

Canonical tables (locations, organizations) have no tenant id by design. Licensed fields are reachable only through views that join the entitlement table.

## Tradeoffs

Every tenant-scoped query must run inside an explicit transaction. Geospatial reads go through hand-written SQL functions that must respect the same rules.

## Validation plan

An isolation test suite that runs queries as one tenant and asserts zero rows from another, run on every change to the data layer.

## Observed results

The isolation suite exists in the codebase. No production incident data yet.

## Reconsideration triggers

- An enterprise customer contractually requiring physical separation.
- Query patterns that RLS makes too slow at real volume.
