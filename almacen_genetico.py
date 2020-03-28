from utils.orders import *
from algorithms.simulated_annealing import ListOrderer, compute_distance
from utils.store_generator import generate_indexed_store
from functools import reduce
import random

import numpy as np

random.seed()


class GeneticStore():
    def __init__(self, size, orders):
        self.size = size
        self.orders = orders
        self.population = []
        self.populate()

    def populate(self):
        for i in range(reduce(lambda x, y: x*y*4, self.size)):
            self.population.append(generate_indexed_store(
                self.size[0], self.size[1], randomize=True))

    def fitness(self, store):
        return sum([compute_distance(order_to_points(i, store)) for i in self.orders])


o_cant = 3
o_len = 8
store_size = (1, 1)  # Not to big or memory will collapse!
store = generate_indexed_store(*store_size)
orders = [create_order(store, random.randint(1, o_len)) for i in range(o_cant)]
print(orders)
orders = [sort_order(i, store) for i in orders]
print(orders)


gs = GeneticStore((1, 1), orders)
