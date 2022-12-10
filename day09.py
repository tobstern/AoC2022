from time import perf_counter as pfc
from collections import defaultdict as dd

day = "09"
test = 0
if test:
    # t = "test_"
    t = "test2_"
else:
    t = ""
#
moves = [
    [l.split(" ")[0], int(l.split(" ")[1])]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]


def HTdist(prev_pos, Tpos):
    return list(
        map(
            abs,
            [
                Tpos[-1][0] - prev_pos[-1][0],
                Tpos[-1][1] - prev_pos[-1][1],
            ],
        )
    )


def moveT(Hpos, Tpos):
    # move the Tail
    # find direction and only move by one (build unit vector)
    vec = [
        int(
            (Hpos[-1][p] - Tpos[-1][p]) / abs(Hpos[-1][p] - Tpos[-1][p])
        )
        if Hpos[-1][p] != Tpos[-1][p]
        else 0
        for p in [0, 1]
    ]
    Tpos += [tuple(Tpos[-1][p] + vec[p] for p in [0, 1])]


def sim_rope(d, steps, Hpos, Tpos):
    # takes the direction (d) and the steps count
    # left, right, up, down
    for s in range(1, steps + 1):
        # go left
        if d == "L":
            Hpos += [(Hpos[-1][0], Hpos[-1][1] - 1)]
            HT_dist = HTdist(Hpos, Tpos)
            if HT_dist[1] == 2:
                moveT(Hpos, Tpos)
        # go right
        if d == "R":
            Hpos += [(Hpos[-1][0], Hpos[-1][1] + 1)]
            HT_dist = HTdist(Hpos, Tpos)
            if HT_dist[1] == 2:
                moveT(Hpos, Tpos)
        # go up
        if d == "U":
            Hpos += [(Hpos[-1][0] + 1, Hpos[-1][1])]
            HT_dist = HTdist(Hpos, Tpos)
            if HT_dist[0] == 2:
                moveT(Hpos, Tpos)
        # go down
        if d == "D":
            Hpos += [(Hpos[-1][0] - 1, Hpos[-1][1])]
            HT_dist = HTdist(Hpos, Tpos)
            if HT_dist[0] == 2:
                moveT(Hpos, Tpos)


# Part 1:
start1 = pfc()
# start is s=(0, 0)
Hpos = [(0, 0)]  # Head positions
Tpos = [(0, 0)]  # Tail positions
#
for d, c in moves:
    sim_rope(d, c, Hpos, Tpos)

visited_pos = len(set(Tpos))
print(f"Part 1 result is: {visited_pos}, t = {pfc() - start1}")


def moveT2(prev_pos, Tposes, T):
    # move the Tail
    # it follows its leading knot, respectively
    # find direction and only move by one (build unit vector).
    # check to break the recursion - for the Tails:
    if T > 9:
        # did it reach the end of the tail, yet?
        return

    Tpos = Tposes[T]
    HT_dist = HTdist(prev_pos, Tpos)

    # move to follow the leading knot of the Tail (if 2 steps away)
    if max(HT_dist) == 2:
        vec = [
            int(
                (prev_pos[-1][p] - Tpos[-1][p])
                / abs(prev_pos[-1][p] - Tpos[-1][p])
            )
            if prev_pos[-1][p] != Tpos[-1][p]
            else 0
            for p in [0, 1]
        ]
        Tposes[T] += [tuple(Tpos[-1][p] + vec[p] for p in [0, 1])]
        # move all following tails (that need to move)
        moveT2(Tposes[T], Tposes, T + 1)
    else:
        return


def sim_rope2(d, steps, Hpos, Tposes):
    # takes the direction (d) and the steps count
    # left, right, up, down
    for s in range(1, steps + 1):
        # go left
        if d == "L":
            Hpos += [(Hpos[-1][0], Hpos[-1][1] - 1)]
            HT_dist = HTdist(Hpos, Tposes[1])
            if HT_dist[1] == 2:
                moveT2(Hpos, Tposes, 1)
        # go right
        if d == "R":
            Hpos += [(Hpos[-1][0], Hpos[-1][1] + 1)]
            HT_dist = HTdist(Hpos, Tposes[1])
            if HT_dist[1] == 2:
                moveT2(Hpos, Tposes, 1)
        # go up
        if d == "U":
            Hpos += [(Hpos[-1][0] + 1, Hpos[-1][1])]
            HT_dist = HTdist(Hpos, Tposes[1])
            if HT_dist[0] == 2:
                moveT2(Hpos, Tposes, 1)
        # go down
        if d == "D":
            Hpos += [(Hpos[-1][0] - 1, Hpos[-1][1])]
            HT_dist = HTdist(Hpos, Tposes[1])
            if HT_dist[0] == 2:
                moveT2(Hpos, Tposes, 1)


# Part 2:
# Tail has now 10 knots (H, 1, 2, ..., 9)
start2 = pfc()
# start is still s=(0, 0)
Hpos = [(0, 0)]  # Head positions
Tpos = [(0, 0)]  # Tail positions
Tposes = dd(list)
for T in range(1, 10):
    Tposes[T] = Tpos.copy()
#
for d, c in moves:
    sim_rope2(d, c, Hpos, Tposes)

# find postions, that are visited by the Tails (look at position 9)
visited_pos2 = len(set(Tposes[9]))
print(f"Part 2 result is: {visited_pos2}, t = {pfc() - start2}")
