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


def is_wall(next_pos):
    # check if wall is next
    if grid[next_pos[0]][next_pos[1]] == "#":
        return True
    else:
        return False


def move_cube(i, cur_pos, cur_dir, cur_face):
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
        return cur_pos, cur_dir, cur_face

    elif type(i) == int:
        # check in which direction:
        if cur_dir == 0:
            # right (+x)
            line = [p for p, ele in enumerate(grid[y]) if ele != " "]
            s, e = line[0], line[-1]

            # make amount of steps
            for _ in range(i):
                if (x + 1 - s) % cube_max == 0:
                    # exceeded the line - wrap around !on cube!
                    # decision by modulo cube_max and check on which face
                    # and check cur_dir -> go to next face...
                    # cube = {cur_face: {cur_dir: (next_face, next_dir, start)}}
                    cur_face, cur_dir, start = cube[cur_face][cur_dir]
                    if is_wall((y, start)):
                        return (y, x), cur_dir, cur_face
                    # cur_pos = (y, s)
                    x = s
                    continue
                if is_wall((y, x + 1)):
                    return (y, x), cur_dir, cur_face
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
                        return (y, x), cur_dir, cur_face
                    # cur_pos = (y, e)
                    x = e
                    continue
                if is_wall((y, x - 1)):
                    return (y, x), cur_dir, cur_face
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
                        return (y, x), cur_dir, cur_face
                    # cur_pos = (s, x)
                    y = s
                    continue
                if is_wall((y + 1, x)):
                    return (y, x), cur_dir, cur_face
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
                        return (y, x), cur_dir, cur_face
                    # cur_pos = (e, x)
                    y = e
                    continue
                if is_wall((y - 1, x)):
                    return (y, x), cur_dir, cur_face
                # after all checks done -> assign next position
                y -= 1
            cur_pos = (y, x)
        return cur_pos, cur_dir, cur_face


# Part 2:
start2 = pfc()
# same rules, but grid changes to cube

# directions = ["r", "d", "l", "u"]
directions = [0, 1, 2, 3]
# select the starting position in the 1st row
cur_pos = (0, [p for p, g in enumerate(grid[0]) if g != " "][0])
cur_dir = 0  # start "right" facing
cur_face = 1
cube_max = 50 if not test else 4
# current_face: {current_direction:(next_face, next_direction, x|ystarting point), ...}, ...
# cube = {cur_face: {cur_dir: (next_face, next_dir, start(y, x))}}
# if abs(cur_dir - next_dir) % 2 != 0 -> swap the y,x coordinates
cube = {
    1: {
        0: (6, 0, [0, 0]),
        1: (4, 1, [0, 0]),
        2: (3, 0, [100, -50]),
        3: (2, 0, [150, 0]),
    },
    2: {
        0: (5, 3, [100, -100]),
        1: (6, 1, [-200, 100]),
        2: (1, 1, [0, -100]),
        3: (3, 3, [0, 0]),
    },
    3: {
        0: (5, 0, [0, 0]),
        1: (2, 1, [0, 0]),
        2: (1, 0, [-100, 50]),
        3: (4, 0, [50, -50]),
    },
    4: {
        0: (6, 3, [-50, 50]),
        1: (5, 1, [0, 0]),
        2: (3, 1, [50, -50]),
        3: (1, 3, [0, 0]),
    },
    5: {
        0: (6, 2, [-100, 50]),
        1: (2, 2, [150, -100]),
        2: (3, 2, [0, 0]),
        3: (4, 3, [0, 0]),
    },
    6: {
        0: (5, 2, [100, -50]),
        1: (4, 2, [-50, 50]),
        2: (1, 2, [0, 0]),
        3: (2, 3, [200, -100]),
    },
}

for i in instructions:
    # start at (top left -> get pos after empty space), facing right
    cur_pos, cur_dir, cur_face = move_cube(
        i, cur_pos, cur_dir, cur_face
    )

res = sum([cur_dir, 1000 * (cur_pos[0] + 1), 4 * (cur_pos[1] + 1)])

print(f"Part 2 result is: {res}, t = {pfc() - start2}")
