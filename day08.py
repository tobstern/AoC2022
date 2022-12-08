from time import perf_counter as pfc
import numpy as np

day = "08"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
grid = np.array(
    [
        list(l)
        for l in open(
            "./puzzle_inputs/" + t + "day" + day + ".txt", "r"
        )
        .read()
        .strip()
        .splitlines()
    ],
    dtype=int,
)


def viewable(row, col):
    # look left & right
    # and look up and down (except for the current tree)
    curr_tree = grid[row, col]
    if (
        np.sum(grid[row, :col] >= curr_tree) >= 1
        and np.sum(grid[row, col + 1 :] >= curr_tree) >= 1
        and np.sum(grid[:row, col] >= curr_tree) >= 1
        and np.sum(grid[row + 1 :, col] >= curr_tree) >= 1
    ):
        # the tree can not be seen
        return False
    else:
        # tree can be seen
        return True


# Part 1:
start1 = pfc()
# find all visible trees (looking from edges)
N = len(grid)
visible = 4 * (N - 1)  # count of visible edges
# print(visible)
for row in range(1, N - 1):
    for col in range(1, N - 1):
        # test if viewable from edges:
        if viewable(row, col):
            visible += 1

print(f"Part 1 result is: {visible}, t = {pfc() - start1}")


def scenic_score(row, col):
    # returns the count of visible trees
    # looking right, left, up, down
    score = 1
    curr_tree = grid[row, col]
    left = grid[row, :col] >= curr_tree
    right = grid[row, col + 1 :] >= curr_tree
    up = grid[:row, col] >= curr_tree
    down = grid[row + 1 :, col] >= curr_tree
    # left:
    c = 0
    for i in range(len(left) - 1, -1, -1):
        if len(left) < 1:
            break
        c += 1
        if left[i] == True:
            break
    score *= c
    # up:
    c = 0
    for i in range(len(up) - 1, -1, -1):
        if len(up) < 1:
            break
        c += 1
        if up[i] == True:
            break
    score *= c
    # right:
    c = 0
    for i in range(len(right)):
        if len(right) < 1:
            break
        c += 1
        if right[i] == True:
            break
    score *= c
    # down:
    c = 0
    for i in range(len(down)):
        if len(down) < 1:
            break
        c += 1
        if down[i] == True:
            break
    score *= c
    return [score]


# Part 2:
start2 = pfc()
# find the highest scenic score (most trees visible) of any tree
N = len(grid)
scores = []
for row in range(N):
    for col in range(N):
        # count visible trees:
        scores += scenic_score(row, col)

print(f"Part 2 result is: {max(scores)}, t = {pfc() - start2}")
