# DEV_NOTES

## define

- Deliver a concise rental management system for a Blockbuster-style game store.
- Provide employees with tools to manage a game inventory, member accounts and rentals/returns.
- Enforce Blockbuster-style business rules and relationships for membership, game availability, overdue fees, and replacement charges.
- Customers create/update their membership, rent/return games and/or pay charges through interfacing with an employee that is using this program.
- Keep the scope limited to core game rental operations rather than detailed historical accuracy.

## constraints

### domain constraints

### invariants

- replacement cost is dictated by head office, cannot be adjusted by individual stores
- a customer must only ever have one address and payment method stored at any one time
- a membership accounts status must be automatically handled by the program, not manually

#### management of the games inventory

- an employee must be able to add new titles
- an employee must be able to increase the copy count of an a non new title
  - employees must not be able to manually reduce the copy count
- an employee must not be able to edit a games database id

### the creation of membership accounts

- a customer must be able to create a new membership account
- a membership account must store a full name, dob, address, valid payment method plus account status flag
- only adults 18+ can create accounts
<!-- TODO: review from here -->
### customers renting games

- each game you rented must be considered a seperate record — has its own rental log (irregardless if the customer checked out multiple rentals at one time)
- a member must not be able to actively rent multiple copies of one game title
- a member can not have more than 3 active rentals at one time
- a customer cannot rent anything if blocked or if outstanding charges exist
- a game must always be due for return 7 days after its rented
- an employee must provide valid `game_id` values
  - reject invalid game ids
  - reject unavailable games
  - available copies are calculated from inventory and active rental logs
- a potential renter must be informed in verbally, that a `$40` replacement fee is incurred if the game is more than 14 days overdue

### customers returning games/paying fees & the penalities stemming from late or lost games

- late fees are to be calculated in dollars per day as soon as it is overdue
  - `$1` per day for non-new releases
  - `$2` per day for new releases
  - late fees do not continue accumulating after a replacement charge has been paid
- a replacement charge is incurred when a rental is 14 days or more overdue
  - late fees are wiped
  - the item must be flagged as "lost"
  - this must be reflected as a loss from the games inventory
- associated membership accounts must remain blocked whilst unpaid late fees or unpaid replacement charges exist
- late fees can only be paid in full, before any further rentals
- replacement charges must be paid in full, before any further rentals
- account unblocking is allowed only when all linked late fees are `$0` and all replacement charges are processed
- an employee must always check the condition of any returned game
  - if damaged beyond repair, a replacement charge must be paid by that member

## technical constraints

### CS50P requirements

- written in Python only
- include `main` and at least 3 additional functions at the same indentation level as `main`
- at least 3 functions (all in `project.py`) must have unit tests with `pytest`
- `main` must be called in a file called `project.py`
- all tests in `test_project.py` (each named `test_funcname`)
- pip libraries are allowed
  - all pip libraries used must be listed in `requirements.txt`
- "How to Submit" section on eDx to be completed, after project is finalized
- README "Your README.md file should be minimally multiple paragraphs in length, and should explain what your project is, what each of the files you wrote for the project contains and does, and if you debated certain design choices, explaining why you made them. Ensure you allocate sufficient time and energy to writing a README.md that documents your project thoroughly. Be proud of it! A README.md in the neighborhood of 500 words is likely to be sufficient for describing your project and all aspects of its functionality. If unable to reach that threshold, that probably means your project is insufficiently complex"


## design

### domain model

### game inventory

- `game_id` - id: automatically generated, not editable
- `title`
- `platform`
- `release_date`
- `total_copies`
- `replacement_cost` - default value: $40

### membership accounts

- `membership_id` - id: auto generated
- `full_name`
- `date_of_birth`
- `address` - 1 max
- `payment_method` - 1 max
- `account_status`

### rental logs

- `rental_id` - id: auto generated
- `membership_id`
- `game_id`
- `date_rented` - always current date
- `due_for_return` - always 7 days after `date_rented`
- `late_fees_total`
- `replacement_charge`
- `replacement_charge_processed`
- `return_status`

### relationships

- A member can have many rental logs.
- A game can appear in many rental logs over time.
- Rental logs bridge the many-to-many relationship between members and the games they rent.

## system design

### - use an OOP approach to practice common industry-style organization
- use JSON storage for persistence
- Startup reconciliation must be idempotent, so repeated restarts do not keep applying the same correction more than once.
- CLI only
- testing focuses on essential core business rules rather than exhaustive coverage
- include one integration test covering the core business flow
- use `rich` to improve CLI presentation
- use `pyfiglet` to generate a retro-looking Blockbuster-style logo for the main menu

### logical structure

- `main.py`
  - program entry point and orchestrator
- `cli.py`
  - user-facing CLI interface
- `inventory.py`
  - handles inventory rules and changes to game records
- `members.py`
  - handles membership rules and changes to member records
- `rentals.py`
  - handles rental rules and changes to rental log records
- `storage.py`
  - handles JSON loading, saving, validation, and normalization
- `reconciliation.py`
  - handles idempotent startup correction of derived state across inventory, members, and rentals

### runtime behaviour

- At startup, `main.py` uses `storage.py` to load all JSON stores into shared in-memory collections.
- Loading all stores at startup keeps orchestration simple for the scope of this CS50 CLI project.
- Loading data separately by domain was considered for stricter separation, but deferred because it adds complexity with little practical benefit for this project.
- After loading, `main.py` calls `reconciliation.py` to apply startup correction rules across the in-memory inventory, membership, and rental data.
- If reconciliation changes any records, `main.py` uses `storage.py` to persist those corrected in-memory collections back to JSON before the program enters the CLI flow.
- During runtime, `main.py` passes the shared in-memory collections into domain modules such as `inventory.py`, `members.py`, and `rentals.py`.
- Domain modules mutate only the relevant records in those shared in-memory collections rather than loading JSON or rebuilding and returning an entire collection.
- Domain methods return a small result object or status message to `main.py`, such as success/failure, a generated id, or a validation error.
- `main.py` uses that returned result to decide what to display through `cli.py` and whether `storage.py` should persist the updated in-memory state.
- This keeps `storage.py` responsible for persistence, domain modules responsible for business rules, `reconciliation.py` responsible for startup correction, and `main.py` responsible for orchestration.

## vertical slices

### startup: load, validate, and reconcile system state

1. load all pre-populated JSON stores through `storage.py`
   1.1 load games inventory, membership accounts, and rental logs from the correct JSON files
   1.2 validate the loaded JSON structures
   1.3 normalize records lightly, e.g. trim whitespace
   1.4 store the validated data in shared in-memory collections
2. run startup reconciliation through `reconciliation.py` and persist any changes to JSON
   2.1 reconcile `is_new_release` for all games based on `release_date`
   2.2 reconcile every rental log whose `return_status` is `rented`
   2.2.1 if a rental is overdue by 14 days or more, set `replacement_charge` to `true`, reset `late_fees_total` to `$0`, set `return_status` to `lost`, and deduct `1` from the linked game's `total_copies`
   2.2.2 if today is past `due_for_return` and `replacement_charge` is not flagged, recalculate `late_fees_total` at `$1` per overdue day for old releases or `$2` for new releases
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

1. employee enters title, platform, release date, and total copies
   1.1 normalize employee input lightly, e.g. trim whitespace
   1.2 reject missing or invalid fields
   1.3 reject duplicate title + platform combination
   1.4 reject non-integer copy count
2. generate and persist the new game record
   2.1 generate a unique `game_id`
   2.2 derive `is_new_release` from `release_date`
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
   2.4 set `due_for_return` to 7 days after today's date, or 2 days for new releases
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
