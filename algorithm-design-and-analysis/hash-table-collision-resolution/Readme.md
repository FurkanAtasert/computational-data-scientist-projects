# Quadratic Probing and Double Hashing

This project demonstrates two open addressing techniques used in hash tables to resolve collisions:

- Quadratic Probing
- Double Hashing

## Problem Description

Given a list of integer keys, the program inserts them into a hash table of fixed size using two different collision resolution methods and prints the final state of each table.

## Algorithm / Approach

The project uses a hash table with a fixed size of 10 and inserts the following keys:

    [18, 19, 20, 29, 30]

### Quadratic Probing

When a collision occurs, the program searches for the next available slot using the formula:

    (key + i^2) % table_size

where `i` increases step by step until an empty position is found.

### Double Hashing

When a collision occurs, the program uses a second hash function to calculate the step size:

    7 - (key % 7)

The new index is computed as:

    (initial_index + attempts * step) % table_size

This continues until an empty position is found or the table is full.

## File

- `quadratic_probing_and_double_hashing.py`

## How to Run

    python quadratic_probing_and_double_hashing.py

## Example Output

    Quadratic Probing Hash Table: [20, None, 30, None, None, 18, 19, 29, None, None]
    Double Hashing Hash Table: [20, None, 30, None, None, 18, 19, 29, None, None]

## Notes

This is a simple educational example for understanding collision resolution techniques in hash tables. It compares how quadratic probing and double hashing place keys into the table when collisions occur.
