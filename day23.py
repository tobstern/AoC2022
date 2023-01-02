from time import perf_counter as pfc
from collections import deque
from collections import Counter as C
from copy import deepcopy as dc

day = "23"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
elves = {}
c = -1
for i, l in enumerate(open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")):
    # print(l)
    for j, ele in enumerate(l):
        if ele == "#":
            c += 1
            # is an elve, save its position:
            elves[c] = (i, j)

# print(elves)


def consider(c, elf):
    y, x = elf

    seen = []

    proposal = []

    for dy, dx in adjacents:
        # check all 8 adj:
        if (y + dy, x + dx) not in elves.values():
            # no other elf in any direction -> do nothing
            continue
        seen.append((y + dy, x + dx))

    if len(seen) < 1:
        return proposal

    # look in all directions (in the order of dirs)
    for d in first_valid[c]:
        # print(any([(y + dy, x + dx) in seen for dy, dx in dir_dict[d]]))
        if all([(y + dy, x + dx) not in seen for dy, dx in dir_dict[d]]):
            # there is no elf in these 3 directions
            if d == "N":
                proposal = (y - 1, x)
            if d == "S":
                proposal = (y + 1, x)
            if d == "W":
                proposal = (y, x - 1)
            if d == "E":
                proposal = (y, x + 1)

            # save the considered direction for this elf
            # print(first_valid[c])
            dirs = first_valid[c]
            # print(dirs)
            dirs.remove(d)
            first_valid[c].append(d)
            # print(first_valid[c])
            break
    # now either there is a proposed direction of that elf
    # or it will not move
    # print("proposal", proposal)
    return proposal


# Part 1:
start1 = pfc()

rounds = 10
dir_dict = {
    "N": [(-1, 0), (-1, 1), (-1, -1)],
    "S": [(1, 0), (1, 1), (1, -1)],
    "W": [(0, -1), (-1, -1), (1, -1)],
    "E": [(0, 1), (-1, 1), (1, 1)],
}
# dirs = deque(["N", "S", "W", "E"])
first_valid = {i: deque(["N", "S", "W", "E"]) for i, elf in enumerate(elves)}
# dirs = deque([(-1, 0), (1, 0), (0, -1), (0, 1)])
# adjacents = ["N", "NE", "NW", "S", "SE", "SW", "W", "E"]
adjacents = [
    (-1, 0),
    (-1, 1),
    (-1, -1),
    (1, 0),
    (1, 1),
    (1, -1),
    (0, -1),
    (0, 1),
]


while rounds:
    # consider the move and then move
    propose = {}

    for i, elf in elves.items():
        proposal = consider(i, elf)
        propose[i] = proposal
        # print(propose)

    # make the moves
    # propose_ = dc(propose)
    propose = {
        i: pos
        for i, pos in propose.items()
        if list(propose.values()).count(pos) < 2
    }
    # print(occ)

    # print(propose_)
    for i, pos in propose.items():
        # print(i, pos)
        elves[i] = pos
        # if pos == []:
        #    continue

        # if occ[i] < 2:
        # there are no other elves considering this direction
        # next_elves.append(considered)
        #    elves[i] = pos

    rounds -= 1

# print(elves)

# print the empty ground tiles -> every point in the square - len(elves)
my, mx = float("inf"), float("inf")

My, Mx = -float("inf"), -float("inf")

for y, x in elves.values():
    my, mx = min(my, y), min(mx, x)

    My, Mx = max(My, y), max(Mx, x)

print(My, my, Mx, mx, len(elves.keys()))
empty = (My - my + 1) * (Mx - mx + 1)
# empty = (My - my + 1) * (Mx - mx + 1) - len(elves.keys())


print(f"Part 1 result is: {empty}, t = {pfc() - start1}")
# 3389 too low, 5776 too high,    3544?,

# Part 2:
start2 = pfc()
print(f"Part 2 result is: {day}, t = {pfc() - start2}")
