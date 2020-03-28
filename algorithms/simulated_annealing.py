from algorithms.astar import Astar
import random
from utils.distances import manhattan as distance
from math import exp
# import itertools
# from functools import reduce


def round_trip(l):
    rounded_l = l.copy()
    rounded_l.insert(0, (0, 0))
    rounded_l.append((0, 0))
    return rounded_l


def compute_distance(path, store=None, fast=True):
    acc = 0
    if (fast):
        for i in range(1, len(path)):
            # Using Manhattan for distance finding (Faster, valid only for this particular scenario)
            acc += distance(path[i - 1], path[i])
    else:
        A = Astar(store)
        # Using A* algorithm for distance finding (Accurate and generic, valid for several scenarios. Slower)
        for i in range(1, len(path)):
            acc += len(A.astar(path[i - 1], path[i]))
    # return reduce((lambda x, y: distance(x, y)), path)
    return acc


class ListOrderer():
    def __init__(self, list, Temperature=10 ** 4, cooling_rate=0.003, iterations=10, seed=True, fast=True, store=None):
        self.list = list.copy()
        self.T = Temperature
        self.cooling_rate = cooling_rate
        self.iterations = iterations
        self.fast = fast
        self.store = store
        if seed:
            random.seed()

    def compute_distance(self, path):
        return compute_distance(path, self.store, self.fast)

    def simulated_annealing(self):
        while self.T > 0.01:
            self.list = self.pick(self.get_neighbors())
            self.update_temp()
        else:
            return self.get_path()

    def update_temp(self):
        self.T *= 1 - self.cooling_rate

    def get_neighbors(self):
        swapped_lists = []
        for i in self.list:
            swapped_list = self.list.copy()
            a, b = 0, 0
            while a == b:
                a = random.randrange(len(self.list) - 1)
                b = random.randrange(len(self.list) - 1)
            swapped_list[a], swapped_list[b] = swapped_list[b], swapped_list[a]
            swapped_lists.append(swapped_list)
        return swapped_lists  # incomplete neighbors list
        # return list(itertools.permutations(self.list)) #correct but inefficient, WIP to develop more cautious alternative.

    def pick(self, list):
        iterations = 0
        while iterations <= self.iterations:
            iterations += 1
            try:
                chosen = random.choice(list)
            except IndexError as e:
                return self.list
            chosen_cost = self.compute_distance(round_trip(chosen))
            current_cost = self.compute_distance(round_trip(self.list))
            if chosen_cost <= current_cost:
                return chosen
            else:
                delta = current_cost - chosen_cost
                probability = exp(delta/self.T)
                if random.random() < probability:
                    return chosen
        else:
            return self.list

    def get_path(self):
        return self.list
