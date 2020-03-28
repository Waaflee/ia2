import numpy as np
import random

# deprecated


def generate_store(size):
    storage = np.ones([4, 2])
    vertical = np.zeros([4, 1])
    horizontal = np.zeros([1, 3])
    store = vertical
    for j in range(size):
        store = np.append(store, storage, axis=1)
        store = np.append(store, vertical, axis=1)
    store = np.insert(store, 0, [np.zeros(store[0].size)], axis=0)
    for i in range(size - 1):
        store = np.append(store, store, axis=0)
    store = np.append(store, [np.zeros(store[0].size)], axis=0)
    return store


def extract_from_set(numbers):
    item = random.choice(numbers)
    numbers.remove(item)
    return item


def generate_indexed_store(rows, columns, randomize=False):
    numbers = []
    if randomize:
        numbers = [i for i in range(1, rows * columns * 8 + 1)]
    slot = 0
    store = np.zeros((6*rows, 4*columns), dtype=np.int)
    for l in range(0, columns):
        for k in range(0, rows):
            for i in range(0, 6):
                for j in range(0, 4):
                    if j != 0 and j != 3 and i != 0 and i != 5:
                        if randomize:
                            store[i+k*6, j+l*4] = extract_from_set(numbers)
                        else:
                            slot = slot+1
                            store[i+k*6, j+l*4] = slot
    return np.array(store)
