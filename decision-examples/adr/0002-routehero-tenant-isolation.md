# ADR 0002: Tenant isolation in depth

- **Status:** accepted
- **Date:** 2026-09 (Phase 1 architecture)

## Context

RouteHero stores four kinds of data, each with its own sharing rules:

- Public business facts: shared with everyone, free.
- Paid contact data: stored once, shown only to customers who have paid for it.
- Each customer account's private data: status, notes, scores.
- Later, data customers choose to share with the network.

Two hood cleaning companies in the same city are competitors. If one could see the other's notes or won accounts, the product would be finished.

## Business objective

No customer ever sees another customer's data, while each public record is still bought only once.

## Options considered

| Option | How well data stays separate | Cost to run | Weakness |
|---|---|---|---|
| A separate database for each customer account | Strong | High, and the shared master list is lost | Buys every overlapping record again for each customer |
| Checks in the app only | One safeguard | Low | One forgotten customer filter (`WHERE tenant_id`) leaks data |
| One shared database, three independent safeguards | Strong | Low | Every way of reading data needs more care |

## Chosen approach

Three safeguards. If any one of them fails, the other two must still stop a leak:

1. **Application:** every request first works out which customer account it belongs to. Every function that reads or writes data must be given the customer account (`tenantId`) as its first input, with no default value.
2. **Postgres row-level security:** the database itself blocks one customer from seeing another's data. This is switched on and forced (`FORCE`) on every table that holds customer data. The database compares each row against a customer setting made for that one request. The app logs in as a user that cannot switch this protection off (RLS).
3. **Customer setting that expires after each request** (`set_local`, not `set`). The app shares database connections between requests (a "pooler"). A setting that lasted the whole connection would carry over to the next request, and the next customer would get the previous customer's access.

The shared master tables (locations, organizations) have no customer field on purpose, because everyone shares them. Paid contact fields can only be read through views that first check whether the customer has paid for them.

## Tradeoffs

Every read or write of customer data must be wrapped in an explicit transaction (one bundled unit of database work). Map-based searches use hand-written database functions (SQL) that must follow the same rules.

## Validation plan

A set of isolation tests that query the data as one customer and confirm zero rows come back from any other customer. They run on every change to the data code.

## Observed results

The isolation tests exist in the codebase. No data from real-world incidents yet.

## Reconsideration triggers

- A large customer whose contract requires its data on physically separate machines.
- Searches that the database's per-row protection (RLS) makes too slow at real volume.
