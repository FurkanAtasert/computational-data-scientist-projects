# Maximum Non-Overlapping Bus Rides

This project finds the maximum number of bus rides that can be taken without overlapping, optionally including a transition time between rides.

## Problem Description

Given a list of buses with start time, end time, and bus ID, the program selects the maximum number of rides such that:

- No two selected rides overlap
- A minimum transition time can be required between the end of one ride and the start of the next

## Algorithm / Approach

The program uses a greedy strategy.

First, all buses are sorted by their end times. Then the algorithm scans the sorted list and always selects the next bus that starts at or after:

    last_end_time + transition_time

This works because choosing the bus that finishes earliest leaves as much room as possible for future rides.

## File

- `maximum_non_overlapping_bus_rides.py`

## How to Run

    python maximum_non_overlapping_bus_rides.py

## Example Input

    [
        (9, 10, "BusA"),
        (10, 12, "BusB"),
        (9, 11, "BusC"),
        (11, 12, "BusD"),
        (12, 15, "BusE"),
        (14, 16, "BusF"),
        (15, 17, "BusG"),
    ]

Transition time:

    1

## Example Output

    Maximum number of bus rides: 3

## Notes

This is a simple educational example for understanding greedy algorithms and interval scheduling in Python.
