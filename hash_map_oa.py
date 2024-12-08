# Name: Jaskaran Singh Sidhu
# OSU Email: sidhuja@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - Open Addressing HashMap Implementation
# Description: Implements a HashMap using Open Addressing with Quadratic Probing.
# It includes put, resize, load factor management, and iterator functionality.

from a6_include import (DynamicArray, HashEntry, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses quadratic probing for collision resolution.
        """
        self._buckets = DynamicArray()
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output.
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        if capacity % 2 == 0:
            capacity += 1
        while not self._is_prime(capacity):
            capacity += 2
        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        if capacity == 2 or capacity == 3:
            return True
        if capacity < 2 or capacity % 2 == 0:
            return False
        for factor in range(3, int(capacity ** 0.5) + 1, 2):
            if capacity % factor == 0:
                return False
        return True

    def get_size(self) -> int:
        return self._size

    def get_capacity(self) -> int:
        return self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Add or update a key-value pair in the hash map using quadratic probing.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            current_index = (index + i ** 2) % self._capacity
            entry = self._buckets[current_index]
            if entry is None or entry.is_tombstone:
                self._buckets[current_index] = HashEntry(key, value)
                self._size += 1
                return
            elif entry.key == key:
                entry.value = value
                return
            i += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to the given capacity, rehashing all key-value pairs.
        """
        if new_capacity < self._size or not self._is_prime(new_capacity):
            return
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        for _ in range(new_capacity):
            self._buckets.append(None)
        for i in range(old_buckets.length()):
            entry = old_buckets[i]
            if entry is not None and not entry.is_tombstone:
                self.put(entry.key, entry.value)

    def table_load(self) -> float:
        """
        Return the current load factor of the hash table.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the hash table.
        """
        count = 0
        for i in range(self._buckets.length()):
            if self._buckets[i] is None or self._buckets[i].is_tombstone:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        Retrieve the value associated with the given key, or None if the key does not exist.
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            current_index = (index + i ** 2) % self._capacity
            entry = self._buckets[current_index]
            if entry is None:
                return None
            if entry.key == key and not entry.is_tombstone:
                return entry.value
            i += 1

    def contains_key(self, key: str) -> bool:
        """
        Check if the given key exists in the hash map.
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            current_index = (index + i ** 2) % self._capacity
            entry = self._buckets[current_index]
            if entry is None:
                return False
            if entry.key == key and not entry.is_tombstone:
                return True
            i += 1

    def remove(self, key: str) -> None:
        """
        Remove the key-value pair associated with the given key from the hash map.
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            current_index = (index + i ** 2) % self._capacity
            entry = self._buckets[current_index]
            if entry is None:
                return
            if entry.key == key and not entry.is_tombstone:
                entry.is_tombstone = True
                self._size -= 1
                return
            i += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Return a dynamic array containing all key-value pairs in the hash map.
        """
        result = DynamicArray()
        for i in range(self._buckets.length()):
            entry = self._buckets[i]
            if entry is not None and not entry.is_tombstone:
                result.append((entry.key, entry.value))
        return result

    def clear(self) -> None:
        """
        Clear the hash map, removing all key-value pairs.
        """
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(None)

    def __iter__(self):
        """
        Initialize the iterator for the hash map.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Iterate through the hash map and return each entry.
        """
        while self._index < self._buckets.length():
            entry = self._buckets[self._index]
            self._index += 1
            if entry is not None and not entry.is_tombstone:
                return entry
        raise StopIteration
