#!/usr/bin/python
from utils.store_generator import generate_store
from utils.orders import order_generator
from algorithms.astar import Astar
from algorithms.simulated_annealing import SimulatedAnnealing

store_size = 2
orders = list(order_generator(2, store_size))
# start = (10, 6)
# end = (0, 0)
start = orders[0]
end = orders[1]

print("----------------------------")
print("----------------------------")
print("A* implementation")
store = generate_store(store_size)
astar = Astar(store)
path = astar.astar(start, end)
print("Cantidad de pasos: ", len(path))
for i in path:
    store[i.point[0]][i.point[1]] = 88
print(store)

print("----------------------------")
print("----------------------------")
print("Simulated Annealing implementation")
store = generate_store(store_size)
sa = SimulatedAnnealing(store)
path = sa.simulated_annealing(start, end)
print("Cantidad de pasos: ", len(path))
for i in path:
    store[i.point[0]][i.point[1]] = 88
print(store)
