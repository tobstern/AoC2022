from time import perf_counter as pfc

# Part 2:
start2 = pfc()
# same rules, but grid changes to cube

test = 0
if test:
    t = "test_"
else:
    t = ""

d = "./puzzle_inputs/" + t + "day22.txt"
for i, l in enumerate(open(d, "r").read().split("\n\n")):

    # read grid (i=0) and instructions (i!=0)
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

# save faces seperately:
# cube side length
cube_max = 50 if not test else 4

# faces dictionary
fd = {i: [] for i in range(1, 7)}

for i, line in enumerate(grid):

    for j in range(0, len(line), cube_max):

        # save faces for puzzle input
        if not test and grid[i][j] != " ":

            if i < cube_max and j == cube_max:
                fd[1].append(line[j : j + cube_max])
            elif i < cube_max and j == 2 * cube_max:
                fd[6].append(line[j : j + cube_max])
            elif cube_max <= i < 2 * cube_max and j == cube_max:
                fd[4].append(line[j : j + cube_max])
            elif 2 * cube_max <= i < 3 * cube_max and j == 0:
                fd[3].append(line[j : j + cube_max])
            elif 2 * cube_max <= i < 3 * cube_max and j == cube_max:
                fd[5].append(line[j : j + cube_max])
            elif 3 * cube_max <= i < 4 * cube_max and j == 0:
                fd[2].append(line[j : j + cube_max])

        # save faces for test input
        if test and grid[i][j] != " ":

            if i < cube_max and j == 2 * cube_max:
                fd[1].append(line[j : j + cube_max])
            elif cube_max <= i < 2 * cube_max and j == 0:
                fd[2].append(line[j : j + cube_max])
            elif cube_max <= i < 2 * cube_max and j == cube_max:
                fd[3].append(line[j : j + cube_max])
            elif cube_max <= i < 2 * cube_max and j == 2 * cube_max:
                fd[4].append(line[j : j + cube_max])
            elif 2 * cube_max <= i < 3 * cube_max and j == 2 * cube_max:
                fd[5].append(line[j : j + cube_max])
            elif 2 * cube_max <= i < 3 * cube_max and j == 3 * cube_max:
                fd[6].append(line[j : j + cube_max])


def is_wall(next_pos, face):
    # check if wall is next
    y, x = next_pos
    if fd[face][y][x] == "#":
        return True
    else:
        return False


def get_pos(cur_dir, next_dir, cur_pos):
    # rotate coordinates
    y, x = cur_pos

    # change the 0 direction to 4
    cd = 4 if cur_dir == 0 else cur_dir
    nd = 4 if next_dir == 0 else next_dir

    θ = -(nd - cd) * 90

    if θ == 0:
        # do not change y,x
        yd, xd = y, x

    elif θ == 90 or θ == -270:
        yd, xd = x + 1, y

    elif θ == -90 or θ == 270:
        yd, xd = x, y + 1

    elif θ == 180 or θ == -180:
        yd, xd = cube_max - y - 1, cube_max - x - 1

    # assign depending on next direction
    if next_dir == 0:
        return yd, 0

    if next_dir == 1:
        return 0, xd

    if next_dir == 2:
        return yd, cube_max - 1

    if next_dir == 3:
        return cube_max - 1, xd


# directions = ["r", "d", "l", "u"]
directions = [0, 1, 2, 3]
cur_pos = (0, 0)  # starting position
cur_dir = 0  # start "right" facing
cur_face = 1  # start @ face=1

# hardcoded cube for puzzle input:
cube = {
    1: {0: (6, 0), 1: (4, 1), 2: (3, 0), 3: (2, 0)},
    2: {0: (5, 3), 1: (6, 1), 2: (1, 1), 3: (3, 3)},
    3: {0: (5, 0), 1: (2, 1), 2: (1, 0), 3: (4, 0)},
    4: {0: (6, 3), 1: (5, 1), 2: (3, 1), 3: (1, 3)},
    5: {0: (6, 2), 1: (2, 2), 2: (3, 2), 3: (4, 3)},
    6: {0: (5, 2), 1: (4, 2), 2: (1, 2), 3: (2, 3)},
}


# all up-left (hardcoded) corners for puzzle input:
corners = {
    1: (0, cube_max),
    2: (3 * cube_max, 0),
    3: (2 * cube_max, 0),
    4: (cube_max, cube_max),
    5: (2 * cube_max, cube_max),
    6: (0, 2 * cube_max),
}

if test:

    # hardcoded cube for test input
    cube = {
        1: {0: (6, 2), 1: (4, 1), 2: (3, 1), 3: (2, 1)},
        2: {0: (3, 0), 1: (5, 3), 2: (6, 3), 3: (1, 1)},
        3: {0: (4, 0), 1: (5, 0), 2: (2, 2), 3: (1, 0)},
        4: {0: (6, 1), 1: (5, 1), 2: (3, 2), 3: (1, 3)},
        5: {0: (6, 0), 1: (2, 3), 2: (3, 3), 3: (4, 3)},
        6: {0: (1, 2), 1: (2, 0), 2: (5, 2), 3: (4, 2)},
    }

    # hardcoded corners for test input
    corners = {
        1: (0, 2 * cube_max),
        2: (cube_max, 0),
        3: (cube_max, cube_max),
        4: (cube_max, 2 * cube_max),
        5: (2 * cube_max, 2 * cube_max),
        6: (2 * cube_max, 3 * cube_max),
    }

# -- basic approach -- #

# slice each cube face and save as list of faces (each its grid)
# loop through grid @(cur_dir, cur_face) - watch out for "#" or limit of face
# -> wrap to next_face, next_dir
# at end of instructions -> get "real" position of original grid

# -- \basic approach -- #

# process instructions
for c, i in enumerate(instructions):
    hit = False

    if type(i) == str:
        # change direction by "90°" - select next direction in directions list
        cur_dir = directions[(cur_dir + 1 if i == "R" else cur_dir - 1) % 4]

    else:
        # type is int -> steps to go:

        ic = i

        while ic and not hit:
            y, x = cur_pos

            next_face, next_dir = cube[cur_face][cur_dir]

            if cur_dir == 0:
                # +x, right

                for j in range(ic):

                    if x + 1 >= cube_max:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (y, x) = (yc, xc)
                            hit = True
                            break

                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            break

                    if is_wall((y, x + 1), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break

                    x += 1

            elif cur_dir == 1:
                # +y, down

                for j in range(ic):

                    if y + 1 >= cube_max:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break

                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            break

                    if is_wall((y + 1, x), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break

                    y += 1

            elif cur_dir == 2:
                # -x, left

                for j in range(ic):

                    if x - 1 < 0:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break

                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            break

                    if is_wall((y, x - 1), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break

                    x -= 1

            elif cur_dir == 3:
                # -y, up

                for j in range(ic):

                    if y - 1 < 0:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break

                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            break

                    if is_wall((y - 1, x), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break
                    y -= 1

            # steps are done - next instruction!
            cur_pos = (y, x)

            if not hit and (j >= ic - 1):
                break

            # adjust steps to go for the current instruction
            ic = ic - j - 1

            # continue still @ current instruction
            continue

oy, ox = corners[cur_face]
y, x = cur_pos

y, x = oy + y, ox + x

print("direction:", cur_dir, "y-pos:", y + 1, "x-pos:", x + 1)
res = sum([cur_dir, 1000 * (y + 1), 4 * (x + 1)])

print(f"Part 2 result is: {res}, t = {pfc() - start2}")
