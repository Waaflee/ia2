# !/usr/bin/python
import random
from utils.store_generator import extract_from_set
from algorithms.simulated_annealing import ListOrderer, compute_distance, round_trip
import numpy as np


def calculate_rows(size):
    acc = 6
    if size == 1:
        return acc
    for i in range(size-1):
        acc *= 2
        acc -= 1
    return acc


def order_generator(order_amount=24, store_size=2, seed=True):
    if seed:
        random.seed()
    orders = set()
    columns = 1 + 3*store_size
    rows = calculate_rows(store_size)
    v_free = set([i for i in range(0, columns, 3)])
    h_free = set([i for i in range(0, rows, 5)])

    for i in range(order_amount):
        x, y = 0, 0
        while (x, y) not in orders and (x, y) == (0, 0):
            while x in h_free:
                x = random.randint(0, rows - 1)
            while y in v_free:
                y = random.randint(0, columns - 1)
        orders.add((x, y))
    return orders


class Product():
    def __init__(self, index, amount):
        self.index = index
        self.amount = amount

    def __str__(self):
        return f"(index: {self.index}, amount: {self.amount})"


class Order():
    def __init__(self, amount, stock, store):
        self.list = self._indexed_order_generator(amount, stock, store)
        self.store = store.copy()
        self.sort()
        self.cost = self.get_cost()

    def _indexed_order_generator(self, amount, stock, store):
        indexes = [i for i in range(1, store[2::].max()+1)]
        return [Product(extract_from_set(indexes), random.randrange(1, stock)) for i in range(amount)]

    def sort(self):
        unordered_list = self._to_list()
        sa = ListOrderer(
            unordered_list, 100, 0.05, 10)
        self.list = [self.list[unordered_list.index(
            i)] for i in sa.simulated_annealing()]

    def _to_point(self, result):
        x = result[0][0]
        y = result[1][0]
        return (x, y)

    def _to_list(self):
        return [self._to_point(
            np.where(self.store == i.index)) for i in self.list]

    def get_cost(self):
        return compute_distance(self._to_list())
