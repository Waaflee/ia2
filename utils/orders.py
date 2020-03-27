#!/usr/bin/python
from utils.store_generator import generate_store
import random


def order_generator(order_amount=24, store_size=2, seed=True):
    if seed:
        random.seed()
    orders = set()
    store = generate_store(store_size)
    columns = store[0].size
    rows = int(store.size / columns)
    v_free = [i for i in range(0, columns, 3)]
    h_free = [i for i in range(0, rows, 5)]

    for i in range(order_amount):
        x, y = 0, 0
        while (x, y) not in orders and (x, y) == (0, 0):
            while x in h_free:
                x = random.randint(0, rows - 1)
            while y in v_free:
                y = random.randint(0, columns - 1)
        orders.add((x, y))
    return orders
