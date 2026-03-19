# Minimum Positive Sum by Subset Size

This project finds the minimum positive sum that can be obtained by selecting exactly k elements from an array, for each possible subset size.

## Problem Description

Given an array that may contain both positive and negative numbers, the program computes the minimum positive sum for every subset size from 1 to n.

If no positive sum can be formed for a given subset size, the result is shown as infinity.

## Algorithm / Approach

The program uses dynamic programming.

Let:

    dp[i][j]

represent the smallest possible sum obtained by selecting exactly j elements from the first i elements of the array.

The algorithm works as follows:

- If the current element is not selected, the previous value is kept.
- If the current element is selected, its value is added to the result of selecting one fewer element from the previous part of the array.
- The minimum of these two choices is stored.

After filling the dynamic programming table, the program checks the result for each subset size and keeps only positive sums.

## File

- `minimum_positive_sum_by_subset_size.py`

## How to Run

    python minimum_positive_sum_by_subset_size.py

## Example Input

    [2, -1, 3, 10, -2, 5]

## Example Output

    k = 1, minimum positive sum = 2
    k = 2, minimum positive sum = 1
    k = 3, minimum positive sum = 3
    k = 4, minimum positive sum = 4
    k = 5, minimum positive sum = 8
    k = 6, minimum positive sum = 17

## Notes

This is a simple educational example for understanding dynamic programming and subset-based optimization problems in Python.
