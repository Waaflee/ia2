#!/usr/bin/python
from algorithms.simulated_annealing import ListOrderer, compute_distance
from utils.orders import order_generator
from utils.store_generator import generate_store

order_amount = 8
store_size = 3  # Not to big or memory will collapse!
store = generate_store(store_size)
orders = [i for i in order_generator(order_amount, store_size)]
print("Current Distance: ", compute_distance(orders, store, False))
lo = ListOrderer(orders, 100, 0.05, 10, seed=True, fast=False, store=store)
print("Optimized Distance: ", compute_distance(
    lo.simulated_annealing(), store, False))
