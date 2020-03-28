from utils.orders import Order
from algorithms.simulated_annealing import ListOrderer, compute_distance, round_trip
from utils.store_generator import generate_indexed_store
import random
from functools import reduce

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


order_amount = 1
max_order_size = 8
max_stock = 5
store_size = (1, 1)  # Not to big or memory will collapse!
store = generate_indexed_store(*store_size, True)
orders = [Order(random.randrange(
    1, max_order_size), max_stock, store) for i in range(order_amount)]

# gs = GeneticStore((1, 1), orders)
