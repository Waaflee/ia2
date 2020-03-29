import multiprocessing
import random
import numpy as np
from algorithms.simulated_annealing import ListOrderer


def create_order(max, size, uniques=False):
    if uniques:
        new_order = set()
        for i in range(size):
            new_order.add(random.randint(1, max))
        return list(new_order)
    else:
        new_order = []
        for i in range(size):
            new_order.append(random.randint(1, max))
        return new_order


def sort_order(order, store):
    sa = ListOrderer(order_to_points(order, store))
    sorted_order = points_to_order(sa.simulated_annealing(), store)
    return sorted_order


def sort_orders(orders, store):
    with multiprocessing.Pool(processes=len(orders)) as pool:
        sorted_orders = pool.starmap(sort_order, [(i, store) for i in orders])
    return sorted_orders


def array_to_point(array):
    x = array[0][0]
    y = array[1][0]
    return (x, y)


def order_to_points(order, store):
    return [array_to_point(np.where(store == i)) for i in order]


def points_to_order(points, store):
    return [store[i[0]][i[1]] for i in points]
