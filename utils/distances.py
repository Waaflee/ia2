def euclidean(point_a, point_b):
    return (
        ((point_a[0] - point_b[0]) ** 2) +
        ((point_a[1] - point_b[1]) ** 2)
    ) ** 0.5 # Euclidean

def manhattan(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1]) # Manhattan
