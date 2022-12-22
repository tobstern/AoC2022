# day12 with the precious video of hyper-neutrino:
# https://youtu.be/xhe79JubaZI?list=PLnNm9syGLD3yf-YW-a5XNh1CJN07xr0Kz
from time import perf_counter as pfc
from collections import deque

day = "12"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
hmap = [
    list(l)
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]

# - Breadth First Search (BFS) - #
# Part 1:
start1 = pfc()
# input is height-map - coded as: a(lowest) to z(highest) spot (S=start=a, E=aim)
# find shortest path from S to E! - use Dijkstra's algorithm –
# note: you can only step on one level higher,
# but multiple level down?
height, width = len(hmap), len(hmap[0])
for i in range(height):
    for j in range(width):
        if hmap[i][j] == "S":
            sr, sc = i, j
            hmap[i][j] = "a"

        if hmap[i][j] == "E":
            er, ec = i, j
            hmap[i][j] = "z"

q = deque()
# init queue: with (starting length, start position row, and s.pos. column)
q.append((0, sr, sc))

# init visisted set
vis = {(sr, sc)}

part1_res = False

while q and not part1_res:
    d, r, c = q.popleft()
    # d(istance), r(ow), c(olumn) in neighbouring nodes
    for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
        # check if in bounds (on map)
        if nr < 0 or nc < 0 or nr >= height or nc >= width:
            # not in bounds:
            continue
        if (nr, nc) in vis:
            # skip node if already visited
            continue
        # and check elevation difference and skip if greater 1
        if ord(hmap[nr][nc]) - ord(hmap[r][c]) > 1:
            continue
        # check if reached the end node (in the neighbours)
        if nr == er and nc == ec:
            print(
                f"Part 1 result is: {d+1}, whole_t = {pfc() - start1}, "
            )
            part1_res = True
            break
        vis.add((nr, nc))
        q.append((d + 1, nr, nc))


# Part 2:
# is almost same, but start at "E" and end at "a" and check if elevation < -1
start2 = pfc()
# do it from the end node to each "a"
q = deque()
# init queue: with (starting length, end position row, and end pos. column)
q.append((0, er, ec))

# init visisted set
vis = {(er, ec)}

while q:
    d, r, c = q.popleft()
    # d(istance), r(ow), c(olumn) in neighbouring nodes
    for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
        # check if in bounds (on map)
        if nr < 0 or nc < 0 or nr >= height or nc >= width:
            # not in bounds:
            continue
        if (nr, nc) in vis:
            # skip node if already visited
            continue
        # and check elevation difference and skip if smaller -1 (go down bigger than 1)
        if ord(hmap[nr][nc]) - ord(hmap[r][c]) < -1:
            continue
        # check if reached the "a" node (in the neighbours)
        if hmap[nr][nc] == "a":
            exit(
                f"Part 2 result is: {d+1}, whole_t = {pfc() - start2}, "
            )
        vis.add((nr, nc))
        q.append((d + 1, nr, nc))
