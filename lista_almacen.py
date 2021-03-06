#!/usr/bin/python
from algorithms.simulated_annealing import ListOrderer, compute_distance
from utils.orders_deprecated import order_generator
from utils.store_generator import generate_store

order_amount = 8
store_size = 3  # Not to big or memory will collapse!
store = generate_store(store_size)
orders = [i for i in order_generator(order_amount, store_size)]

# Correct algorithm
# print("Current Distance: ", compute_distance(orders, store, False))
# lo = ListOrderer(orders, 500, 0.05, 50, seed=True, fast=False, store=store)
# print("Optimized Distance: ", compute_distance(
#     lo.simulated_annealing(), store, False))

# Fast Algorithm
print("Current Distance: ", compute_distance(orders))
lo = ListOrderer(orders, 100, 0.05, 10, seed=True)
print("Optimized Distance: ", compute_distance(
    lo.simulated_annealing()))
