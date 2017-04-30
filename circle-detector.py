import math
from collections import namedtuple


def enumerate_matrix(matrix):
    for (y, row) in enumerate(matrix):
        for (x, val) in enumerate(row):
            yield ((x, y), val)


def get_topleft(matrix):
    for (pos, val) in enumerate_matrix(matrix):
        if bool(val):
            return pos

    return None


def distance(a, b):
    (ax, ay) = a
    (bx, by) = b

    dx = ax - bx
    dy = ay - by

    return math.sqrt(dx * dx + dy * dy)


Circle = namedtuple('Circle', ('center', 'radius'))


# Assumes circle is rendered by filling in a pixel if the center of the pixel
# is within the radius
def circle_info(matrix):
    def get_matrix(matrix, x, y):
        try:
            return matrix[int(y)][int(x)]
        except IndexError:
            return None

    topleft = get_topleft(matrix)
    (tr_x, tr_y) = topleft
    while bool(get_matrix(matrix, tr_x, tr_y)):
        tr_x += 1

    topright = (tr_x, tr_y)
    topcenter = (
        (topleft[0] + topright[0]) / 2,
        (topleft[1] + topright[1]) / 2,
    )

    (bc_x, bc_y) = topcenter
    while bool(get_matrix(matrix, bc_x, bc_y)):
        bc_y += 1

    center = (bc_x, (topcenter[1] + bc_y) / 2)
    max_radius = (bc_y - topcenter[1]) / 2
    min_radius = max(
        ((bc_y - 1) - (topcenter[1] + 1)) / 2,
        0,
    )

    for ((x, y), val) in enumerate_matrix(matrix):
        dist = distance((x + 0.5, y + 0.5), center)

        if dist < min_radius and not bool(val):
            return None
        elif dist > max_radius and bool(val):
            return None
        else:
            continue

    return Circle(center, (max_radius + min_radius) / 2)


def center_of_points(matrix):
    count = 0
    sum_x = 0.0
    sum_y = 0.0
    for ((x, y), val) in matrix:
        if bool(val):
            sum_x += x
            sum_y += y
            count += 1

    if count == 0:
        return None
    else:
        return (sum_x / count, sum_y / count)


def get_shape_center(matrix):
    circle = circle_info(matrix)
    if circle is None:
        return center_of_points(matrix)
    else:
        return circle.center


print(
    get_shape_center(
        [[0, 0, 1, 0, 0],
         [0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0]]
    )
)
