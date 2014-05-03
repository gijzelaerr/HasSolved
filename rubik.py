#!/usr/bin/env python
"""
well, first do it in python

        back
    A----C----D
    |         |\
    E    .    F \
    |         |  \
    H----I----J   \
     \        top  \
      \   K----.----L
       \  |         |\
left    \ .    .    . \   right
         \|         |  \
          M----.----N   \
           \   down      \
            \   P----Q----S
             \  |         |
              \ T    .    U
               \|         |
                V----X----Z

                   front

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

# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
# A C D E F H I J K M  L  N  P  Q  S  T  U  V  X  Z

solved_pos = list("ACDEFHIJKLMNPQSTUVXZ")
solved_orients = len(solved_pos) * ["0"]
indx = {b: a for a, b in enumerate(solved_pos)}


def flip(v):
    """ toggle bool"""
    return str(int(not int(v)))


def rotate(l, s):
    """a -> b -> c -> d -> a"""
    a, b, c, d = [indx[i] for i in s]
    l[b], l[c], l[d], l[a] = l[a], l[b], l[c], l[d]


def cornerflip(orient, codes):
    """flips the bits in orients in position defined in codes"""
    for i in codes:
        pos = indx[i]
        orient[pos] = flip(orient[pos])


def edgeflip(orient, cubes, mapping):
    """ flips cubes in orient given mapping (dict)"
    """
    for cube in cubes:
        pos = indx[cube]
        orient[pos] = str(mapping.get(int(orient[pos]), orient[pos]))


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
        cornerflip(self.orients, "KTNE")
        rotate(self.positions, "HAQV")
        edgeflip(self.orients, "HAQV", {0: 2, 2: 0})

    def anti_left(self):
        rotate(self.positions, "TKEN")
        cornerflip(self.orients, "TKEN")
        rotate(self.positions, "VQAH")
        edgeflip(self.orients, "VQAH", {0: 2, 2: 0})

    def right(self):
        rotate(self.positions, "SDJZ")
        cornerflip(self.orients, "SDJZ")
        rotate(self.positions, "MFPU")
        edgeflip(self.orients, "MFPU", {0: 2, 2: 0})

    def anti_right(self):
        rotate(self.positions, "ZJDS")
        cornerflip(self.orients, "ZJDS")
        rotate(self.positions, "UPFM")
        edgeflip(self.orients, "UPFM", {0: 2, 2: 0})

    def top(self):
        rotate(self.positions, "ADSP")
        rotate(self.positions, "CLQK")
        edgeflip(self.orients, "CLQK", {0: 1, 1: 0})

    def anti_top(self):
        rotate(self.positions, "PSDA")
        rotate(self.positions, "KQLC")
        edgeflip(self.orients, "KQLC", {0: 1, 1: 0})

    def down(self):
        rotate(self.positions, "HVZJ")
        rotate(self.positions, "IMXN")
        edgeflip(self.orients, "IMXN", {0: 1, 1: 0})

    def anti_down(self):
        rotate(self.positions, "JZVH")
        rotate(self.positions, "NXMI")
        edgeflip(self.orients, "NXMI", {0: 1, 1: 0})

    def front(self):
        rotate(self.positions, "PSZV")
        rotate(self.positions, "QUXT")
        edgeflip(self.orients, "QUXT", {1: 2, 2: 1})

    def anti_front(self):
        rotate(self.positions, "VZSP")
        rotate(self.positions, "TXUQ")
        edgeflip(self.orients, "TXUQ", {1: 2, 2: 1})

    def back(self):
        rotate(self.positions, "DAHJ")
        rotate(self.positions, "CEIF")
        edgeflip(self.orients, "CEIF", {1: 2, 2: 1})

    def anti_back(self):
        rotate(self.positions, "JHAD")
        rotate(self.positions, "FIEC")
        edgeflip(self.orients, "FIEC", {1: 2, 2: 1})