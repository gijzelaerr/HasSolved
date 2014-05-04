import itertools
import rubik


def solve(work_cube, depth=5):
    """
    naive solver that just tries all moves until `depth` and then
    actually performs the one yielding the shortest manhatten distance
    """
    solved = rubik.cube.Cube()
    while True:
        shortest_dist = float('Inf')
        shortest_cube = None
        for move_set in itertools.product(rubik.cube.moves, repeat=depth):
            move_cube = work_cube.copy()
            for move in move_set:
                getattr(move_cube, move)()

            dist = rubik.cube.cube_distance(move_cube, solved)
            if dist < shortest_dist:
                shortest_dist = dist
                shortest_cube = move_cube
        work_cube = shortest_cube
        print shortest_dist, work_cube