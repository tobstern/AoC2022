from time import perf_counter as pfc
import numpy as np
from tqdm import trange

day = "17"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
jets = [
    1 if j == ">" else -1
    for j in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
]


class Tetris:
    # rock types: -(1,4), +(3,3), L(mirrored-3,3), I(4,1), square(2,2)
    # chamber width = 7
    # rocks start @ 2 from left wall + 3 above floor|highest stone
    # rocks are pushed by jet (left|right), then falling one unit down
    #   -stops when next move down would be rock (+ becomes solid "#"),
    #       -and a new rock starts
    def __init__(self, rock_count):
        # initial chamber size (walls -> left bottom corner @ 0,0)
        self.chamber_width = 7
        # all rock shapes as list
        self.rocks = [
            [1, 1, 1, 1],
            [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
            # this has no rotation symmetrie -> coordinates are-> x=i, y=-j
            [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
            [[1], [1], [1], [1]],
            [[1, 1], [1, 1]],
        ]
        self.highest_pos = [-1] * 7
        self.stones = rock_count

    def move(self, jets):
        jetlen = len(jets)
        jet_pointer = 0
        rock_pointer = 0
        # posses = [
        #     (i, j) for i, j in zip(self.highest_pos.copy(), range(7))
        # ]
        posses = set(
            (i, j) for i, j in zip(self.highest_pos.copy(), range(7))
        )
        # print(posses)
        while self.stones >= 0:
            # for _ in trange(self.stones):
            # move one stone:
            self.stones -= 1
            # print(self.stones)
            stop = False
            rock = self.rocks[rock_pointer % 5]
            # print(f"Current rock is: \n{np.array(rock)}")
            # first rock is just one list:
            if type(rock[0]) == list:
                rock_poss = [
                    (i, j)
                    for i in range(len(rock))
                    for j in range(len(rock[0]))
                    if rock[i][j] == 1
                ]
            else:
                rock_poss = [(0, j) for j in range(len(rock))]
            rock_poss = [
                (i + max(self.highest_pos) + 4, j + 2)
                for (i, j) in rock_poss
            ]
            # print("The starting rock poss:", rock_poss)
            while not stop:
                # move one by jet and one down,
                # if not possible -> stop
                cur_rock_poss = rock_poss.copy()
                horizontal_move = jets[jet_pointer % jetlen]
                cycle_happend = (
                    jet_pointer % jetlen == 0 and rock_pointer % 5 == 0
                )
                print(
                    f"the cycle started newly!"
                ) if cycle_happend else None
                # l_or_r = (
                #     "right"
                #     if jets[jet_pointer % jetlen] == 1
                #     else "left"
                # )
                # print(f"Jet pushes: {l_or_r}")
                jet_pointer += 1
                # move rock horizontally
                rock_poss = []
                for (i, j) in cur_rock_poss:
                    if (
                        j + horizontal_move < 0
                        or j + horizontal_move > 6
                        or (i, j + horizontal_move) in posses
                        # or self.highest_pos[j + horizontal_move] >= i
                    ):
                        rock_poss = cur_rock_poss.copy()
                        break
                    else:
                        rock_poss += [(i, j + horizontal_move)]
                cur_rock_poss = rock_poss.copy()
                # print(
                #     f"Current rock poss after 'hor' move: {cur_rock_poss}"
                # )
                # move rock vertically
                rock_poss = []
                # cur_heights = self.highest_pos
                for pos in cur_rock_poss:
                    if (
                        (pos[0] - 1, pos[1])
                        in posses
                        # self.highest_pos[pos[1]]
                        # == pos[0] - 1
                        # or pos[0] - 1 <= 0
                    ):
                        stop = True
                        # highest = self.highest_pos.copy()
                        # print(f"When stopped moving: {cur_rock_poss}")
                        for (i, j) in cur_rock_poss:
                            # print(f"before stopping: (i={i}, j={j})")
                            if self.highest_pos[j] < i:
                                self.highest_pos[j] = i
                        # print(
                        #     "When stopped moving - highest 'floor' poss:",
                        #     self.highest_pos,
                        # )
                        posses |= set(cur_rock_poss)
                        # posses -= set(list(sorted(posses))[:2])
                        # posses += cur_rock_poss
                        # posses = [
                        #     (i, j)
                        #     for i, j in posses
                        #     if i >= self.highest_pos[j]
                        # ]
                        break
                    else:
                        rock_poss += [(pos[0] - 1, pos[1])]

            # print(f"highest positions: {self.highest_pos}\n")
            rock_pointer += 1
        # h = np.max(posses) + 1
        # grid = np.array([["."] * 7] * (h))
        # for pos in posses:
        #     grid[h - 2 - pos[0], pos[1]] = "#"
        # print(grid)
        # np.max(self.highest_pos) - 1
        # return max(max(posses)) - 2
        return max(self.highest_pos) - 2


# Part 1:
start1 = pfc()
Game = Tetris(rock_count=2022)
# Game = Tetris(rock_count=9)
# print(Game.move(jets))
print(f"Part 1 result is: {Game.move(jets)}, t = {pfc() - start1}")
# 3158 too high

# Part 2:
start2 = pfc()
rock_count = 1000000000000
Game = Tetris(rock_count)
print(f"Part 2 result is: {Game.move(jets)}, t = {pfc() - start2}")
