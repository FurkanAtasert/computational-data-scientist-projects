def maximum_non_overlapping_bus_rides(buses, transition_time=0):
    # 1) Sort the buses by end time
    #    so that we can always choose the bus that finishes earliest first
    buses_sorted = sorted(buses, key=lambda x: x[1])  # x[1] = end time

    max_count = 0
    # End time of the last selected bus
    # Start with -infinity because no bus has been selected yet
    last_end_time = float("-inf")

    for start, end, bus_id in buses_sorted:
        # To take this bus, its start time must be greater than or equal to
        # the last end time plus the transition time
        if start >= last_end_time + transition_time:
            # Select this bus
            max_count += 1
            # Mark ourselves as busy until this bus ends
            last_end_time = end

    return max_count


if __name__ == "__main__":
    # Example bus list:
    # (start_time, end_time, bus_id)
    # Here, there is an actual travel duration between start and end times.
    # transition_time = extra time needed after getting off one bus before taking another

    bus_list = [
        (9, 10, "BusA"),   # Starts at 9, ends at 10
        (10, 12, "BusB"),  # Starts at 10, ends at 12
        (9, 11, "BusC"),   # Starts at 9, ends at 11
        (11, 12, "BusD"),  # Starts at 11, ends at 12
        (12, 15, "BusE"),  # Starts at 12, ends at 15
        (14, 16, "BusF"),  # Starts at 14, ends at 16
        (15, 17, "BusG"),  # Starts at 15, ends at 17
    ]

    # For example, assume there is a 1-hour transition/waiting time after each ride
    transition_time = 1

    result = maximum_non_overlapping_bus_rides(bus_list, transition_time)
    print("Maximum number of bus rides:", result)