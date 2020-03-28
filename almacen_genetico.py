from utils.orders import Order
from algorithms.simulated_annealing import ListOrderer, compute_distance, round_trip
from utils.store_generator import generate_indexed_store
import random
from functools import reduce

import numpy as np

random.seed()


def create_order(store, size, uniques=False):
    if uniques:
        order = set()
        for i in range(size):
            order.add(random.randint(1, store[2::].max()))
        return list(order)
    else:
        order = []
        for i in range(size):
            order.append(random.randint(1, store[2::].max()))
        return order


def array_to_point(array):
    print(array)
    x = array[0][0]
    y = array[1][0]
    return (x, y)


def order_to_points(order, store):
    return [array_to_point(np.where(store == i)) for i in order]


def points_to_order(points, store):
    return [store[i[0]][i[1]] for i in points]


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

    def fitness(self):
        return sum([compute_distance(i._to_list()) for i in self.orders])


order_amount = 3
max_order_size = 8


# max_stock = 5
store_size = (1, 1)  # Not to big or memory will collapse!
store = generate_indexed_store(*store_size)

orders = [create_order(store, random.randint(1, max_order_size))
          for i in range(order_amount)]
a = order_to_points(orders[0], store)
b = points_to_order(order_to_points(orders[0], store), store)

c = "as"
# orders = [Order(random.randrange(
#     1, max_order_size), max_stock, store) for i in range(order_amount)]

# gs = GeneticStore((1, 1), orders)
# print(gs.fitness())
