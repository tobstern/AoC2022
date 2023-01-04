from time import perf_counter as pfc

day = "23"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
elves = set()
for i, l in enumerate(open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")):
    # print(l)
    for j, ele in enumerate(l):
        if ele == "#":
            # is an elve, save its position:
            elves.add((i, j))

# print(elves)

# Part 1:
start1 = pfc()

dir_dict = {
    (-1, 0): [(-1, 0), (-1, 1), (-1, -1)],
    (1, 0): [(1, 0), (1, 1), (1, -1)],
    (0, -1): [(0, -1), (-1, -1), (1, -1)],
    (0, 1): [(0, 1), (-1, 1), (1, 1)],
}
# dirs = deque(["N", "S", "W", "E"])
# dirs = {i: deque(["N", "S", "W", "E"]) for i, elf in enumerate(elves)}
# dirs = deque(["N", "S", "W", "E"])
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
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


for _ in range(10):
    # consider the move and then move
    propose = set()
    propose_double = set()

    for elf in elves:
        y, x = elf
        if all((y + dy, x + dx) not in elves for dy, dx in adjacents):
            # has no neighbours -> skip elf
            continue

        # look in all directions (in the order of dirs)
        for d in dirs:
            if all((y + dy, x + dx) not in elves for dy, dx in dir_dict[d]):
                dy, dx = d
                proposal = (y + dy, x + dx)
                # there is no elf in these 3 directions
                # save the considered direction for this elf
                if proposal in propose_double:
                    pass
                elif proposal in propose:
                    # doublicate
                    propose_double.add(proposal)
                else:
                    # consider(elf)
                    propose.add(proposal)
                break

    # make the moves
    elves_c = set(elves)

    for elf in elves_c:
        y, x = elf
        if all((y + dy, x + dx) not in elves_c for dy, dx in adjacents):
            # has no neighbours -> skip elf
            continue

        for d in dirs:
            # if in direction d and its diagonals is no elf
            if all((y + dy, x + dx) not in elves_c for dy, dx in dir_dict[d]):
                # move the elf
                dy, dx = d
                next_move = (y + dy, x + dx)
                if next_move not in propose_double:
                    # move the elve to the next position
                    elves.remove(elf)
                    elves.add(next_move)
                break

    dirs.append(dirs.pop(0))

# min and max values for the bounding box
my, mx = float("inf"), float("inf")

My, Mx = -float("inf"), -float("inf")

for y, x in elves:
    my, mx = min(my, y), min(mx, x)

    My, Mx = max(My, y), max(Mx, x)

# number of empty tiles
empty = (My - my + 1) * (Mx - mx + 1) - len(elves)

print(f"Part 1 result is: {empty}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()

elves = set()
for i, l in enumerate(open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")):
    # print(l)
    for j, ele in enumerate(l):
        if ele == "#":
            # is an elve, save its position:
            elves.add((i, j))


dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

rounds = 0

last_elves = set(elves)

while True:
    # consider the move and then move
    propose = set()
    propose_double = set()

    for elf in elves:
        y, x = elf
        if all((y + dy, x + dx) not in elves for dy, dx in adjacents):
            # has no neighbours -> skip elf
            continue

        # look in all directions (in the order of dirs)
        for d in dirs:
            if all((y + dy, x + dx) not in elves for dy, dx in dir_dict[d]):
                dy, dx = d
                proposal = (y + dy, x + dx)
                # there is no elf in these 3 directions
                # save the considered direction for this elf
                if proposal in propose_double:
                    pass
                elif proposal in propose:
                    # doublicate
                    propose_double.add(proposal)
                else:
                    # consider(elf)
                    propose.add(proposal)
                break

    # make the moves
    elves_c = set(elves)

    for elf in elves_c:
        y, x = elf
        if all((y + dy, x + dx) not in elves_c for dy, dx in adjacents):
            # has no neighbours -> skip elf
            continue

        for d in dirs:
            # if in direction d and its diagonals is no elf
            if all((y + dy, x + dx) not in elves_c for dy, dx in dir_dict[d]):
                # move the elf
                dy, dx = d
                next_move = (y + dy, x + dx)
                if next_move not in propose_double:
                    # move the elve to the next position
                    elves.remove(elf)
                    elves.add(next_move)
                break

    dirs.append(dirs.pop(0))

    rounds += 1

    # the previous and the current sets are equal -> no further movement
    if last_elves == elves:
        break

    last_elves = set(elves)


print(f"Part 2 result is: {rounds}, t = {pfc() - start2}")
