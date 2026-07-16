# DEV_NOTES

## define

- Problem: A pen and paper rental management system for a Blockbuster-style store is less reliable and more human error-prone. Employees need a digital solution to manage game rentals, returns, late fees/replacement charges, and member accounts effectively.
- Success: Ship a concise rental management system for a Blockbuster-style store. It should be user-friendly, reliable and extensible for future features.
- None-goals: Scope should be limited to core game rental operations, not movies etc. It also does not need to be historically accurate to the real Blockbuster company, just a rough version of it. It does not handle concurrent access, as this is a single-user CLI application. A GUI is not required, but the CLI should be user-friendly and visually appealing. It does not need to handle authentication or authorization, as it assumes a single trusted employee operator. A database is not required, but JSON storage should be used for persistence. Audit logging and security hardening are out of scope.

## constraints

### domain constraints

#### invariants

- replacement cost is dictated by head office, cannot be adjusted by individual employees
- membership account statuses must be automatically handled by the program, not editable by employees
- each game rented must be considered a separate record, even if the customer checked out multiple rentals at one time (one rental log per game always)
- if a customers account is blocked, they may not take any actions asides from paying fees and returning games
- account unblocking is possible only when no late fees or replacement charges are present on it
- late fees cannot accumulate on rental logs were a replacement charge has been issued
- no membership accounts may ever exist were the age of the holder is under 18

#### management of the games inventory

- an employee must be able to add new titles
- an employee must be able to increase the copy count of an a non new title
- employees must not be able to manually reduce the copy count
- an employee must not be able to edit a games database id

#### the creation of membership accounts

- a customer must be able to create a new membership account

#### customers renting games

- a member must not be able to actively rent more than one copy of a game title
- a member can not have more than 3 total active rentals at any one time
- a game must always be due for return 7 days after its rented
- a rental log can only be created after game availability is confirmed
- a potential renter must be informed verbally, that a `$40` replacement fee will be incurred if the game is more than 14 days overdue

#### management of late and replacement fees

- late fees are to be calculated at $1 per day as soon as the overdue date is hit
- a replacement charge of $40 must be incurred when any rental is 14 days or more overdue
  - late fees are wiped and stay at 0
  - the item must be flagged as "lost" and this loss must automatically be reflected in the stock of the games inventory

#### customers returning games

- customers are expected to provide the correct rental ids when returning a game, through receipts
- returned games are to be flagged as returned, with the games inventory automatically updating to reflect this
- an employee must always check the condition of any returned game
  - if damaged beyond repair, a replacement charge must incurred on the associated rental log

#### customers paying late and/or replacement fees

- late fees and replacement charges can only be paid in full, for all rental logs were they are being incurred by said customer

### technical constraints

#### CS50P

- written in Python only
- includes a `main` func (`project.py`) and at least 3 additional functions at the same indentation level as `main`
- at least 3 functions (all in `project.py`) must have unit tests through `pytest` (in `test_project.py`)
- all tests in `test_project.py` (each named `test_funcname`)
- pip libraries are allowed
  - all pip libraries used must be listed in `requirements.txt`
- "How to Submit" section on final proj edx page to be completed, after project is finalized
- README
  - what each of the files you wrote for the project contains and does
  - if you debated certain design choices, explaining why you made them
  - A README.md in the neighborhood of 500 words is likely to be sufficient for describing your project and all aspects of its functionality. If unable to reach that threshold, that probably means your project is insufficiently complex

#### self-imposed

- Several real-world concerns are intentionally out of scope
  - Authentication and authorization are omitted — the system assumes a single trusted employee operator.
  - Concurrency is not handled; JSON storage is safe only because one process runs at a time.
  - Audit logging, security hardening are all deferred.
  - These are standard requirements in production systems at scale but would add significant complexity with no benefit at this for a CS50P final project.
