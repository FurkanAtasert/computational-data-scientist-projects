# Create hash tables and insert elements using quadratic probing
table_size = 10
hash_table_qp = [None] * table_size
keys = [18, 19, 20, 29, 30]


def quadratic_probing_insert(table, key):
    index = key % table_size
    i = 0
    while table[index] is not None:  # If the slot is occupied
        i += 1
        index = (key + i ** 2) % table_size  # Quadratic probing
    table[index] = key  # Insert the key into the table


# Insert keys using quadratic probing
for key in keys:
    quadratic_probing_insert(hash_table_qp, key)

# Output the quadratic probing hash table
print("Quadratic Probing Hash Table:", hash_table_qp)


# Place elements into the table using double hashing
hash_table_dh = [None] * table_size


# Helper function for double hashing
def second_hash(key):
    return 7 - (key % 7)


def double_hash_insert(table, key):
    index = key % table_size
    step = second_hash(key)
    initial_index = index  # Store the initial index
    attempts = 0  # Track the number of attempts

    while table[index] is not None:  # If the slot is occupied
        attempts += 1
        if attempts >= table_size:  # Stop if the entire table has been checked
            print(f"Table is full: could not insert {key}.")
            return  # The key could not be inserted
        index = (initial_index + attempts * step) % table_size  # Double hashing

    table[index] = key  # Insert the key into the table


# Insert keys using double hashing
for key in keys:
    double_hash_insert(hash_table_dh, key)

# Output the double hashing hash table
print("Double Hashing Hash Table:", hash_table_dh)