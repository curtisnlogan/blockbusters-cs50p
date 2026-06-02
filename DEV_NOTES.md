# DEV_NOTES

## define

- Deliver a concise rental management system for a Blockbuster-style game store.
- Provide employees with tools to manage a game inventory, member accounts and rentals/returns.
- Enforce Blockbuster-style business rules and relationships for membership, game availability, overdue fees, and replacement charges.
- Customers create/update their membership, rent/return games and/or pay charges through interfacing with an employee that is using this program.
- Keep the scope limited to core game rental operations rather than detailed historical accuracy.

## constraints

### domain constraints

#### invariants

- replacement cost is dictated by head office, cannot be adjusted by individual stores
- a customer must only ever have one address and payment method stored at any one time
- a membership accounts status must be automatically handled by the program, not manually
- each game rented must be considered a seperate record (even if the customer checked out multiple rentals at one time)
- if a customers account is blocked, they may not take any actions asides from paying fees
- account unblocking is allowed only when no late fees or replacement charges are tied to it
- late fees cannot accumlate on rental logs were a replacement charge is active

#### management of the games inventory

- an employee must be able to add new titles
- an employee must be able to increase the copy count of an a non new title
  - employees must not be able to manually reduce the copy count
- an employee must not be able to edit a games database id

#### the creation of membership accounts

- a customer must be able to create a new membership account
- a membership account must store a full name, dob, address, valid payment method plus account status flag
- only adults 18+ can create accounts

#### customers renting games

- a member must not be able to actively rent more than one copy of a game title
- a member can not have more than 3 total active rentals at any one time
- a game must always be due for return 7 days after its rented
- a rental log can only be created after game availability is confirmed
- a potential renter must be informed verbally, that a `$40` replacement fee will be incurred if the game is more than 14 days overdue

#### management of late and replacement fees

- late fees are to be calculated at $2 per day as soon as the overdue date is hit
- a replacement charge of $40 must be incurred when any rental is 14 days or more overdue
  - late fees are wiped and stay at 0
  - the item must be flagged as "lost" and this loss must automatially be reflected in the stock of the games inventory

#### customers returning games

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

-  Several real-world concerns are intentionally out of scope
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

######  game inventory

- `game_id` - id: automatically generated
- `title` - optional
- `platform` - optional
- `total_copies` - default value: 1
- `replacement_cost` - default value: $40

##### membership accounts

- `membership_id` - id: auto generated
- `full_name` - 20 char limit
- `date_of_birth` - format: 31/05/23
- `address`
- `payment_method`
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
  - program entry point (main lives here)
- `cli.py` (not an object)
  - user-facing CLI interface
- `game_inventory.py` (OOP)
  - handles inventory rules and changes to game records
- `membership.py` (OOP)
  - handles membership rules and changes to member records
- `rental_record.py` (OOP)
  - handles rental rules and changes to rental log records
- `json_storage.py` (not an object)
  - handles JSON loading, saving, validation, and normalization
- `reconciliation.py` (not an object)
  - handles idempotent startup correction of derived state across inventory, members, and rentals

- `config.py`
   - centralized location to store files paths e.g. "instead of "data/inventory.json" appearing in storage.py and reconciliation.py, both would import INVENTORY_PATH from config.py"
- `test_project.py`
   - all of my unit tests live here
<!-- TODO: review from here -->
### behaviour

#### runtime

- At startup, `main.py` calls `json_storage.py` to load all JSON stores into in-memory dicts (loading all stores at startup keeps things simple for the scope of this project.)
- After this, `main.py` calls `reconciliation.py` to apply any valid adjustments across in-memory dicts
- If reconciliation alters any of in-memory dicts, `storage.py` should persist these changes back to all relevant JSONs before the CLI is available to the end-user
- Once completed, `main.py` passes only the correct shared in-memory collection into each buissness logic module
- At this point, the CLI main menu is now available to the end-user, it should note that all data has been loaded successfully, the system is now fully-operational
- The user is presented with 4 main options, inventory, memberships, rentals and exit. The first 3 have a sub-menu of actions that can then be performed, with the exit asking for confirmation (they will then have to restart the program manually)
- If the user has decided to close the program, it is expected that that the JSON stores represent the in-memory states which were present before exiting (the user can only exit the program mid-operation, not part-way through modification)
- If the user performs any operations on any domain through the CLI, it will call the appropriate actions
- Buissness logic modules return results and a status message to `main.py`, such as a validation error or success
- `main.py` uses that returned result to decide what to display through `cli.py` and to call `storage.py` to persist anything new to JSONs.
- After performing any operation either successfully or unsuccessfully, the user will be returned to the main menu

## vertical slices

### startup: load, validate, and reconcile system state

