import unittest
import rubik


class TestRubik(unittest.TestCase):
    def setUp(self):
        self.turned = {
            "left": rubik.Cube("HCDNFVIJELMTPASKUQXZ",
                               "20010200100102010200"),
            "right": rubik.Cube("ACSEMHIDKLUNFQZTPVXJ",
                                "00102001002020102001"),
            "top": rubik.Cube("PKAEFHIJQCMNSLDTUVXZ",
                              "01000000110001000000"),
            "down": rubik.Cube("ACDEFJNZKLIXPQSTUHMV",
                               "00000010001100000010"),
            "front": rubik.Cube("ACDEFHIJKLMNVTPXQZUS",
                                "00000000000000000000"),
            "back": rubik.Cube("DFJCIAEHKLMNPQSTUVXZ",
                               "00000000000000000000"),
        }

    def testTurn(self):
        for direction in ("left", "right", "top", "down", "front", "back"):
            cube = rubik.Cube()
            getattr(cube, direction)()
            self.assertEqual(cube, self.turned[direction])

            cube_turn = rubik.Cube()
            [getattr(cube_turn, direction)() for _ in range(4)]
            self.assertEqual(cube_turn, rubik.Cube())

            cube = self.turned[direction].copy()
            getattr(cube, "anti_" + direction)()
            self.assertEqual(cube, rubik.Cube())
