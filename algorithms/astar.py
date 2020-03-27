from utils.distances import manhattan as distance


class Node():
    def __init__(self, point, f, g, parent):
        self.point = point
        self.f = f
        self.g = g
        self.parent = parent


class Astar():
    def __init__(self, maze):
        self.maze_original = maze
        self.open_list = set()
        self.closed_list = set()

    def astar(self, start, end):
        self.maze = self.maze_original.copy()
        self.start = start
        self.end = end
        self.open_list.add(Node(start, distance(
            start, end), distance(start, end), None))

        while self.open_list:
            current = min(self.open_list, key=lambda x: x.f)
            if current.point == self.end:
                return self.get_path(current)
            self.open_list.remove(current)
            self.closed_list.add(current)
            for node in self.get_children(current):
                if node in self.closed_list:
                    continue
                elif node in self.open_list:
                    pass
                else:
                    # Por algún motivo se guardan con hash diferente entre los 2 sets
                    for i in self.closed_list:
                        if i.point == node.point:
                            break
                    else:
                        self.open_list.add(node)
        return []

    def get_path(self, current):
        path = []
        while current.parent:
            path.append(current)
            current = current.parent
        path.append(current)
        return path[::-1]

    def get_children(self, current):
        x, y = current.point
        childs = []
        for i in [(x-1, y), (x, y - 1), (x, y + 1), (x+1, y)]:
            point = i
            try:
                if (point[0] >= 0 and point[0] < self.maze.shape[0]) and (point[1] >= 0 and point[1] < self.maze.shape[1]):
                    if self.maze[point[0]][point[1]] == 0:
                        g = distance(point, self.start)
                        h = distance(point, self.end)
                        f = g + h
                        child = Node(point, f, g, current)
                        childs.append(child)
                    elif self.maze[point[0]][point[1]] == 1:
                        if point == self.end:
                            g = distance(point, self.start)
                            h = distance(point, self.end)
                            f = g + h
                            return [Node(point, f, g, current)]
                    else:
                        continue
            except IndexError as e:
                print("caught index error")
        return childs
