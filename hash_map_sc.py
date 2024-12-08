# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Description: This file implements a HashMap using Separate Chaining for collision resolution.
# It includes methods for put, get, remove, resizing, and finding mode in a dynamic array.

from a6_include import (DynamicArray, LinkedList, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int = 11, function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Add or update key/value pair in the hash map
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]

        if bucket.contains(key):
            bucket.remove(key)
        else:
            self._size += 1

        bucket.insert(key, value)

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to new capacity
        """
        if new_capacity < 1:
            return

        new_capacity = self._next_prime(new_capacity)
        new_map = HashMap(new_capacity, self._hash_function)

        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            for node in bucket:
                new_map.put(node.key, node.value)

        self._buckets = new_map._buckets
        self._capacity = new_map._capacity

    def table_load(self) -> float:
        """
        Return the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets in the hash table
        """
        count = 0
        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        Return value associated with the given key
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        node = bucket.contains(key)
        return node.value if node else None

    def contains_key(self, key: str) -> bool:
        """
        Return True if the given key is in the hash map
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        return bucket.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        Remove the given key and its associated value from the hash map
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        if bucket.contains(key):
            bucket.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array of all key/value pairs in the hash map
        """
        result = DynamicArray()
        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            for node in bucket:
                result.append((node.key, node.value))
        return result

    def clear(self) -> None:
        """
        Clear the contents of the hash map
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find the mode (most frequent value) in a dynamic array
    """
    map = HashMap()
    max_frequency = 0
    modes = DynamicArray()

    for i in range(da.length()):
        key = da[i]
        value = map.get(key)
        if value is None:
            map.put(key, 1)
        else:
            map.put(key, value + 1)

        max_frequency = max(max_frequency, map.get(key))

    for i in range(map.get_capacity()):
        bucket = map._buckets[i]
        for node in bucket:
            if node.value == max_frequency:
                modes.append(node.key)

    return modes, max_frequency
