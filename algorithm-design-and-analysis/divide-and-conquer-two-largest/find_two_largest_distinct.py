def find_two_largest_distinct(arr):
    n = len(arr)

    # Base cases
    if n == 0:
        return (float("-inf"), float("-inf"))
    if n == 1:
        return (arr[0], float("-inf"))  # No second largest value
    if n == 2:
        if arr[0] > arr[1]:
            return (arr[0], arr[1])
        elif arr[0] < arr[1]:
            return (arr[1], arr[0])
        else:
            # If both values are the same, keep the second one as -inf
            return (arr[0], float("-inf"))

    # Split the array into two halves
    mid = n // 2
    left_part = arr[:mid]
    right_part = arr[mid:]

    # Recursively get max1 and max2 from left and right halves
    (left_max1, left_max2) = find_two_largest_distinct(left_part)
    (right_max1, right_max2) = find_two_largest_distinct(right_part)

    # Merge step
    # Find the overall largest value
    if left_max1 > right_max1:
        max1 = left_max1
        max2 = max(left_max2, right_max1)
    elif right_max1 > left_max1:
        max1 = right_max1
        max2 = max(right_max2, left_max1)
    else:
        # If left_max1 == right_max1, the largest value is the same
        max1 = left_max1
        # For the second largest distinct value, take the larger of left_max2 and right_max2
        max2 = max(left_max2, right_max2)

    return (max1, max2)


if __name__ == "__main__":
    array1 = [3, 1, 7, 7, 9, 2, 9, 8]
    largest, second_largest = find_two_largest_distinct(array1)
    print("Largest number:", largest)
    print("Second largest number:", second_largest)