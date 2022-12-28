from time import perf_counter as pfc
from collections import deque

day = "18"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
cubes = [
    tuple(map(int, l.split(",")))
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]


def adjacents(cube, cubes, c):
    adj = [-1, 1]
    x, y, z = cube
    for a in adj:
        # look if cube's adjacent is not in cubes - then count it
        if (x + a, y, z) not in cubes:
            c += 1
        if (x, y + a, z) not in cubes:
            c += 1
        if (x, y, z + a) not in cubes:
            c += 1
    return c


# Part 1:
start1 = pfc()
# count up the surface area - 6 sides each (max_area = 6 * len(cubes))
# s_area = max_area - adjacents not in cubes
c = 0
for cube in cubes:
    c += adjacents(cube, cubes, 0)

print(f"Part 1 result is: {c}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
surface = {}

offsets = [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (0, 0, -1),
    (0, -1, 0),
    (-1, 0, 0),
]

mx = my = mz = float("inf")
Mx = My = Mz = -float("inf")

droplet = set()

for cube in cubes:
    x, y, z = cube
    droplet.add(cube)

    # bounding box
    mx = min(mx, x)
    my = min(my, y)
    mz = min(mz, z)

    Mx = max(Mx, x)
    My = max(My, y)
    Mz = max(Mz, z)
    for dx, dy, dz in offsets:
        adj = (x + dx / 2, y + dy / 2, z + dz / 2)
        if adj not in surface:
            surface[adj] = 0
        surface[adj] += 1

# print(list(surface.values()).count(1))

# extend the bounding box
mx -= 1
my -= 1
mz -= 1

Mx += 1
My += 1
Mz += 1

q = deque([(mx, my, mz)])
air = {(mx, my, mz)}

# pathfind around the droplet
while q:
    x, y, z = q.popleft()

    for dx, dy, dz in offsets:
        nx, ny, nz = adj = (x + dx, y + dy, z + dz)

        # if it is not inside bounding box -> skip
        if not (mx <= nx <= Mx and my <= ny <= My and mz <= nz <= Mz):
            continue

        # if it is air (is visited) or one of the droplet cubes -> skip too
        if adj in droplet or adj in air:
            continue

        air.add(adj)
        q.append(adj)

# now having all available air outside -> find the faces facing air :)
free = set()

for x, y, z in air:
    for dx, dy, dz in offsets:
        free.add((x + dx / 2, y + dy / 2, z + dz / 2))

res = 0

# look if air is adjacent to a cube
for key in surface:
    if key in free:
        res += 1

print(f"Part 2 result is: {res}, t = {pfc() - start2}")
# 1042 too low, 3444 too high, 4408 too high, not 2097, not 2698,