1. load all pre-populated JSON stores through `storage.py`
   1.1 load games inventory, membership accounts, and rental logs from the correct JSON files
   1.2 validate the loaded JSON structures
   1.3 normalize records lightly, e.g. trim whitespace
   1.4 store the validated data in shared in-memory collections
2. run startup reconciliation through `reconciliation.py` and persist any changes to JSON
   2.2 reconcile every rental log whose `return_status` is `rented`
   2.2.1 if a rental is overdue by 14 days or more, set `replacement_charge` to `true`, reset `late_fees_total` to `$0`, set `return_status` to `lost`, and deduct `1` from the linked game's `total_copies`
   2.2.2 if today is past `due_for_return` and `replacement_charge` is not flagged, recalculate `late_fees_total` at `$1` per overdue day for old releases
   2.3 reconcile each member's `account_status` from linked rental logs
   2.3.1 keep the account `blocked` if any linked `replacement_charge` is `true` and `replacement_charge_processed` is `false`
   2.3.2 otherwise keep the account `blocked` if any linked `late_fees_total > 0` exists
   2.3.3 otherwise set the account to `unblocked`

### view game inventory

1. employee requests the current games inventory
   1.1 display all loaded game records through the CLI
   1.2 show identifiers needed for rental workflows, including `game_id`

### increase game copy count

1. employee enters a `game_id` and requested new copy count
   1.1 reject invalid `game_id`
   1.2 reject non-integer copy count
   1.3 reject attempts to reduce copy count
   1.4 reject attempts to increase copy count above 99
2. update the relevant game record in memory and persist the successful change to JSON

### add new game to inventory

1. employee enters title, platform and total copies
   1.1 normalize employee input lightly, e.g. trim whitespace
   1.2 reject missing or invalid fields
   1.3 reject duplicate title + platform combination
   1.4 reject non-integer copy count
2. generate and persist the new game record
   2.1 generate a unique `game_id`
   2.3 default `replacement_cost` to `$40`
   2.4 append the new record in memory and persist to JSON

### create membership account

1. employee enters full name, date of birth, address, and payment method on customer request
   1.1 normalize employee input lightly, e.g. trim whitespace
   1.2 reject duplicate `full_name` + `date_of_birth`
   1.3 reject customers under 18
   1.4 reject invalid `payment_method`
2. generate and persist the new member record
   2.1 generate a unique `membership_id`
   2.2 default `account_status` to `unblocked`
   2.3 append the new record in memory and persist to JSON

### update membership account

1. employee enters a `membership_id` and confirms a formal customer request
   1.1 reject invalid `membership_id`
   1.2 reject update if no formal request exists
   1.3 only allow `address` and `payment_method` updates
   1.4 reject invalid `payment_method`
2. update the relevant member record in memory and persist the successful change to JSON

### rent games

1. employee enters a `membership_id` and one or more requested `game_id` values
   1.1 normalize employee input lightly, e.g. trim whitespace
   1.2 reject invalid `membership_id`
   1.3 reject invalid `game_id`
   1.4 reject blocked member accounts
   1.5 reject members with outstanding late fees (check `account_status`
  - check linked rental logs for unpaid late fees or unpaid replacement charges)
   1.6 reject members with unprocessed replacement charges
   1.7 reject unavailable games
   1.8 reject duplicate active rentals for the same member + game (check existing rental logs for the same `membership_id` + `game_id` where `return_status` is `rented`)
   1.9 reject transactions that would exceed 3 active rentals (include the requested rentals in the cap check before approving the transaction)
2. generate one rental log per approved game and persist to JSON
   2.1 generate a unique `rental_id`
   2.2 set `membership_id` and `game_id` from employee input
   2.3 set `date_rented` to today's date
   2.4 set `due_for_return` to 7 days after today's date
   2.5 default `late_fees_total` to `$0`
   2.6 default `replacement_charge` to `false`
   2.7 default `replacement_charge_processed` to `false`
   2.8 default `return_status` to `rented`

### pay outstanding charges

1. employee enters a `membership_id`
   1.1 reject invalid `membership_id`
   1.2 calculate all linked outstanding late fees and unprocessed replacement charges
   1.3 reject partial payment
2. process full payment
   2.1 reset paid `late_fees_total` values to `$0`
   2.2 set paid `replacement_charge_processed` values to `true`
   2.3 unblock the member only if no outstanding linked charges remain
   2.4 persist successful changes to JSON

### return games

1. employee enters a `rental_id`
   1.1 reject invalid `rental_id`
   1.2 reject rental logs that are already `returned` or `lost`
2. employee records return condition
   2.1 if the game is returned successfully, set `return_status` to `returned`
   2.2 if damaged beyond repair, set `replacement_charge` to `true`, set `return_status` to `lost`, reset `late_fees_total` to `$0`, and deduct `1` from the linked game's `total_copies`
3. reconcile linked member account status and persist successful changes to JSON
