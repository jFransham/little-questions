import math


def distance(a, b):
    (ax, ay) = a
    (bx, by) = b

    dx = ax - bx
    dy = ay - by

    return math.sqrt(dx * dx + dy * dy)


def reconstruct(step_back_map, end):
    out = []
    current = end
    while current is not None:
        out.append(current)
        current = step_back_map.get(current)

    out.reverse()

    return out


# Basic A* pathfinding
# Maze is a 2-dimensional list of booleans (or anything implementing the
# list-like dunder methods, you could make an infinite maze if you wanted)
def solve_maze(maze, start, end):
    dead = set()
    live = set([start])

    best_step_back = dict()

    cost_from_start = dict()
    cost_to_end_est = dict()

    cost_from_start[start] = 0
    cost_to_end_est[start] = distance(start, end)

    while any(live):
        closest_to_end = min(
            live,
            key=lambda x: cost_to_end_est.get(x, float('inf'))
        )

        if closest_to_end == end:
            return reconstruct(best_step_back, end)

        live.remove(closest_to_end)
        dead.add(closest_to_end)

        (cx, cy) = closest_to_end

        # No playing smart with iterators, just write it out manually
        neighbors = {
                              (cx,     cy - 1),
            (cx - 1, cy),     (cx,     cy),     (cx + 1, cy),
                              (cx,     cy + 1),
        }

        # We know that cost has to be calculated if we got this from the open
        # set
        cur_cost = cost_from_start[closest_to_end]

        for neighbor in neighbors - dead:
            (x, y) = neighbor

            # HACK: Ideally we'd use a numpy array since it's guaranteed not
            #       to be jagged, but this is a simple solution that only uses
            #       the stdlib and works
            try:
                # Python indexes wrap around so we have to manually check < 0
                if x < 0 or y < 0 or maze[y][x]:
                    continue
            except IndexError:
                continue

            neighbor_cost = cur_cost + distance(closest_to_end, neighbor)

            if neighbor in live and cost_from_start[neighbor] < neighbor_cost:
                continue

            live.add(neighbor)

            best_step_back[neighbor] = closest_to_end
            cost_from_start[neighbor] = neighbor_cost
            cost_to_end_est[neighbor] = neighbor_cost + distance(neighbor, end)

    # Live set was emptied without reaching the end
    return None


def make_maze(inp):
    return [[bool(x) for x in y_list] for y_list in inp]


print(
    solve_maze(
        make_maze(
            [[0, 1, 1, 1, 0],
             [0, 1, 0, 1, 0],
             [0, 1, 0, 0, 0],
             [0, 0, 0, 1, 0]]
        ),
        (0, 0),
        (4, 0),
    )
)