- OOP - industry standard to this problem
- JSON storage for persistence - time-constraint no database
- does not need to account for 'race conditions', were two employees edit the same JSON at the same time - out of scope for this project, complexity
- CLI only - time-constraint, GUI mandatory in real-world
- must use `rich` to improve CLI presentation - compensate for lack of GUI ( Plain rich tables for displaying inventory/rentals is genuinely useful (data is unreadable otherwise)

## design

### structure

#### domain model

- each JSON store is a dict of dicts keyed by its record's id (not a list of records) — the id lives as the outer key only, not duplicated as a field inside the record. this gives O(1) lookups by id and avoids the key/field drifting apart

###### game inventory

- `game_id` - id: automatically generated - the outer key of each record
- `title`
- `platform`
- `total_copies`
- `replacement_cost` - default value: $40

##### membership accounts

- `membership_id` - id: auto generated - the outer key of each record
- `full_name`
- `is_over_18` - bool
- `address`
- `payment_method` - either 'Debit Card' or 'Credit Card'
- `account_status` - default: active

##### rental logs

- `rental_id` - id: auto generated - the outer key of each record
- `membership_id` - from membership accounts (field inside the record, references a members key)
- `game_id` - from game inventory (field inside the record, references a game inventory key)
- `date_rented` - always current date
- `due_for_return` - always 7 days after rented date
- `late_fees_total` - default: $0
- `replacement_charge` - default: false
- `return_status` - default: rented

##### relationships

- A member can have many rental logs over time.
- A game can appear in many rental logs over time.
- Rental logs as a "join table" bridges that many-to-many relationship between members and the games that they rent.

#### application structure

- `project.py`
  - program entry point (main lives here); handles startup and top-level error catching only
- `handlers.py` (not an object)
  - receives user actions from the CLI, calls the appropriate domain module, processes the result, and calls `cli.py` to render and `storage.py` to persist
- `cli.py` (not an object)
  - user-facing CLI interface; pure presentation layer — collects input and renders output only
- `game_record.py` (OOP)
  - handles inventory rules and changes to game records
- `membership.py` (OOP)
  - handles membership rules and changes to member records
- `rental_record.py` (OOP)
  - handles rental rules and changes to rental log records
- `storage.py` (not an object)
  - handles JSON loading, saving, validation, and normalization
- `startup_reconciliation.py` (not an object)
  - handles idempotent startup correction of derived state across inventory, members, and rentals

- `config.py`
  - centralized location to store files paths e.g. "instead of "data/inventory.json" appearing in storage.py and reconciliation.py, both would import INVENTORY_PATH from config.py"
- `test_project.py`
  - all of my unit tests live here

### behavior

#### runtime

- At startup, `project.py` calls `storage.py` to load all JSON stores into in-memory dicts <!-- loading all stores at startup, instead of on request, keeps things simple for the scope of this project -->
- `project.py` calls `handlers.py` immediately
- `handlers.py` should always call `startup_reconciliation.py` first, to apply any necessary changes to in-memory dicts
- `handlers.py` then calls `cli.py`, which makes the terminal main menu available to the end-user
- `handlers.py` then passes only the appropriate shared in-memory collection into each class module, if called
- `cli.py` should first note that all data has been loaded successfully and that the system is fully-operational
- the user is presented with 4 main options, game records, memberships, rental records, and exit
- The exit option asks for confirmation, then either closes the program or returns to the main menu if cancelled
- Rentals will have a sub-menu of actions that can be performed if selected
- If the user has decided to close the program, it is expected that that the JSON stores now represent the in-memory states which were present before exiting
<!-- TODO -->
- If the user selects operations in `cli.py` that alter in-memory dicts, the subsequent methods are called by `handlers.py` and displays success messages back through `cli.py`
- `project.py` should handle all high level errors such as IO etc. from storage.py

## slices

### user stories (end-to-end)

#### startup — as an employee, when I launch the program, all data is loaded in-memory, reconciled both in-memory and to JSONs, and confirmed operational before I can take any action.

#### view game inventory — as an employee, I can view the full game inventory so I know what is available.

### view members - as an employee, I can view the entire list of members so I know what customers exist.

#### rent games — as an employee, I can check out one or more games to an eligible member, with rental logs being created for each game.

#### return game — as an employee, I can process a game return and record its condition so stock and member account status update accordingly.

#### pay charges — as an employee, I can process full payment of a member's outstanding fees so their account is unblocked.

#### user friendly - as an employee, I can navigate the CLI, find it visually appealing with clear instructions so I can perform my job effectively.

#### exit — as an employee, I can exit the program from the main menu after confirming, so I don't close it accidentally mid-operation.

### user story flows

#### startup

- `project.py` loads prepopulated JSON stores through `storage.py`
- `project.py` calls `handlers.py` with data from `storage.py` as arg
- `handlers.py` calls `startup_reconciliation.py`
- `reconciliation.py`
  - skip rentals where `return_status` is already `returned` or `lost`

  - if 14+ days overdue and `replacement_charge` is false, set `replacement_charge` to `true`, reset `late_fees_total` to `0.0`, set `return_status` to `lost`, deduct `1` from the corresponding game's `total_copies`, and block the associated member's account
  - else if overdue but under 14 days, recalculate `late_fees_total` at $1 per day overdue and block the associated member's account

### view game inventory

- employee selects to view the current games inventory
  - display all available game records and associated values through the rich library in the CLI
  - should allow the user to go back to the main menu at any point

### view members

- an employee selections the option to view the current list of members
  - display all available and associated values through the rich library in the CLI
  - should allow the user to go back to the main menu at any point

### rent games

- an employee selects the option to rent games to a customer
  - employee enters a membership id and a game id value for each separate rental
  - employee informs the potential renter of late fees and replacement charge business rules
  - `cli.py` validates and normalizes the employee inputs
    - normalizes input lightly, e.g. trim whitespace
    - rejects invalid membership ids
    - rejects invalid game ids
    - rejects unavailable games (0 copies in-stock)
    - rejects blocked accounts
  - if checks pass, `handlers.py` generates a new rental log for each game, decrements `total_copies` by `1` on the corresponding game record, and adds the new entry to the in-memory store

### return games

- an employee enters into the cli a rental id that is provided by the customer
  - `handler.py` validates input
  - rejects invalid game ids
  - reject rental logs that are already marked as `returned` or `lost`
  - if all checks pass, `handler.py` marks the rental log as `returned`, increments upwards `total_copies` by `1` on the corresponding game record, and updates the in-memory store
### pay charges

- an employee selects the option to pay a member's outstanding charges
  - employee enters a `membership_id`
  - rejects invalid `membership_id`
  - rejects if no outstanding late fees or replacement charges exist
  - if checks pass, `cli.py` calculates the amount owed across all rental logs
    <!-- TODO -->
  - once payment by member is confirmed by employee, `cli.py` returns a set of rental_ids that are to have fees nullified, `handlers.py` referencing this set, mutates the in-memory store to reflect this
    - for rental logs where only late fees were owed, set `return_status` to `returned`
    - for rental logs where a replacement charge was owed, `return_status` remains `lost`
    - unblock the member's account

### user friendly

- rich library is used to improve the CLI presentation
  - tables are used to display game inventory and member records
  - clear instructions are provided for each action
  - input prompts are clear and concise
  - success and error messages confirm current state of the system after each action
  - uses rich syntax to add visual appeal to the CLI, e.g. colors, bold text, etc.

### exit

- an employee selects the exit option from the main menu
  - CLI asks for confirmation
  - if confirmed, the program exits cleanly
  - if declined, the employee is returned to the main menu
