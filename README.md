# blockbusters-rental-manager
#### Video Demo: URL

## Description

A CLI rental management system for a Blockbuster-style game store. The program gives a single employee operator tools to manage game inventory, create member accounts, and process rentals, returns, and fee payments — all enforced by a defined set of business rules.

The system is a rough approximation of how Blockbuster operated, not an attempt at historical accuracy. The scope is limited to core game rental operations. Authentication, concurrency handling, audit logging, and a GUI are all intentionally out of scope for this CS50P final project.

The system is designed from the perspective of an employee operating a terminal at a store counter. Customers interact with the store through the employee — they do not use the program directly.

## Domain Rules

- Late fees accrue at `$1/day` as soon as a rental is overdue
- A rental overdue by 14 or more days triggers a `$40` replacement charge — late fees are wiped, the item is marked `lost`, and stock is decremented automatically
- A game returned damaged beyond repair also triggers a replacement charge and marks the item `lost`
- A member account is blocked automatically when outstanding fees or replacement charges are present; a blocked account may not take any actions aside from paying fees or returning games, and is unblocked only once all charges are cleared

### Invariants

- A member may hold at most 3 active rentals at any one time, and may not rent more than one copy of the same title simultaneously
- All rentals are always due back 7 days from the rental date — no exceptions
- Each game in a transaction is its own separate rental log record
- Fees can only be paid in full, covering all outstanding charges across all of a member's rental logs at once
- Only customers aged 18 or older may create a membership account
- Replacement cost (`$40`) is fixed by head office and cannot be adjusted per store
- A customer must only ever have one address and one payment method stored at a time
- Late fees cannot accumulate on a rental log where a replacement charge is already active
- Copy counts may never be manually reduced — only system logic may do this
- Account status is always managed by the program, never set manually

## Technical Constraints

### [CS50P Requirements](https://cs50.harvard.edu/python/project/)

### Self-Imposed
- OOP for domain modules — the natural fit for encapsulating business rules per entity
- JSON for persistence — no database setup required; acceptable given single-process, single-operator scope
- CLI only — a GUI would be expected in a real-world system but is out of scope here
- `rich` for CLI output — plain `print` is unreadable for tabular data; `rich` tables are the minimum viable presentation layer
- Authentication and authorisation omitted — the system assumes a single trusted employee operator
- Concurrency not handled — JSON storage is safe only because one process runs at a time; race conditions are explicitly out of scope
- Audit logging and security hardening deferred — standard in production systems but add complexity with no benefit at this scope

## Data Model

The project stores data in JSON across three entities:

**Games**
- `game_id` — auto-generated
- `title`
- `platform`
- `total_copies` — default: `1`
- `replacement_cost` — default: `$40`

**Members**
- `membership_id` — auto-generated
- `full_name` — max 20 characters
- `date_of_birth` — format: `DD/MM/YY`
- `address`
- `payment_method`
- `account_status` — default: `active`

**Rental Logs**
- `rental_id` — auto-generated
- `membership_id` — links to a member
- `game_id` — links to a game
- `date_rented` — always today's date at checkout
- `due_for_return` — always 7 days after `date_rented`
- `late_fees_total` — default: `$0`
- `replacement_charge` — default: `false`
- `return_status` — default: `rented`

A member can have many rental logs over time, and a game can appear in many rental logs over time. The rental log acts as the join between members and games, capturing the full history of every rental.

## Design Decisions

- The program loads inventory, memberships, and rental logs at startup for simpler orchestration. Loading by domain was considered for stricter seperation, but deferred because it adds complexity with little benefit for the scope of this CS50 CLI project.

