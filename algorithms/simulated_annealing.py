from utils.distances import manhattan as distance
import random
from math import exp, log


class Node():
    def __init__(self, point, distance, parent):
        self.point = point
        self.distance = distance
        self.parent = parent


class SimulatedAnnealing():
    start = 0
    end = 0
    current = 0

    def __init__(self, maze, Temperature=10**4, cooling_rate=0.003, seed=True):
        # self.maze = []
        self.maze_original = maze
        self.T = Temperature
        self.cooling_rate = cooling_rate
        if seed:
            random.seed()

    def simulated_annealing(self, start, end):
        self.maze = self.maze_original.copy()
        self.start = start
        self.end = end
        self.current = Node(self.start, distance(self.start, self.end), None)
        while self.T > 0.0001:
            # print(self.maze)
            # import time
            # time.sleep(0.05)
            if self.current.point == self.end:
                return self.get_path(self.current)
            else:
                self.current = self.pick(self.get_neighbors(self.current))
                self.update_temp()

        else:
            print("No path founded from ", self.start, " to ", self.end)
            return []

    def update_temp(self):
        self.T *= 1 - self.cooling_rate

    def get_neighbors(self, current):
        x, y = current.point
        childs = []
        for i in [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]:
            point = i
            if (point[0] >= 0 and point[0] < self.maze.shape[0]) and (point[1] >= 0 and point[1] < self.maze.shape[1]):
                if self.maze[point[0]][point[1]] == 0:
                    child = Node(i, distance(current.point, self.end), current)
                    childs.append(child)
                elif self.maze[point[0]][point[1]] == 1:
                    if point == self.end:
                        return [Node(i, distance(current.point, self.end), current)]
                else:
                    continue
        return childs

    def pick(self, list):
        while True:
            try:
                chosen = random.choice(list)
            except IndexError as e:
                return self.current.parent
            if chosen.distance <= self.current.distance:
                self.maze[chosen.point] = 2
                return chosen
            else:
                delta = self.current.distance - chosen.distance
                probability = exp(delta/self.T)
                if random.random() < probability:
                    self.maze[chosen.point] = 2
                    return chosen

    def get_path(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1]
