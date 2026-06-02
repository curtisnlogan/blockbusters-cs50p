# DEV_NOTES

## define

- Deliver a concise rental management system for a Blockbuster-style game store.
- Provide employees with tools to manage a game inventory, member accounts and rentals/returns.
- Enforce Blockbuster-style business rules and relationships for membership, game availability, overdue fees, and replacement charges.
- Customers create their membership, rent/return games and/or pay charges through interfacing with an employee that is using this program.
- Keep the scope limited to core game rental operations rather than detailed historical accuracy.

## constraints

### domain constraints

#### invariants

- replacement cost is dictated by head office, cannot be adjusted by individual stores
- a customer must only ever have one address and payment method stored at any one time
- a membership accounts status must be automatically handled by the program, not manually
- each game rented must be considered a seperate record (even if the customer checked out multiple rentals at one time)
- if a customers account is blocked, they may not take any actions asides from paying fees or returning games
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
- `title`
- `platform`
- `total_copies` - default value: 1
- `replacement_cost` - default value: $40

##### membership accounts

- `membership_id` - id: auto generated
- `full_name` - 20 char limit
- `date_of_birth` - format: DD/MM/YY
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
- If the user performs any operations on any in-memory dicts through the CLI, buissness logic modules will always return a result, with a status message to `main.py`, such as a validation error or success (with payload)
- `main.py` then uses that returned result to decide what to display through `cli.py` and to call `storage.py` to persist anything new to JSONs.
- The user will then be returned to the main-menu, regardless

## slices

### user stories (end-to-end)

#### startup — as an employee, when I launch the program, all data is loaded in-memory, reconciled both in-memory and to JSONs, and confirmed operational before I can take any action.

#### view game inventory — as an employee, I can view the full game inventory so I know what is available.

#### add game to inventory — as an employee, I can add a new game title to the inventory so it becomes available to rent.

#### increase copy count — as an employee, I can increase the copy count of an existing game so stock levels stay accurate.

#### create membership — as an employee, I can create a membership account for a customer so they can begin renting games.

####  rent games — as an employee, I can check out one or more games to an eligible member, with rental logs being created for each game.

####  return game — as an employee, I can process a game return and record its condition so stock and member account status update accordingly.

####  pay charges — as an employee, I can process full payment of a member's outstanding fees so their account is unblocked.

####  exit — as an employee, I can exit the program from the main menu after confirming, so I don't close it accidentally mid-operation.

### user story specifications

#### startup

1. load all JSON stores through `project.py` and `storage.py`
   - store the validated data inside seperate in-memory dicts (one for each domain)

2. run startup reconciliation through `reconciliation.py` and persist any changes to JSON
   - calculate if a rental is overdue by 14 days or more, if so set `replacement_charge` to `true`, reset `late_fees_total` to `0`, set `return_status` to `lost`, deduct `1` from the game ids `total_copies` and block the associated members account
   - if today is past `due_for_return` and `replacement_charge` is not flagged, recalculate `late_fees_total` at `$1` per day overdue and block the associated members account

### view game inventory

1. employee selects through the cli option to view the current games inventory
   - display all available game records and associated fields through the CLI, in a neat but functional rich table format
   - allows the user to go back to the main menu once finished

### add new game to inventory

1. employee selects the sub menu option to add a new game to inventory
   - employee is asked to enter title, platform and total copies
   - checks - inform in user-friendly manner if any violation
      - normalize employee input lightly, e.g. trim whitespace
      - reject if any missing field
      - reject duplicate title + platform combination
      - reject non-integer copy count (must be below 100)
   - confirm creation to end-user if succesful
2. generate and persist the new game record to JSON/in-memory dict
   - generate a unique `game_id`
   - default `replacement_cost` set to 40
   - update in-memory dict
   - persist that in-memory dict to JSON

### increase copy count

1. employee choose sub-menu option to increase the copy count of pre-existing game, due to new stock arrival
   - employee is asked to enter a valid `game_id` and requested new copy count (int)
   - checks - inform employee in user-friendly manner if violated
      - reject invalid `game_id`
      - reject non-integer copy count (< 100)
      - reject any attempt to reduce the copy count
2. update the associated game records copy count in memory and persist the successful change to JSON
<!-- TODO: review from here -->
### create membership

1. employee enters full name, date of birth, address, and payment method on customer request
   - normalize employee input lightly, e.g. trim whitespace
   - reject duplicate `full_name` + `date_of_birth`
   - reject customers under 18
   - reject invalid `payment_method`
2. generate and persist the new member record
   - generate a unique `membership_id`
   - default `account_status` to `active`
   - append the new record in memory and persist to JSON

### rent games
<!-- "a potential renter must be informed verbally, that a $40 replacement fee will be incurred if the game is more than 14 days overdue." -->
1. employee enters a `membership_id` and one or more requested `game_id` values
   - normalize employee input lightly, e.g. trim whitespace
   - reject invalid `membership_id`
   - reject invalid `game_id`
   - reject blocked member accounts
   - reject members with outstanding late fees (check `account_status`
  - check linked rental logs for unpaid late fees or unpaid replacement charges)
   - reject members with unprocessed replacement charges
   - reject unavailable games
   - reject duplicate active rentals for the same member + game (check existing rental logs for the same `membership_id` + `game_id` where `return_status` is `rented`)
   - reject transactions that would exceed 3 active rentals (include the requested rentals in the cap check before approving the transaction)
2. generate one rental log per approved game and persist to JSON
   - generate a unique `rental_id`
   - set `membership_id` and `game_id` from employee input
   - set `date_rented` to today's date
   - set `due_for_return` to 7 days after today's date
   - default `late_fees_total` to `$0`
   - default `replacement_charge` to `false`
   - default `return_status` to `rented`

### return games

1. employee enters a `rental_id` (provided by the customer)
   - reject invalid `rental_id`
   - reject rental logs that are already `returned` or `lost`
2. employee records return condition
   - if the game is returned successfully, set `return_status` to `returned`
   - if damaged beyond repair, set `replacement_charge` to `true`, set `return_status` to `lost`, reset `late_fees_total` to `$0`, and deduct `1` from the linked game's `total_copies`
3. reconcile linked member account status and persist successful changes to JSON

### pay charges

1. employee enters a `membership_id`
   - reject invalid `membership_id`
   - calculate all linked outstanding late fees and unprocessed replacement charges
   - reject partial payment
2. process full payment
   - reset paid `late_fees_total` values to `$0`
   - set paid `replacement_charge_processed` values to `true`
   - unblock the member only if no outstanding linked charges remain
   - persist successful changes to JSON

### exit

1. employee clicks the exit option in the `cli.py` main menu
   - ask them if they are sure that they want to exit the program.
   - if they click no, run the command to display the mani menu, if they click yes, exit the program cleanly
