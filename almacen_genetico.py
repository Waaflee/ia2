import time
from utils.orders import order_generator, indexed_order_generator
from utils import store_generator
import random
from algorithms.simulated_annealing import ListOrderer, compute_distance, round_trip
from utils.store_generator import generate_store, generate_indexed_store
from pydash import arrays as _
import numpy as np


def populate_store(amount=5, stock=20, store_size=3, seed=True):
    if seed:
        random.seed()
    orders = list(order_generator(amount, store_size))
    products = {}
    for i in range(len(orders)):
        products[f"product_{i}"] = {"stock": random.randrange(stock) + 1,
                                    "location": orders[i]}
    return products


order_amount = 8
max_order_size = 5
max_stock = 20
store_size = (1, 1)  # Not to big or memory will collapse!
store = generate_indexed_store(*store_size, True)
print(store)
print(*np.where(store == 8))
print(store[2::].max())
orders = [indexed_order_generator(random.randrange(
    1, max_order_size), max_stock, store) for i in range(order_amount)]
print(orders)
# for i in store.T:
#     print(i)
# p = populate_store(order_amount, max_stock, store_size)
# l = [p[i]["location"] for i in p]

# print("Current Distance: ", compute_distance(round_trip(l), store, False))
# lo = ListOrderer(l, 100, 0.1, len(l)/2, seed=True, fast=True, store=store)
# ol = lo.simulated_annealing()

# print("Optimized Distance: ", compute_distance(
#     round_trip(ol), store, False))

# for i in ol:
#     print(f"product_{l.index(i)}", p[f"product_{l.index(i)}"])
# for i in ol:
#     store[i] = 88
#     print(store)
#     time.sleep(0.5)


class GeneticStore():
    def __init__(self):
        pass
