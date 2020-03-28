from algorithms.astar import Astar
from utils.distances import manhattan as distance
from math import exp
import random

# How much costs everything going from and to the starting point.


def round_trip(l):
    rounded_l = l.copy()
    rounded_l.insert(0, (0, 0))
    rounded_l.append((0, 0))
    return rounded_l


def compute_distance(path, store=None, fast=True):
    acc = 0
    path = round_trip(path)
    if (fast):
        for i in range(1, len(path)):
            # Using Manhattan for distance finding (Faster, valid only for this particular scenario)
            acc += distance(path[i - 1], path[i])
    else:
        A = Astar(store)
        # Using A* algorithm for distance finding (Accurate and generic, valid for several scenarios. Slower)
        for i in range(1, len(path)):
            acc += len(A.astar(path[i - 1], path[i]))
    return acc


class ListOrderer():
    def __init__(self, list, Temperature=10 ** 4, cooling_rate=0.003, iterations=10, seed=True, fast=True, store=None):
        self.list = list.copy()
        self.T = Temperature
        self.cooling_rate = cooling_rate
        self.iterations = iterations
        self.fast = fast
        self.store = store
        self.best = {
            "list": self.list.copy(),
            "cost": self.compute_distance(self.list)
        }
        if seed:
            random.seed()

    def compute_distance(self, path):
        return compute_distance(path, self.store, self.fast)

    def simulated_annealing(self):
        if len(self.list) == 1:
            return self.list
        while self.T > 0.01:
            self.list = self.pick(self.get_neighbors())
            self.is_better()
            self.update_temp()
        else:
            return self.get_path()

    def update_temp(self):
        self.T *= 1 - self.cooling_rate

    def is_better(self):
        cost = self.compute_distance(self.list)
        if cost < self.best["cost"]:
            self.best["list"] = self.list.copy()
            self.best["cost"] = cost

    def get_neighbors(self):
        swapped_lists = []
        while len(swapped_lists) < len(self.list) / 2:
            idx = range(len(self.list))
            a, b = random.sample(idx, 2)
            seq = self.list.copy()
            seq[a], seq[b] = seq[b], seq[a]
            if seq not in swapped_lists:
                swapped_lists.append(seq)
        return swapped_lists

    def pick(self, list):
        iterations = 0
        while iterations <= self.iterations:
            iterations += 1
            try:
                chosen = random.choice(list)
            except IndexError as e:
                return self.list
            chosen_cost = self.compute_distance(chosen)
            current_cost = self.compute_distance(self.list)
            if chosen_cost < current_cost:
                return chosen
            else:
                delta = current_cost - chosen_cost
                probability = exp(delta/self.T)
                if random.random() < probability:
                    return chosen
        else:
            return self.list

    def get_path(self):
        return self.best["list"]
