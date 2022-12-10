from time import perf_counter as pfc
from collections import defaultdict as dd

day = "09"
test = 1
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


def HTdist(Hpos, Tpos):
    return list(
        map(
            abs,
            [Tpos[-1][0] - Hpos[-1][0], Tpos[-1][1] - Hpos[-1][1]],
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


def moveT2(Hpos, Tposes):
    # move the Tail
    # it follows its leading knot, respectively
    # find direction and only move by one (build unit vector)
    Lpos = Hpos.copy()  # Lpos is Leading position
    for T in range(1, 10):
        Tpos = Tposes[T].copy()
        if T > 1:
            Lpos = Tposes[T - 1].copy()
        HT_dist = HTdist(Lpos, Tpos)
        if HT_dist[0] == 2 or HT_dist[1] == 2:
            vec = [
                int(
                    (Lpos[-1][p] - Tpos[-1][p])
                    / abs(Lpos[-1][p] - Tpos[-1][p])
                )
                if Lpos[-1][p] != Tpos[-1][p]
                else 0
                for p in [0, 1]
            ]
            # print(f"The unit vector is: {vec}")
            Tposes[T] += [tuple(Tpos[-1][p] + vec[p] for p in [0, 1])]
            # print(f"The updated Tpositions are: {Tpos}")
        else:
            return
        print(f"Tposes dict is: {Tposes}")


def sim_rope2(d, steps, Hpos, Tpos):
    # takes the direction (d) and the steps count
    # left, right, up, down
    for s in range(1, steps + 1):
        # go left
        if d == "L":
            Hpos += [(Hpos[-1][0], Hpos[-1][1] - 1)]
            moveT2(Hpos, Tposes)
        # go right
        if d == "R":
            Hpos += [(Hpos[-1][0], Hpos[-1][1] + 1)]
            moveT2(Hpos, Tposes)
        # go up
        if d == "U":
            Hpos += [(Hpos[-1][0] + 1, Hpos[-1][1])]
            moveT2(Hpos, Tposes)
        # go down
        if d == "D":
            Hpos += [(Hpos[-1][0] - 1, Hpos[-1][1])]
            moveT2(Hpos, Tposes)


# Part 2:
# Tail has now 10 knots (H, 1, 2, ..., 9)
start2 = pfc()
# start is still s=(0, 0)
Hpos = [(0, 0)]  # Head positions
Tpos = [(0, 0)]  # Tail positions
Tposes = dd(list)
for T in range(1, 10):
    Tposes[T] = Tpos
#
print(Tposes)
for d, c in moves:
    sim_rope2(d, c, Hpos, Tposes)

# find postions, that are visited by all Tails
visited_pos2 = 0
for pos in Tposes[1]:
    print(pos)
    print([1 if pos in Tposes[T] else 0 for T in range(1, 10)])
    l = [1 if pos in Tposes[T] else 0 for T in range(1, 10)]
    if sum(l) == len(l):
        # then the postion has been visited by all knots
        visited_pos2 += 1

print(f"Part 2 result is: {visited_pos2}, t = {pfc() - start2}")
