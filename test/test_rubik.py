import unittest
import rubik
import random

class TestRubik(unittest.TestCase):
    def setUp(self):
        self.turned = {
            "left": rubik.cube.Cube("HCDNFVIJELMTPASKUQXZ",
                               "20010200100102010200"),
            "right": rubik.cube.Cube("ACSEMHIDKLUNFQZTPVXJ",
                                "00102001002020102001"),
            "top": rubik.cube.Cube("PKAEFHIJQCMNSLDTUVXZ",
                              "01000000110001000000"),
            "down": rubik.cube.Cube("ACDEFJNZKLIXPQSTUHMV",
                               "00000010001100000010"),
            "front": rubik.cube.Cube("ACDEFHIJKLMNVTPXQZUS",
                                "00000000000000000000"),
            "back": rubik.cube.Cube("DFJCIAEHKLMNPQSTUVXZ",
                               "00000000000000000000"),
        }

    def testTurn(self):
        for direction in ("left", "right", "top", "down", "front", "back"):
            cube = rubik.cube.Cube()
            getattr(cube, direction)()
            self.assertEqual(cube, self.turned[direction])

            cube_turn = rubik.cube.Cube()
            [getattr(cube_turn, direction)() for _ in range(4)]
            self.assertEqual(cube_turn, rubik.cube.Cube())

            cube = self.turned[direction].copy()
            getattr(cube, "anti_" + direction)()
            self.assertEqual(cube, rubik.cube.Cube())

    def testPath(self):
        choices = ["left", "right", "top", "down", "front", "back"]
        m = [random.choice(choices) for _ in xrange(1000)]
        n = ["anti_" + i for i in reversed(m)]
        cube = rubik.Cube()
        for i in m + n:
            getattr(cube, i)()
        self.assertEqual(cube, rubik.Cube())
