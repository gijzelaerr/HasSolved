#!/usr/bin/env python

import rubik
from rubik.solve import solve


def main():
    work_cube = rubik.cube.Cube()
    work_cube.shuffle()
    solve(work_cube, depth=5)


if __name__ == "__main__":
    main()