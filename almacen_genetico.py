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
                self.size[0], self.size[1], randomize=True)
            )

    def fitness(self):
        stores = []
        # compute scrores
        for i in self.population:
            stores.append({"score": self.score(i), "store": store})
        max_score = max([i["score"] for i in stores])
        return stores, max_score
        # sort
        # stores.sort(key=lambda x: x["score"], reverse=True)
        # normalize
        # normalized_score = [i/max(stores) for i in stores]

    def match(self, stores, max_score):
        weights = [1 - i["score"] / max_score for i in stores]
        new_population = []
        for i in len(self.population)/2:
            match = random.choices(stores, weights=weights, k=2)
            # stores.remove(match[0])
            # stores.remove(match[1])
            new_population += self.crossover(match)

    def crossover(self, stores):
        index = random.randint(1, len(stores[0]))
        sons = []
        sons[0] = stores[0][:index] + stores[1][index:]
        sons[1] = stores[1][:index] + stores[0][index:]
        return sons

    def score(self, store):
        return sum([compute_distance(order_to_points(i, store)) for i in self.orders])


o_cant = 3
o_len = 8
store_size = (1, 1)  # Not to big or memory will collapse!
store = generate_indexed_store(*store_size)
orders = [create_order(store, random.randint(1, o_len)) for i in range(o_cant)]
orders = [sort_order(i, store) for i in orders]


gs = GeneticStore((1, 1), orders)
