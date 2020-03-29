from utils.orders import *
from algorithms.simulated_annealing import ListOrderer, compute_distance
from utils.store_generator import generate_indexed_store
from functools import reduce
import random

import numpy as np
import itertools


class GeneticStore():
    max_iterations = 100
    min_increment = 0.001

    def __init__(self, size, orders):
        self.size = size
        self.orders = orders
        self.population = []
        self.best = {}
        self.populate()

    def populate(self):
        for i in range(reduce(lambda x, y: x*y*4, self.size)):
            self.population.append(generate_indexed_store(
                self.size[0], self.size[1], randomize=True)
            )
        stores = self.fitness()
        self.best = stores[0]

    def fitness(self):
        stores = []
        # compute scrores
        for i in self.population:
            stores.append({"score": self.score(i), "store": store})
        norm = sum([i["score"] for i in stores])
        stores.sort(key=lambda x: x["score"], reverse=True)
        # Normalize scores
        for i in stores:
            i["score"] = 1 - i["score"] / norm
        return stores

    def run(self):
        acc = 0
        while acc < self.max_iterations:
            acc += 1
            nex_best = self.evolve()
            if abs(self.best["score"] - nex_best["score"]) < self.min_increment:
                return nex_best["store"]
            if self.best["score"] > nex_best["score"]:
                self.best = nex_best

    def evolve(self):
        nex_gen = self.match(self.fitness())
        for i in nex_gen:
            if random.random() > 0.5:
                mutations = random.randint(1, sum(self.size))
                self.mutate(i, mutations)
        self.population = nex_gen
        stores = self.fitness()
        return stores[0]

    def match(self, stores):
        weights = [i["score"] for i in stores]
        new_population = []
        for i in range(int(len(self.population)/2)):
            match = random.choices([i["store"]
                                    for i in stores], weights=weights, k=2)
            # stores.remove(match[0])
            # stores.remove(match[1])
            new_population += self.crossover(match)
        return new_population

    def crossover(self, stores):
        # Produce sub especificación
        # index = random.randint(2, len(stores[0])-1)
        # son_a = np.concatenate((stores[0][:index, :], stores[1][index:, :]))
        # son_b = np.concatenate((stores[1][:index, :], stores[0][index:, :]))
        # son_a = np.concatenate(
        #     (stores[0][:, :index], stores[1][:, index:]), axis=1)
        # son_b = np.concatenate(
        #     (stores[1][:, :index], stores[0][:, index:]), axis=1)
        # return [son_a, son_b]

        # PMX crossover
        # 2 different split points
        idx_a = random.randint(2, len(stores[0])-1)
        idx_b = random.randint(2, len(stores[0])-1)
        while idx_a == idx_b:
            idx_b = random.randint(2, len(stores[0])-1)

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


if __name__ == "__main__":
    # random.seed()
    # o_cant = 3
    # o_len = 8
    store_size = (1, 1)  # Not to big or memory will collapse!

    store = generate_indexed_store(*store_size)
    store_shape = store.shape

    # orders = [create_order(store, random.randint(1, o_len))
    #           for i in range(o_cant)]
    # # orders = [sort_order(i, store) for i in orders]
    # orders = sort_orders(orders, store)
    # gs = GeneticStore(store_size, orders)
    # current_fitness = gs.score(store)
    # acc = 0
    # while acc < 100:
    #     acc += 1
    #     store = gs.run()
    #     # orders = [sort_order(i, store) for i in orders]
    #     orders = sort_orders(orders, store)
    #     gs = GeneticStore(store_size, orders)
    #     new_fitness = gs.score(store)
    #     if abs(current_fitness - new_fitness) < 0:
    #         break
    #     else:
    #         current_fitness = new_fitness
    # print("Optimized Store: ")
    # print(store)
    print("---------------------------------")
    store = generate_indexed_store(*store_size)
    a = store.flatten()
    store = generate_indexed_store(*store_size, True)
    b = store.flatten()
    # b = b[::-1]
    print(a)
    print(b)

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
    print("Crossover: ")
    print(a)
    print(b)
    print(cicles)
