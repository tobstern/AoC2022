from time import perf_counter as pfc

day = "14"
test = 0
if test:
    t = "test_"
else:
    t = ""

#
coords = [
    [tuple(map(int, co.split(","))) for co in pair]
    for pair in [
        l.split(" -> ")
        for l in open(
            "./puzzle_inputs/" + t + "day" + day + ".txt", "r"
        )
        .read()
        .strip()
        .splitlines()
    ]
]


def lines():
    # get all coordinates in between:
    # takes start and end tuple:
    # adds coordinates to grid
    # (500, 0) - (x, y)
    dx, dy = cur[0] - prev[0], cur[1] - prev[1]
    (d, x_y) = (dy, 1) if dx == 0 else (dx, 0)
    if d > 0:
        # increasing order
        li = (
            range(prev[0], prev[0] + d + 1)
            if not x_y
            else range(prev[1], prev[1] + d + 1)
        )
        [
            rocks.add((n, cur[1]))
            if not x_y
            else rocks.add((cur[0], n))
            for n in li
        ]
    if d < 0:
        d = abs(d)
        # "decreasing" order
        li = (
            range(cur[0], cur[0] + d + 1)
            if not x_y
            else range(cur[1], cur[1] + d + 1)
        )
        [
            rocks.add((n, cur[1]))
            if not x_y
            else rocks.add((cur[0], n))
            for n in li
        ]


def move():
    cur_pos = start
    while cur_pos[1] < gsh:
        (x, y) = cur_pos
        # try down:
        if (x, y + 1) not in rocks and (x, y + 1) not in resting:
            cur_pos = (x, y + 1)
        # try left-down
        elif (x - 1, y + 1) not in rocks and (
            x - 1,
            y + 1,
        ) not in resting:
            cur_pos = (x - 1, y + 1)
        # try right-down
        elif (x + 1, y + 1) not in rocks and (
            x + 1,
            y + 1,
        ) not in resting:
            cur_pos = (x + 1, y + 1)
        else:
            if start in resting:
                break
            resting.add(cur_pos)
            cur_pos = start


# Part 1:
start1 = pfc()
# create grid of rocks coordinates: (column, row)
#   + rocks are "#" and air is "."
#   + start is "+" and resting sand is "o"
# behavior of sand:
#   + it moves:
#       + if down possible (no: rock|resting sand)
#           -> continue moving down...
#           -> elif down not possible
#               -> move down_left (diagonal)
#               -> elif move down_left not possible
#                   -> move down right
#
# stop condition - sand to come can not come to rest any more!
#   -> if curent sand position > greatest rock position number (row)
#       -> break.
# => count all resting sand units
start = (500, 0)
rocks = set()
resting = set()
for l in coords:
    for i in range(1, len(l)):
        prev, cur = l[i - 1], l[i]
        lines()

# ->gsh = greatest_stone_height
gsh = max([co[1] for l in coords for co in l])
# move sand:
move()

print(f"Part 1 result is: {len(resting)}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
# new gsh and new resting:
gsh += 2
# ->(g/s)sw = (greatest_/smallest_)stone_width
sw = [co[0] for l in coords for co in l]
gsw, ssw = max(sw), min(sw)
[
    rocks.add((x, gsh))
    for x in range(int(ssw - ssw / 2), int(gsw + gsw / 2))
]
resting = set()
move()
print(f"Part 2 result is: {len(resting)}, t = {pfc() - start2}")
