class HashMap:

    # Constructor -> O(1)
    def __init__(self):
        self.size = 64
        self.map = [None] * self.size

    # Getter that creates a hash key -> O(1)
    def _get_hash(self, key):

        return int(key) % self.size

    # Inserts a new value into the hash table -> O(1)
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            self.map[key_hash].append(key_value)
            return True

    # Updates an existing hash table entry with a new value -> O(N)
    def update(self, key, value):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        else:
            for key_value_pair in self.map[key_hash]:
                if key_value_pair[0] == key:
                    key_value_pair[1] = value
                    return True

    # Updates an existing hash table chained entry with a new value at the specified index -> O(N)
    def update_at(self, key, value, index):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        else:
            for key_value_pair in self.map[key_hash]:
                if (key_value_pair[0] == key) & (self.map[key_hash].index(key_value_pair) == index):
                    key_value_pair[1] = value
                    return True

    # Returns an existing value from the hash table -> O(1)
    def get(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is not None:
            for key_value_pair in self.map[key_hash]:
                if key_value_pair[0] == key:
                    return key_value_pair[1]
        else:
            return None

    # Returns all matching values given a key from the hash table -> O(N)
    def get_all(self, key):
        key_hash = self._get_hash(key)
        return_list = list()
        return_list.append(key)

        if self.map[key_hash] is not None:
            for key_value_pair in self.map[key_hash]:
                if key_value_pair[0] == key:
                    return_list.extend(key_value_pair[1:])

        return return_list

    # Deletes a value from the hash table -> O(N)
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is not None:
            for i in range(0, len(self.map[key_hash])):
                if self.map[key_hash][i][0] == key:
                    self.map[key_hash].pop(i)
                    return True
        else:
            return False
