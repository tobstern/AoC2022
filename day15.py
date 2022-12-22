from time import perf_counter as pfc
import re

day = "15"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
SBs = [
    [
        list(map(int, re.findall(r"-?[0-9]+", l.split(":")[0]))),
        list(map(int, re.findall(r"-?[0-9]+", l.split(":")[1]))),
    ]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]

# Part 1:
start1 = pfc()
# SBs -> [..., [[Sx, Sy], [Bx, By]], ...]
# create all reachable positions by sensors to beacons -> set()
# check the line "2,000,000"
pos = 10 if test else int(2e6)
intervals = []
known = set()

for S, B in SBs:
    # start at sensor position -> delta = |Sx - Bx| + |Sy - By|
    # fill current line (while loop - as long as delta > 1):
    #   -> delta-i (left) & delta - i (right)
    #   -> up as well as down
    # manhatten distance
    d = abs(S[0] - B[0]) + abs(S[1] - B[1])
    o = d - abs(pos - S[1])  # offset = distance - line length

    if o < 0:
        continue

    # boundary range where no other beacons can be
    lx, hx = S[0] - o, S[0] + o

    # save the known beacon position (line=pos) for later:
    if B[1] == pos:
        known.add(B[0])

    # intervals - points that can not exist (start and end point inclusive)
    intervals.append((lx, hx))

intervals.sort()

# all non overlapping intervals
q = []

for lo, hi in intervals:
    # if empty
    if not q:
        q.append([lo, hi])
        continue
    # now check overlaps
    # look at last boundary in q
    qlo, qhi = q[-1]
    # now check if it is not contained in lo<->hi;
    # +1 because doubly inclusive bounds in intervals
    if lo > qhi + 1:
        # if it is not contained already
        q.append([lo, hi])
        continue

    # modify the upper bound in q to "new|greater" boundary
    q[-1][1] = max(qhi, hi)

cannot = set()
for lo, hi in q:
    for x in range(lo, hi + 1):
        cannot.add(x)

print(f"Part 1 result is: {len(cannot-known)}, t = {pfc() - start1}")


# part 2:
# SBs -> [..., [[Sx, Sy], [Bx, By]], ...]
# create all reachable positions by sensors to beacons -> set()
# check the line "2,000,000"
M = 20 if test else int(4e6)

for pos in range(M + 1):
    intervals = []
    for S, B in SBs:
        # start at sensor position -> delta = |Sx - Bx| + |Sy - By|
        # fill current line (while loop - as long as delta > 1):
        #   -> delta-i (left) & delta - i (right)
        #   -> up as well as down
        # manhatten distance
        d = abs(S[0] - B[0]) + abs(S[1] - B[1])
        o = d - abs(pos - S[1])  # offset = distance - line length

        if o < 0:
            continue

        # boundary range where no other beacons can be
        lx, hx = S[0] - o, S[0] + o

        # intervals - points that can not exist (start and end point inclusive)
        intervals.append((lx, hx))

    intervals.sort()

    # all non overlapping intervals
    q = []

    for lo, hi in intervals:
        # if empty
        if not q:
            q.append([lo, hi])
            continue
        # now check overlaps
        # look at last boundary in q
        qlo, qhi = q[-1]
        # now check if it is not contained in lo<->hi;
        # +1 because doubly inclusive bounds in intervals
        if lo > qhi + 1:
            # if it is not contained already
            q.append([lo, hi])
            continue

        # modify the upper bound in q to "new|greater" boundary
        q[-1][1] = max(qhi, hi)
    # print(pos, q)

    # linear search through found intervals:
    x = 0
    for lo, hi in q:
        # if no next interval intersects -> finished
        if x < lo:
            exit(
                f"Part 2 result is: {x * int(4e6) + pos}, t = {pfc() - start1}"
            )
        else:
            # set x to the previous upper boundary + 1
            # x = max(x, hi + 1)
            x = hi + 1
        if x > M:
            # break if exceeding search boundary
            break
