import numpy as np


def generate_store(size):
    storage = np.ones([4, 2])
    vertical = np.zeros([4, 1])
    horizontal = np.zeros([1, 3])
    store = vertical
    for j in range(size):
        store = np.append(store, storage, axis=1)
        store = np.append(store, vertical, axis=1)
    # store = np.append(store, [np.zeros(store[0].size)], axis=0)
    store = np.insert(store, 0, [np.zeros(store[0].size)], axis=0)
    for i in range(size - 1):
        store = np.append(store, store, axis=0)
    store = np.append(store, [np.zeros(store[0].size)], axis=0)
    return store