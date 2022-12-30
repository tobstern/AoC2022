from time import perf_counter as pfc

day = "22"
test = 1
if test:
    t = "test_"
else:
    t = ""
#
for i, l in enumerate(
    open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .split("\n\n")
):
    # grid and instructions
    if i == 0:
        grid = []
        for s in l.split("\n"):
            line = []
            for char in list(s):
                line.append(char if char != " " else " ")
            grid.append(line)
    else:
        # print(l.replace("R", ",R,").replace("L", ",L,"))
        l = l.replace("R", ",R,").replace("L", ",L,")
        instructions = [
            int(s) if s.isdigit() else s for s in l.split(",")
        ]
# for l in grid:
# print(len(l))
# print("".join(l))
# print([len(l) for l in grid])
# print(instructions)
# get all min & max positions
all_rows = []
for j, l in enumerate(grid):
    row_poss = []
    for p, g in enumerate(l):
        if g != "":
            row_poss.append(p)
    all_rows.append((row_poss[0], row_poss[-1]))
# print(all_rows)
# exit()

# Part 1:
start1 = pfc()


def is_wall(next_pos):
    # check if wall is next
    if grid[next_pos[0]][next_pos[1]] == "#":
        return True
    else:
        return False


def move(i, cur_pos, cur_dir):
    # print(i, pos, direction)
    # can not move trough walls '#'
    # wrap around (if no wall there)
    # ' ' is no path - place-holder
    # instruction can be int() or char(R|L) -> changing the direction by 90°
    y, x = cur_pos[:]
    if type(i) == str:
        # change direction by "90°" - select next direction in directions list
        cur_dir = directions[
            (cur_dir + 1 if i == "R" else cur_dir - 1) % 4
        ]
        return cur_pos, cur_dir

    elif type(i) == int:
        # check in which direction:
        if cur_dir == 0:
            # right (+x)
            line = [p for p, ele in enumerate(grid[y]) if ele != " "]
            s, e = line[0], line[-1]

            # make amount of steps
            for _ in range(i):
                if x + 1 > e:
                    # exceeded the line - wrap around
                    if is_wall((y, s)):
                        return (y, x), cur_dir
                    # cur_pos = (y, s)
                    x = s
                    continue
                if is_wall((y, x + 1)):
                    return (y, x), cur_dir
                # after all checks done -> assign next position
                x += 1
            cur_pos = (y, x)

        if cur_dir == 2:
            # left (-x)
            line = [p for p, ele in enumerate(grid[y]) if ele != " "]
            s, e = line[0], line[-1]

            # make amount of steps
            for _ in range(i):
                if x - 1 < s:
                    # exceeded the line - wrap around
                    if is_wall((y, e)):
                        return (y, x), cur_dir
                    # cur_pos = (y, e)
                    x = e
                    continue
                if is_wall((y, x - 1)):
                    return (y, x), cur_dir
                # after all checks done -> assign next position
                x -= 1
            cur_pos = (y, x)

        if cur_dir == 1:
            # down (+y)
            col = [
                j
                for j, l in enumerate(grid)
                if all_rows[j][0] <= x <= all_rows[j][1]
            ]
            line = [p for p in col if grid[p][x] != " "]
            s, e = line[0], line[-1]

            # make amount of steps
            for _ in range(i):
                if y + 1 > e:
                    # exceeded the line - wrap around
                    if is_wall((s, x)):
                        return (y, x), cur_dir
                    # cur_pos = (s, x)
                    y = s
                    continue
                if is_wall((y + 1, x)):
                    return (y, x), cur_dir
                # after all checks done -> assign next position
                y += 1
            cur_pos = (y, x)

        if cur_dir == 3:
            # up (-y)
            col = [
                j
                for j, l in enumerate(grid)
                if all_rows[j][0] <= x <= all_rows[j][1]
            ]
            # line = [p for p, ele in enumerate(col) if ele != ""]
            line = [p for p in col if grid[p][x] != " "]
            s, e = line[0], line[-1]
            m = e - s  # modulus

            # make amount of steps
            for _ in range(i):
                if y - 1 < s:
                    # exceeded the line - wrap around
                    if is_wall((e, x)):
                        return (y, x), cur_dir
                    # cur_pos = (e, x)
                    y = e
                    continue
                if is_wall((y - 1, x)):
                    return (y, x), cur_dir
                # after all checks done -> assign next position
                y -= 1
            cur_pos = (y, x)
        return cur_pos, cur_dir


# directions = ["r", "d", "l", "u"]
directions = [0, 1, 2, 3]
# select the starting position in the 1st row
cur_pos = (0, [p for p, g in enumerate(grid[0]) if g != " "][0])
cur_dir = 0  # start "right" facing

for i in instructions:
    # start at (top left -> get pos after empty space), facing right
    cur_pos, cur_dir = move(i, cur_pos, cur_dir)

res = sum([cur_dir, 1000 * (cur_pos[0] + 1), 4 * (cur_pos[1] + 1)])
print(f"Part 1 result is: {res}, t = {pfc() - start1}")
