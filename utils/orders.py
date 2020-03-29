import multiprocessing
import random
import numpy as np
from algorithms.simulated_annealing import ListOrderer


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


def sort_order(order, store):
    sa = ListOrderer(order_to_points(order, store))
    return points_to_order(sa.simulated_annealing(), store)


def sort_orders(orders, store):
    # pool = multiprocessing.Pool(len(orders))
    # return list(zip(*pool.starmap(sort_order, [(i, store) for i in orders])))
    with multiprocessing.Pool(processes=3) as pool:
        return list(zip(*pool.starmap(sort_order, [(i, store) for i in orders])))


def array_to_point(array):
    x = array[0][0]
    y = array[1][0]
    return (x, y)


def order_to_points(order, store):
    return [array_to_point(np.where(store == i)) for i in order]


def points_to_order(points, store):
    return [store[i[0]][i[1]] for i in points]
