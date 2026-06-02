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
- All three JSON stores loaded at startup rather than on demand — this is not a production app operating against a large database; loading everything upfront keeps orchestration simple with no meaningful cost at this scale
- CLI only — a GUI would be expected in a real-world system but is out of scope here
- `rich` for CLI output — plain `print` is unreadable for tabular data; `rich` tables are the minimum viable presentation layer
- `handlers.py` as a dedicated layer between `main` and the domain modules — without it, `main` would have to interpret every possible domain result and decide what to display and persist, which is logic that has no place in an entry point
- `startup_reconciliation.py` as its own module — reconciliation is critical to the accuracy of all three stores and must complete before the CLI is available; embedding it in `main` would bury something that important
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

## Files

**`project.py`** — Program entry point. `main` lives here. Handles startup only: loads all JSON stores via `storage.py`, runs reconciliation, persists any changes, then calls into `handlers.py`. Has a top-level error catch around that call for any unexpected failures.

**`handlers.py`** — Receives user actions from `cli.py`, calls the appropriate domain module, processes the result, and calls `cli.py` to render and `storage.py` to persist. This is where the "what do I do with this result" logic lives, keeping `main` minimal and `cli.py` as a pure presentation layer.

**`cli.py`** — User-facing CLI interface (not a class). Renders all menus, prompts, and output using `rich`. Collects input and renders output only — no business logic or persistence.

**`game_inventory.py`** — OOP module encapsulating all inventory rules and mutations: adding new titles, incrementing copy counts, and enforcing inventory constraints.

**`membership.py`** — OOP module encapsulating all membership rules and mutations: account creation, age validation, duplicate checking, and account status management.

**`rental_record.py`** — OOP module encapsulating all rental rules and mutations: creating rental logs, enforcing rental caps, processing returns, and calculating late fees and replacement charges.

**`storage.py`** — Handles all JSON I/O: loading stores at startup, saving in-memory dicts back to disk after mutations, validating and normalising data on load. Not a class.

**`startup_reconciliation.py`** — Runs once at startup before the CLI is available. Applies idempotent corrections to in-memory state: recalculates late fees, flags rentals overdue by 14+ days as `lost`, decrements stock, and blocks affected accounts. Any changes are persisted before the employee can act.

**`config.py`** — Single source of truth for all file paths. Prevents path strings from being scattered across multiple modules.

**`test_project.py`** — All unit tests, written with `pytest`. Each test follows the `test_<funcname>` naming convention required by CS50P.

**`requirements.txt`** — Lists all third-party pip libraries used by the project.

## Runtime

1. `main` calls `storage.py` to load all three JSON stores into in-memory dicts
2. `startup_reconciliation.py` runs — correcting fees, flagging lost items, updating stock, and blocking affected accounts
3. Any changes from reconciliation are persisted back to JSON before the CLI is available
4. The main menu is presented to the employee via `cli.py`
5. Each action the employee takes is routed through `handlers.py`, which calls the appropriate domain module and processes the result — validation errors and success responses are passed back through `cli.py` as user-friendly messages
6. On success, `handlers.py` calls `storage.py` to persist changes
7. The employee is returned to the main menu after every action, regardless of outcome
8. On exit, the JSON stores reflect the final in-memory state

