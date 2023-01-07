from time import perf_counter as pfc
import sys

sys.setrecursionlimit(10**6)

day = "22"
test = 0
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
        instructions = [int(s) if s.isdigit() else s for s in l.split(",")]

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

    elif grid[next_pos[0]][next_pos[1]] == " ":
        print("out of bounds!!!")

    else:
        return False


def move_cube(i, cur_pos, cur_dir, cur_face, last_corner):
    print(
        "initial set:",
        "steps:",
        i,
        "pos:",
        cur_pos,
        "dir:",
        cur_dir,
        "face:",
        cur_face,
        "last corner",
        last_corner,
    )
    # can not move trough walls '#'
    # wrap around (if no wall there)
    # ' ' is no path - place-holder
    # instruction can be int() or char(R|L) -> changing the direction by 90°
    y, x = cur_pos[:]
    # if y < 0 or x < 0:
    #    return cur_pos, cur_dir, cur_face

    if type(i) == str:
        # change direction by "90°" - select next direction in directions list
        cur_dir = directions[(cur_dir + 1 if i == "R" else cur_dir - 1) % 4]
        return cur_pos, cur_dir, cur_face

    elif type(i) == int:
        # check in which direction:
        next_face, next_dir, corner = cube[cur_face][cur_dir]
        if cur_dir == 0:
            # right (+x)
            # make amount of steps
            for j in range(i):
                if x + 1 > last_corner[1] + cube_max:
                    # exceeded the line - wrap around !on cube!
                    # cube = {cur_face: {cur_dir: (next_face, next_dir, corner=(y, x))}}
                    yc, xc = y, x  # old position
                    if abs(cur_dir - next_dir) % 2 != 0:
                        # swap the coordinates (y, x)
                        temp_ = y
                        y = x
                        x = temp_
                    y_ = y % cube_max + corner[0]
                    x_ = x % cube_max + corner[1]
                    print("(at boundary) go right:", y_, x_)
                    if is_wall((y_, x_)):
                        return (yc, xc), cur_dir, cur_face
                    # cur_pos = (y, s)
                    y, x = y_, x_
                    move_cube(i - j - 1, (y, x), next_dir, next_face, corner)
                    break
                    # continue
                print("go right:", y, x)
                if is_wall((y, x + 1)):
                    return (y, x), cur_dir, cur_face
                # after all checks done -> assign next position
                x += 1
            cur_pos = (y, x)

        if cur_dir == 2:
            # left (-x)
            # make amount of steps
            for j in range(i):
                # if x <= 0 or x <= (cube_max - 1) or x <= 2 * (cube_max - 1):
                if x - 1 < last_corner[1] - (cube_max) or x - 1 < 0:
                    # exceeded the line - wrap around !on cube!
                    # cube = {cur_face: {cur_dir: (next_face, next_dir, corner=(y, x))}}
                    yc, xc = y, x  # old position
                    if abs(cur_dir - next_dir) % 2 != 0:
                        # swap the coordinates (y, x)
                        temp_ = y
                        y = x
                        x = temp_
                    y_ = y % cube_max + corner[0]
                    x_ = x % cube_max + corner[1]
                    print("(at boundary) go left:", y_, x_)
                    if is_wall((y_, x_)):
                        return (yc, xc), cur_dir, cur_face
                    # cur_pos = (y, s)
                    y, x = y_, x_
                    # switch now to the next face
                    # if j == i - 1:
                    #     return (y, x), cur_dir, cur_face
                    move_cube(i - j - 1, (y, x), next_dir, next_face, corner)
                    break
                    # continue
                print("go left:", y, x)
                if is_wall((y, x - 1)):
                    return (y, x), cur_dir, cur_face
                # after all checks done -> assign next position
                x -= 1
            cur_pos = (y, x)

        if cur_dir == 1:
            # down (+y)
            # make amount of steps
            for j in range(i):
                if y + 1 > last_corner[0] + cube_max:
                    # exceeded the line - wrap around !on cube!
                    # cube = {cur_face: {cur_dir: (next_face, next_dir, corner=(y, x))}}
                    yc, xc = y, x  # old position
                    if abs(cur_dir - next_dir) % 2 != 0:
                        # swap the coordinates (y, x)
                        temp_ = y
                        y = x
                        x = temp_
                    y_ = y % cube_max + corner[0]
                    x_ = x % cube_max + corner[1]
                    print("(at boundary) go down:", y_, x_)
                    if is_wall((y_, x_)):
                        return (yc, xc), cur_dir, cur_face
                    # cur_pos = (y, s)
                    y, x = y_, x_
                    move_cube(i - j - 1, (y, x), next_dir, next_face, corner)
                    break
                    # continue
                print("go down:", y, x)
                if is_wall((y + 1, x)):
                    return (y, x), cur_dir, cur_face
                # after all checks done -> assign next position
                y += 1
            cur_pos = (y, x)

        if cur_dir == 3:
            # up (-y)
            # make amount of steps
            for j in range(i):
                if y - 1 < last_corner[0] - (cube_max) or y - 1 < 0:
                    # exceeded the line - wrap around !on cube faces!
                    # cube = {cur_face: {cur_dir: (next_face, next_dir, corner=(y, x))}}
                    yc, xc = y, x  # old position
                    if abs(cur_dir - next_dir) % 2 != 0:
                        # swap the coordinates (y, x)
                        temp_ = y
                        y = x
                        x = temp_
                    y_ = y % cube_max + corner[0]
                    x_ = x % cube_max + corner[1]
                    print("(at boundary) go up:", y_, x_)
                    if is_wall((y_, x_)):
                        return (yc, xc), cur_dir, next_face
                    # cur_pos = (y, s)
                    y, x = y_, x_
                    # switch now to the next face
                    # if j == i - 1:
                    #    return (y, x), cur_dir, cur_face
                    move_cube(i - j - 1, (y, x), next_dir, next_face, corner)
                    break
                    # continue
                print("go up:", y, x)
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
# current_face: {current_direction:(next_face, next_direction, x|y corner), ...}, ...
# cube = {cur_face: {cur_dir: (next_face, next_dir, start(y, x))}}
# if abs(cur_dir - next_dir) % 2 != 0 -> swap the y,x coordinates
cube = {
    1: {
        0: (6, 0, [0, 2 * cube_max]),
        1: (4, 1, [cube_max, cube_max]),
        2: (3, 0, [2 * cube_max, 0]),
        3: (2, 0, [3 * cube_max, 0]),
    },
    2: {
        0: (5, 3, [3 * cube_max, cube_max]),
        1: (6, 1, [0, 2 * cube_max]),
        2: (1, 1, [0, cube_max]),
        3: (3, 3, [3 * cube_max, 0]),
    },
    3: {
        0: (5, 0, [2 * cube_max, cube_max]),
        1: (2, 1, [3 * cube_max, 0]),
        2: (1, 0, [0, cube_max]),
        3: (4, 0, [cube_max, cube_max]),
    },
    4: {
        0: (6, 3, [cube_max, 2 * cube_max]),
        1: (5, 1, [2 * cube_max, cube_max]),
        2: (3, 1, [2 * cube_max, 0]),
        3: (1, 3, [cube_max, cube_max]),
    },
    5: {
        0: (6, 2, [0, 3 * cube_max]),
        1: (2, 2, [3 * cube_max, cube_max]),
        2: (3, 2, [2 * cube_max, cube_max]),
        3: (4, 3, [2 * cube_max, cube_max]),
    },
    6: {
        0: (5, 2, [2 * cube_max, 2 * cube_max]),
        1: (4, 2, [cube_max, 2 * cube_max]),
        2: (1, 2, [0, 2 * cube_max]),
        3: (2, 3, [4 * cube_max, 0]),
    },
}

for i in instructions:
    # start at (top left -> get pos after empty space), facing right
    cur_pos, cur_dir, cur_face = move_cube(
        i, cur_pos, cur_dir, cur_face, [0, cube_max - 1]
    )

print("direction:", cur_dir, "y-pos:", cur_pos[0] + 1, "x-pos:", cur_pos[1] + 1)
res = sum([cur_dir, 1000 * (cur_pos[0] + 1), 4 * (cur_pos[1] + 1)])

print(f"Part 2 result is: {res}, t = {pfc() - start2}")
