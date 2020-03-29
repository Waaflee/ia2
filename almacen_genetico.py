from utils.orders import *
from algorithms.simulated_annealing import ListOrderer, compute_distance
from utils.store_generator import generate_indexed_store
from functools import reduce
import random

import numpy as np
import itertools


class GeneticStore():
    max_iterations = 100
    min_increment = 0.99

    def __init__(self, size, orders, shape):
        self.size = size
        self.shape = shape
        self.orders = orders
        self.population = []
        self.population_score = 0
        self.populate()

    def populate(self):
        for i in range(self.size[0] * self.size[1] * 10):
            self.population.append(generate_indexed_store(
                self.size[0], self.size[1], randomize=True)
            )
        self.population_score = self.pop_score()

    def fitness(self):
        stores = []
        for i in self.population:
            stores.append({"score": self.score(i), "store": i})
        norm = sum([i["score"] for i in stores])
        stores.sort(key=lambda x: x["score"])
        for i in stores:
            i["cost"] = i["score"]
            i["score"] = 1 - (i["score"] / norm)
        return stores

    def run(self):
        acc = 0
        while acc < self.max_iterations:
            acc += 1
            self.evolve()
            current_population_score = self.pop_score()
            if current_population_score / self.population_score > self.min_increment:
                # return min([self.score(i) for i in self.population])
                return self.fitness()[0]
                # return self.fitness()[0]["store"]
            self.population_score = current_population_score
        return self.fitness()[0]

    def evolve(self):
        nex_gen = self.match(self.fitness())
        for i in nex_gen:
            # if random.random() > 0.25:
            mutations = random.randint(1, sum(self.size))
            self.mutate(i, mutations)
        self.population = nex_gen.copy()
        return

    def match(self, stores):
        weights = [i["score"] for i in stores]
        new_population = []
        # for i in range(int(len(self.population)/2)):
        #     match = random.choices([i["store"]
        #                             for i in stores], weights=weights, k=2)
        #     # match = random.sample(self.population, 2)
        #     # stores.remove(match[0])
        #     # stores.remove(match[1])
        #     new_population += self.crossover(match)
        for i in range(1, (len(self.population)), 2):
            pair = [stores[i-1]["store"], stores[i]["store"]]
            new_population += self.crossover(pair)
        return new_population

    def crossover(self, stores):
        a = stores[0].flatten()
        b = stores[1].flatten()
        cicles = list()
        cicle = set()
        for i in a:
            if i != 0:
                if i not in list(itertools.chain.from_iterable(cicles)):
                    p1 = i
                    p2 = 0
                    cicle.add(i)
                    while p2 != i:
                        p2 = int(b[np.where(a == p1)])
                        cicle.add(p2)
                        p1 = int(a[np.where(a == p2)])
                        cicle.add(p1)
                    cicles.append(list(cicle))
                    cicle = set()
        for i in range(len(cicles)):
            if i % 2 == 1:
                cicle = cicles[i]
                indexes = [np.where(a == j) for j in cicle]
                for k in indexes:
                    a[k[0]], b[k[0]] = b[k[0]], a[k[0]]
        a = np.reshape(a, self.shape)
        b = np.reshape(b, self.shape)
        return [a, b]

    def mutate(self, store, mutations=1):
        for i in range(mutations):
            item_a = random.randint(1, store[2::].max())
            item_b = random.randint(1, store[2::].max())
            point_a = np.where(store == item_a)
            point_b = np.where(store == item_b)
            store[point_a] = item_b
            store[point_b] = item_a

    def score(self, store):
        return sum([compute_distance(order_to_points(i, store)) for i in self.orders])

    def pop_score(self):
        return sum([self.score(i) for i in self.population])


if __name__ == "__main__":
    random.seed()
    o_cant = 3
    o_len = 8
    store_size = (1, 1)  # Not to big or memory will collapse!
    store_max = store_size[0] * store_size[1] * 8
    store_shape = (store_size[0] * 6, store_size[1]*4)
    store = generate_indexed_store(*store_size)
    orders = [create_order(store_max, random.randint(1, o_len), True)
              for i in range(o_cant)]
    gs = GeneticStore(store_size, orders, store_shape)
    print("Initial Cost: ", gs.score(store))
    store = gs.run()
    print("First optimization: ", store["cost"])
    current_fitness = gs.score(store["store"])
    acc = 0
    while acc < 100:
        acc += 1
        store = gs.run()
        orders = sort_orders(orders, store["store"])
        gs = GeneticStore(store_size, orders, store_shape)
        new_fitness = gs.score(store["store"])
        if abs(current_fitness - new_fitness) < 0:
            break
        else:
            current_fitness = new_fitness
    print("Optimized Store: ")
    print(store)
