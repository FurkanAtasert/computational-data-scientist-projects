def find_minimum_positive_sum_by_subset_size(arr):
    n = len(arr)

    # dp[i][j] = the smallest possible sum obtained by selecting exactly j elements
    # from the first i elements of arr[:i]
    # Size: (n+1) x (n+1)

    dp = [[float("inf")] * (n + 1) for _ in range(n + 1)]

    # Initial state: dp[0][0] = 0 (sum is 0 when selecting 0 elements)
    dp[0][0] = 0

    for i in range(1, n + 1):
        for j in range(0, i + 1):
            # If j > i, it is already impossible, so j only goes up to i
            if j == 0:
                # Sum is 0 when selecting 0 elements
                dp[i][0] = 0
            else:
                # Case where the current element is not selected
                not_take = dp[i - 1][j]
                # Case where the current element is selected
                take = dp[i - 1][j - 1] + arr[i - 1]

                dp[i][j] = min(not_take, take)

    # dp[n][k] -> minimum sum when selecting k elements
    # Since we need a "positive" sum, check whether the result is greater than 0

    result = {}
    for k in range(1, n + 1):
        value = dp[n][k]
        if value <= 0:
            # If the result is 0 or negative, it is not considered positive
            result[k] = float("inf")
        else:
            result[k] = value

    return result


if __name__ == "__main__":
    array2 = [2, -1, 3, 10, -2, 5]
    min_sums = find_minimum_positive_sum_by_subset_size(array2)
    for k in range(1, len(array2) + 1):
        print(f"k = {k}, minimum positive sum = {min_sums[k]}")