# - with precious help from https://www.youtube.com/watch?v=bLMj50cpOug :) - #
from time import perf_counter as pfc
from collections import deque

day = "16"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
valves = [
    [
        l.split("; ")[0][6:].split(" has flow rate=")[0],
        int(l.split("; ")[0].split("=")[1]),
        l.split("; ")[1].strip().replace(",", "").split(" ")[4:],
    ]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]
# print(valves)
tunnels = {v[0]: v[2] for v in valves}
rates = {v[0]: v[1] for v in valves}
# print(tunnels)
# print(rates)

# Part 1:
start1 = pfc()
# -- Depth First Search (DFS) -- #
# smarter brute-force ;)
dists = {}
nonempty = []

for valve in rates:
    # if a valve is not "AA" and the rate is 0 - skip this valve
    if valve != "AA" and not rates[valve]:
        continue

    if valve != "AA":
        nonempty.append(valve)

    # initialize distances, dict(dist) - "AA" sticks to rate=0
    dists[valve] = {valve: 0, "AA": 0}

    # init visited
    visited = {valve}
    # deque is like opposed to a stack (faster than list)
    queue = deque([(0, valve)])

    while queue:
        # pick valve from beginning of queue
        distance, position = queue.popleft()
        # go through neighbours
        for neigh in tunnels[position]:
            if neigh in visited:
                continue
            visited.add(neigh)
            # if the rate is not 0 - add new distance
            if rates[neigh]:
                dists[valve][neigh] = distance + 1
            queue.append((distance + 1, neigh))

    # - delete them - at the end -> to not revisit them!
    del dists[valve][valve]
    # and if valve ain't "AA", del it too
    if valve != "AA":
        del dists[valve]["AA"]

# print(dists)

indices = {}

for index, elem in enumerate(nonempty):
    indices[elem] = index

# use a cache to not recompute situations in the dfs()
cache = {}


def dfs(time, valve, bitmask):
    if (time, valve, bitmask) in cache:
        return cache[(time, valve, bitmask)]

    # depth first algorithm - with recursion
    maxval = 0
    for neigh in dists[valve]:
        # creates bit of the valve position (in nonempty list)
        # + does bitwise left-shift (for right position -> create offset of 1)
        bit = 1 << indices[neigh]
        # if valve is already open -> skip this neigh
        if bitmask & bit:
            continue
        remtime = time - dists[valve][neigh] - 1
        if remtime <= 0:
            continue
        # recursive calculate the maxval=pressure * remtime
        # in dfs(, bitmask | bit) only the current bit (valve position) will be turned on
        maxval = max(
            maxval,
            dfs(remtime, neigh, bitmask | bit) + rates[neigh] * remtime,
        )

    cache[(time, valve, bitmask)] = maxval
    return maxval


# run dfs() with (30 min, starting @ "AA", no valves open):
print(f"Part 1 result is: {dfs(30, 'AA', 0)}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
# split unblocked valves into 2 sets and me and the elephant go through one of them
# dfs checks the increase of pressure (not total amount)
# current valves are open (do not add anything to flow rate)
# dfs calculates max-released pressure (givin remaining valves)
# b gives end state all valves open
b = (1 << len(nonempty)) - 1
m = 0  # maximum
# elephant and me are not distinguashable -> only need to compute half the bits
#   -> just one second faster

for i in range((b + 1) // 2):
    m = max(m, dfs(26, "AA", i) + dfs(26, "AA", b ^ i))

print(f"Part 2 result is: {m}, t = {pfc() - start2}")
