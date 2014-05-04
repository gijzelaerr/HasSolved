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

# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
# A C D E F H I J K M  L  N  P  Q  S  T  U  V  X  Z

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

from random import choice

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
moves += ["anti_" + move for move in moves]


def distance(a, b):
    """return manhatten distance between 2 points"""
    return sum(abs(x - y) for x, y in zip(coords[a], coords[b]))


def cube_distance(cube1, cube2):
    return sum(distance(i, j) for i, j in zip(cube1.positions, cube2.positions))


def flip(v):
    """ toggle bool"""
    return str(int(not int(v)))


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

    def shuffle(self, twists=100):
        for _ in range(twists):
            getattr(self, choice(moves))()

    def _rotate(self, s):
        """a -> b -> c -> d -> a"""
        a, b, c, d = [indx[j] for j in s]
        l = self.positions
        l[b], l[c], l[d], l[a] = l[a], l[b], l[c], l[d]

    def _corner_flip(self, codes):
        """flips the bits in orients in position defined in codes
        """
        for j in codes:
            pos = indx[j]
            self.orients[pos] = flip(self.orients[pos])

    def _edge_flip(self, edges, mapping):
        """ flips cubes in orient given mapping (dict)"
        """
        for edge in edges:
            pos = indx[edge]
            self.orients[pos] = str(mapping.get(int(self.orients[pos]),
                                                self.orients[pos]))

    def _turn(self, corners, edges, flip_map, flip_corners=False):
        self._rotate(corners)
        if flip_corners:
            self._corner_flip(corners)
        self._rotate(edges)
        self._edge_flip(edges, flip_map)

    def left(self):
        self._turn("KTNE", "HAQV", {0: 2, 2: 0}, flip_corners=True)

    def anti_left(self):
        self._turn("TKEN", "VQAH", {0: 2, 2: 0}, flip_corners=True)

    def right(self):
        self._turn("SDJZ", "MFPU", {0: 2, 2: 0}, flip_corners=True)

    def anti_right(self):
        self._turn("ZJDS", "UPFM", {0: 2, 2: 0}, flip_corners=True)

    def top(self):
        self._turn("ADSP", "CLQK", {0: 1, 1: 0})

    def anti_top(self):
        self._turn("PSDA", "KQLC", {0: 1, 1: 0})

    def down(self):
        self._turn("HVZJ", "IMXN", {0: 1, 1: 0})

    def anti_down(self):
        self._turn("JZVH", "NXMI", {0: 1, 1: 0})

    def front(self):
        self._turn("PSZV", "QUXT",  {1: 2, 2: 1})

    def anti_front(self):
        self._turn("VZSP", "TXUQ",  {1: 2, 2: 1})

    def back(self):
        self._turn("DAHJ", "CEIF",  {1: 2, 2: 1})

    def anti_back(self):
        self._turn("JHAD", "FIEC",  {1: 2, 2: 1})
