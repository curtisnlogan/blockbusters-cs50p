# DEV_NOTES

## define

- Deliver a concise rental management system for a Blockbuster-style store. Scope limited to core game rental operations.
- Provide employees with tools to manage a game inventory, member accounts and rentals/returns.
- More specifically, customers create their membership, rent/return games and/or pay charges through interfacing with a Blockbuster employee that is using this program.

## constraints

### domain constraints

#### invariants

- replacement cost is dictated by head office, cannot be adjusted by individual employees
- membership account statuses must be automatically handled by the program, not editable by employees
- each game rented must be considered a seperate record, even if the customer checked out multiple rentals at one time (one rental log per game always)
- if a customers account is blocked, they may not take any actions asides from paying fees and returning games
- account unblocking is possible only when no late fees or replacement charges are present on it
- late fees cannot accumlate on rental logs were a replacement charge has been issued
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
  - the item must be flagged as "lost" and this loss must automatially be reflected in the stock of the games inventory

#### customers returning games

- customers are expected to provide the correcy rental ids when returning a game, through receipts
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
  - Authentication and authorisation are omitted — the system assumes a single trusted employee operator.
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

###### game inventory

- `game_id` - id: automatically generated
- `title`
- `platform`
- `total_copies`
- `replacement_cost` - default value: $40

##### membership accounts

- `membership_id` - id: auto generated
- `full_name`
- `is_over_18` - bool
- `address`
- `payment_method` - either 'Debit Card' or 'Credit Card'
- `account_status` - default: active

##### rental logs

- `rental_id` - id: auto generated
- `membership_id` - from membership accounts
- `game_id` - from game inventory
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

### behaviour

#### runtime

- At startup, `main.py` calls `json_storage.py` to load all JSON stores into in-memory dicts <!-- loading all stores at startup, instead of on request, keeps things simple for the scope of this project -->
- `main.py` calls `reconciliation.py` to apply any valid changes to in-memory dicts
- If reconciliation alters any in-memory dict, `storage.py` should persist these changes back to JSONs before the CLI is available to the end-user
- `main.py` then passes only the appropriate shared in-memory collection into each buissness logic module
- The CLI main menu is now available to the end-user, it should note that all data has been loaded successfully and that the system is fully-operational
- The user is presented with 4 main options, inventory, memberships, rentals and exit
- The first 3 of these have a sub-menu of actions that can then be performed, with the exit option asking for confirmation (after which the user will then have to restart the program manually)
- If the user has decided to close the program, it is expected that that the JSON stores represent the in-memory states which were present before exiting (the user can only exit the program through the main menu, not part-way through modification... the user should be warned about this)
- If the user performs any operations on any in-memory dicts through the CLI, business logic modules will always return a result, with a status such as a validation error or success (with payload), to `handlers.py`
- `handlers.py` then uses that returned result to decide what to display through `cli.py` and to call `storage.py` to persist anything new to JSONs
- `main.py` has a top-level error catch around the `handlers.py` call to handle any unexpected failures cleanly
- The user will then be returned to the main-menu, regardless

## slices

### user stories (end-to-end)

#### startup — as an employee, when I launch the program, all data is loaded in-memory, reconciled both in-memory and to JSONs, and confirmed operational before I can take any action.

#### view game inventory — as an employee, I can view the full game inventory so I know what is available.

#### rent games — as an employee, I can check out one or more games to an eligible member, with rental logs being created for each game.

#### return game — as an employee, I can process a game return and record its condition so stock and member account status update accordingly.

#### pay charges — as an employee, I can process full payment of a member's outstanding fees so their account is unblocked.

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
  <-- TODO -->
- employee selects to view the current games inventory
  - display all available game records and associated fields through the rich library in the CLI
  - should allow the user to go back to the main menu at any point

### rent games

- an employee selects the option to rent games to a customer
  - employee enters a membership id and a game id value for each seperate rental
  - employee informs the potential renter that a $40 replacement fee will be incurred if the game is more than 14 days overdue
  - `handlers.py` validates and normalizes the employee inputs
    - `normalizes input lightly, e.g. trim whitespace
    - `rejects invalid membership ids
    - rejects invalid game ids
    - rejects unavaiable games (no copies)
    - rejects duplicate active rentals for the same member + game (check existing rental logs for the same `membership_id` + `game_id` where `return_status` is `rented`)
    - reject transactions that would exceed 3 active rentals (include the requested rentals in the cap check before approving the transaction)
    - rejects blocked accounts
  - if checks pass, `handlers.py` generates a rental log for each game, decrements `total_copies` by `1` on the corresponding game record, and adds both changes to the in-memory store

### return games

- an employee enters into the cli a rental id that is provided by the customer
  - `handler.py` validates input
  - rejects invalid game ids
  - reject rental logs that are already marked as `returned` or `lost`
  - if all checks pass, `handler.py` marks the rental log as `returned`, increments `total_copies` by `1` on the corresponding game record, and updates the in-memory store
### pay charges

- an employee selects the option to pay a member's outstanding charges
  - employee enters a `membership_id`
  - `handlers.py` validates input
    - rejects invalid `membership_id`
    - rejects if no outstanding late fees or replacement charges exist
  - if checks pass, `handlers.py` calculates the full amount owed across all linked rental logs
    - resets all `late_fees_total` values to `0.0`
    - resets all `replacement_charge` values to `false`
    - for rental logs where only late fees were owed, set `return_status` to `returned`
    - for rental logs where a replacement charge was owed, `return_status` remains `lost`
    - unblocks the member account

### exit

- an employee selects the exit option from the main menu
  - CLI asks for confirmation
  - if confirmed, the program exits cleanly
  - if declined, the employee is returned to the main menu
