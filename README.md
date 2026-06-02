# blockbusters-rental-manager
#### Video Demo: URL

## Description

A CLI rental management system for a Blockbuster-style game store. The program gives a single employee operator tools to manage game inventory, create member accounts, and process rentals, returns, and fee payments — all enforced by a defined set of business rules.

The system is a rough approximation of how Blockbuster operated, not an attempt at historical accuracy. The scope is limited to core game rental operations. Authentication, concurrency handling, audit logging, and a GUI are all intentionally out of scope for this CS50P final project.

The system is designed from the perspective of an employee operating a terminal at a store counter. Customers interact with the store through the employee — they do not use the program directly.

## Domain Rules/Logic

- One customer can rent a maximum of 3 games at a time
- Standard rentals due in 7 days
- Games flagged as new releases, due back in 2 days
- Late fees are charged at $1 per day, $2 per day for new releases
- Replacement fee charged automatically once a game has not been returned for 14 days

## Data Model

The project stores data in JSON using three main entities:

- `games`: id, title, platform, release date, total copies, replacement cost, new release flag
- `members`: id, name, date of birth, address, payment method, account status
- `rental_logs`: links members to games and stores: rental id, membership id, rental id, rental date, due date, late fees, replacement charges, and return status

In-terms of the overall relationships between my date, a member can have many rental logs, and a game can appear in many rental logs over time. The rental log system is the bridge which provides the many-to-many relationship between members and all of their rented games.

## Design Decisions

- The program loads inventory, memberships, and rental logs at startup for simpler orchestration. Loading by domain was considered for stricter seperation, but deferred because it adds complexity with little benefit for the scope of this CS50 CLI project.

