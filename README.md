# blockbusters-rental-manager

## Problem Statement

- A software solution to manage the Blockbuster games rental service

## Core Functionality

- Concerned with core rental management functionality only
- Not attempting to be "perfectly" accurate with regards to Blockbuster policies
- Automatic account blocking/unblocking
- An employee can add and update game inventory
- An employee can create and update blockbuster membership accounts
- A customer can rent games
- A customer can pay late fees
- A customer can return games

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

