#!/usr/bin/env python
"""
well, first do it in python

(0, 0, 0)  back
    A----C----D
    |         |\
    E    .    F \
    |         |  \
    H----I----J   \
     \        top  \
      \   K----.----L
       \  |         |\
left    \ .    .    . \   right
         \|  down   |  \
          M----.----N   \
           \             \
            \   P----Q----S
             \  |         |
              \ T    .    U
               \|         |
                V----X----Z
                   front   (2, 2, 2)


 * Rotations are defined thusly:
 * For corner cubies:
 *  It is defined to have a rotation of 0 if the white or yellow face
 *  of the cubie is facing front or back.
 *  It is defined to have a rotation of 1 if the white or yellow face
 *  of the cubie is facing left or right.
 *  It is defined to have a rotation of 2 if the white or yellow face
 *  of the cubie is facing up or down.
 * For edge cubies:
 *  All edge cubies have a rotation of 0 in their solved state.  The
 *  rotation of an edge cubie is toggled when it is present on either
 *  the left or the right face, and that face experiences a quarter turn.
 *  Otherwise, the edge rotation remains the same.
"""
import random
import itertools

# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
# A C D E F H I J K M  L  N  P  Q  S  T  U  V  X  Z

solved_pos = list("ACDEFHIJKLMNPQSTUVXZ")
solved_orients = len(solved_pos) * ["0"]
indx = {b: a for a, b in enumerate(solved_pos)}


coords = {
    "A": (0, 0, 0), "C": (1, 0, 0), "D": (2, 0, 0), "E": (0, 1, 0),
    "F": (2, 1, 0), "H": (0, 2, 0), "I": (1, 2, 0), "J": (2, 2, 0),
    "K": (0, 0, 1), "L": (2, 0, 1), "M": (0, 2, 1), "N": (2, 2, 1),
    "P": (0, 0, 2), "Q": (1, 0, 2), "S": (2, 0, 2), "T": (0, 1, 2),
    "U": (2, 1, 2), "V": (0, 2, 2), "X": (1, 2, 2), "Z": (2, 2, 2),
}

moves = ["left", "right", "top", "down", "front", "back"]
moves += ["anti_" + i for i in moves]


def distance(a, b):
    """return manhatten distance between 2 points"""
    return sum(abs(x - y) for x, y in zip(coords[a], coords[b]))


def cube_distance(cube1, cube2):
    return sum(distance(i, j) for i, j in zip(cube1.positions, cube2.positions))


def flip(v):
    """ toggle bool"""
    return str(int(not int(v)))


def shuffle(cube, twists=100):
    for _ in range(twists):
        move = random.choice(moves)
        getattr(cube, move)()


def rotate(l, s):
    """a -> b -> c -> d -> a"""
    a, b, c, d = [indx[i] for i in s]
    l[b], l[c], l[d], l[a] = l[a], l[b], l[c], l[d]


def corner_flip(orient, codes):
    """flips the bits in orients in position defined in codes"""
    for i in codes:
        pos = indx[i]
        orient[pos] = flip(orient[pos])


def edge_flip(orient, cubes, mapping):
    """ flips cubes in orient given mapping (dict)"
    """
    for cube in cubes:
        pos = indx[cube]
        orient[pos] = str(mapping.get(int(orient[pos]), orient[pos]))


def solve(work_cube):
    solved = Cube()
    while True:
        shortest_dist = float('Inf')
        shortest_cube = None
        for move_set in itertools.product(moves, repeat=5):
            move_cube = work_cube.copy()
            for move in move_set:
                getattr(move_cube, move)()

            dist = cube_distance(move_cube, solved)
            if dist < shortest_dist:
                shortest_dist = dist
                shortest_cube = move_cube
        work_cube = shortest_cube
        print shortest_dist, work_cube


def main():
    work_cube = Cube()
    shuffle(work_cube)
    solve(work_cube)


class Cube(object):
    def __init__(self, positions=solved_pos, orients=solved_orients):
        self.positions = list(positions)
        self.orients = list(orients)
        assert len(self.positions) == len(solved_pos)
        assert len(self.orients) == len(solved_pos)

    def copy(self):
        return Cube(self.positions[:], self.orients[:])

    def __eq__(self, other):
        return self.positions == other.positions \
            and self.orients == other.orients

    def __repr__(self):
        return "".join(self.positions + self.orients)

    def left(self):
        rotate(self.positions, "KTNE")
        corner_flip(self.orients, "KTNE")
        rotate(self.positions, "HAQV")
        edge_flip(self.orients, "HAQV", {0: 2, 2: 0})

    def anti_left(self):
        rotate(self.positions, "TKEN")
        corner_flip(self.orients, "TKEN")
        rotate(self.positions, "VQAH")
        edge_flip(self.orients, "VQAH", {0: 2, 2: 0})

    def right(self):
        rotate(self.positions, "SDJZ")
        corner_flip(self.orients, "SDJZ")
        rotate(self.positions, "MFPU")
        edge_flip(self.orients, "MFPU", {0: 2, 2: 0})

    def anti_right(self):
        rotate(self.positions, "ZJDS")
        corner_flip(self.orients, "ZJDS")
        rotate(self.positions, "UPFM")
        edge_flip(self.orients, "UPFM", {0: 2, 2: 0})

    def top(self):
        rotate(self.positions, "ADSP")
        rotate(self.positions, "CLQK")
        edge_flip(self.orients, "CLQK", {0: 1, 1: 0})

    def anti_top(self):
        rotate(self.positions, "PSDA")
        rotate(self.positions, "KQLC")
        edge_flip(self.orients, "KQLC", {0: 1, 1: 0})

    def down(self):
        rotate(self.positions, "HVZJ")
        rotate(self.positions, "IMXN")
        edge_flip(self.orients, "IMXN", {0: 1, 1: 0})

    def anti_down(self):
        rotate(self.positions, "JZVH")
        rotate(self.positions, "NXMI")
        edge_flip(self.orients, "NXMI", {0: 1, 1: 0})

    def front(self):
        rotate(self.positions, "PSZV")
        rotate(self.positions, "QUXT")
        edge_flip(self.orients, "QUXT", {1: 2, 2: 1})

    def anti_front(self):
        rotate(self.positions, "VZSP")
        rotate(self.positions, "TXUQ")
        edge_flip(self.orients, "TXUQ", {1: 2, 2: 1})

    def back(self):
        rotate(self.positions, "DAHJ")
        rotate(self.positions, "CEIF")
        edge_flip(self.orients, "CEIF", {1: 2, 2: 1})

    def anti_back(self):
        rotate(self.positions, "JHAD")
        rotate(self.positions, "FIEC")
        edge_flip(self.orients, "FIEC", {1: 2, 2: 1})


if __name__ == "__main__":
    main()