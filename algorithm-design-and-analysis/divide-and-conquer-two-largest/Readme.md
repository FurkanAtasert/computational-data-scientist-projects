# Find Two Largest Distinct Numbers

This project finds the largest and second largest distinct numbers in an array using a divide and conquer approach.

## Problem Description

Given an array of numbers, the program recursively divides the array into smaller parts, finds the two largest distinct values in each part, and then combines the results to obtain the final answer.

If there is no second distinct largest value, the program returns negative infinity for the second value.

## Algorithm / Approach

The algorithm uses a divide and conquer strategy:

- If the array is empty, it returns negative infinity for both values.
- If the array has one element, it returns that element and negative infinity.
- If the array has two elements, it compares them directly.
- Otherwise, it splits the array into two halves, solves each half recursively, and merges the results.

This approach demonstrates recursive problem solving and comparison-based merging.

## File

- `find_two_largest_distinct.py`

## How to Run

    python find_two_largest_distinct.py

## Example Input

    [3, 1, 7, 7, 9, 2, 9, 8]

## Example Output

    Largest number: 9
    Second largest number: 8

## Notes

This is a simple educational example for understanding divide and conquer techniques in Python.
