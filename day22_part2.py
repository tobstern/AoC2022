from time import perf_counter as pfc

test = 1
if test:
    t = "test_"
else:
    t = ""

d = "./puzzle_inputs/" + t + "day22.txt"
for i, l in enumerate(open(d, "r").read().split("\n\n")):

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

# save faces seperately:
cube_max = 50 if not test else 4

fd = {i: [] for i in range(1, 7)}

for i, line in enumerate(grid):

    for j in range(0, len(line), cube_max):

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


# print([len(fd[i]) for i in range(1, 7)])
# f = 5
# print(np.array(fd[f])[-1, :], np.array(fd[f]).shape)
# exit()


def is_wall(next_pos, face):
    # check if wall is next
    y, x = next_pos
    if fd[face][y][x] == "#":
        return True
    else:
        return False


def get_pos(cur_dir, next_dir, cur_pos):
    y, x = cur_pos

    # return y, x
    cd = 4 if cur_dir == 0 else cur_dir
    nd = 4 if next_dir == 0 else next_dir

    # θ = -(nd - cd) * pi / 2
    θ = -(nd - cd) * 90

    # rotate coordinates
    if θ == 0:
        sinθ, cosθ = 0, 1
        # do not change y,x
        yd, xd = y, x

    elif θ == 90 or θ == -270:
        sinθ, cosθ = 1, 0
        yd, xd = x, y % cube_max

    elif θ == -90 or θ == 270:
        sinθ, cosθ = -1, 0
        yd, xd = x % cube_max, y

    elif θ == 180 or θ == -180:
        sinθ, cosθ = 0, -1
        yd, xd = (cube_max - y - 1) % cube_max, (cube_max - x - 1) % cube_max

    # assign depending on next direction
    if next_dir == 0:
        return yd, 0

    if next_dir == 1:
        return 0, xd

    if next_dir == 2:
        return yd, cube_max - 1

    if next_dir == 3:
        return cube_max - 1, xd


# Part 2:
lim = 82
start2 = pfc()
# same rules, but grid changes to cube

# directions = ["r", "d", "l", "u"]
directions = [0, 1, 2, 3]
# select the starting position in the 1st row
# cur_pos = (0, [p for p, g in enumerate(grid[0]) if g != " "][0])
cur_pos = (0, 0)
cur_dir = 0  # start "right" facing
cur_face = 1

# current_face: {current_direction:(next_face, next_direction), ...}, ...
# cube = {cur_face: {cur_dir: (next_face, next_dir)}}
# if abs(cur_dir - next_dir) % 2 != 0 -> swap the y,x coordinates
cube = {
    1: {0: (6, 0), 1: (4, 1), 2: (3, 0), 3: (2, 0)},
    2: {0: (5, 3), 1: (6, 1), 2: (1, 1), 3: (3, 3)},
    3: {0: (5, 0), 1: (2, 1), 2: (1, 0), 3: (4, 0)},
    4: {0: (6, 3), 1: (5, 1), 2: (3, 1), 3: (1, 3)},
    5: {0: (6, 2), 1: (2, 2), 2: (3, 2), 3: (4, 3)},
    6: {0: (5, 2), 1: (4, 2), 2: (1, 2), 3: (2, 3)},
}


# all up-left corners:
corners = {
    1: (0, cube_max),
    2: (3 * cube_max, 0),
    3: (2 * cube_max, 0),
    4: (cube_max, cube_max),
    5: (2 * cube_max, cube_max),
    6: (0, 2 * cube_max),
}

if test:
    cube = {
        1: {0: (6, 2), 1: (4, 1), 2: (3, 1), 3: (2, 1)},
        2: {0: (3, 0), 1: (5, 3), 2: (6, 3), 3: (1, 1)},
        3: {0: (4, 0), 1: (5, 0), 2: (2, 2), 3: (1, 0)},
        4: {0: (6, 1), 1: (5, 1), 2: (3, 2), 3: (1, 3)},
        5: {0: (6, 0), 1: (2, 3), 2: (3, 3), 3: (4, 3)},
        6: {0: (1, 2), 1: (2, 0), 2: (5, 2), 3: (4, 2)},
    }

    corners = {
        1: (0, 2 * cube_max),
        2: (cube_max, 0),
        3: (cube_max, cube_max),
        4: (cube_max, 2 * cube_max),
        5: (2 * cube_max, 2 * cube_max),
        6: (2 * cube_max, 3 * cube_max),
    }
# slice each cube face and save as list of faces (each its grid)
# loop through grid @(cur_dir, cur_face) - watch out for "#" or limit of face
# -> wrap to next_face, next_dir
# at end of instructions -> get "real" position of original grid

for c, i in enumerate(instructions):
    # start at (top left -> get pos after empty space), facing right
    hit = False

    print("\n\n# --", c, "-- #")

    if type(i) == str:
        print("\nfrom cur_dir:", cur_dir)
        # change direction by "90°" - select next direction in directions list
        cur_dir = directions[(cur_dir + 1 if i == "R" else cur_dir - 1) % 4]
        print("rotate to:", cur_dir)

    # elif type(i) == int:
    else:
        # type is int -> steps to go:

        ic = i

        print(
            "\nNext instruction:",
            "cur_pos:",
            cur_pos,
            "steps to make:",
            ic,
            "cur_dir:",
            cur_dir,
            "cur_face:",
            cur_face,
            "\n",
        )
        while ic and not hit:
            y, x = cur_pos

            print(
                "Start the stepping:",
                "cur_pos:",
                cur_pos,
                "steps to make:",
                ic,
                "cur_dir:",
                cur_dir,
                "cur_face:",
                cur_face,
            )

            next_face, next_dir = cube[cur_face][cur_dir]
            # print("cur_dir:", cur_dir, "next_dir:", next_dir)

            # offset for the 'real' coordinates
            oy, ox = corners[cur_face]
            noy, nox = corners[next_face]

            if cur_dir == 0:
                # +x, right

                for j in range(ic):

                    if x + 1 >= cube_max:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        print(
                            "bound - right (0):",
                            "steps made:",
                            j,
                            "before:",
                            (yc + oy, xc + ox),
                            "after:",
                            (y_ + noy, x_ + nox),
                            "next dir:",
                            next_dir,
                            "cur face:",
                            cur_face,
                            "next face:",
                            next_face,
                        )

                        if is_wall((y_, x_), next_face):
                            cur_pos = (y, x) = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            ic = ic - j - 1
                            print(
                                "move to next face:",
                                cur_face,
                                "next_pos:",
                                cur_pos,
                                "next steps to make:",
                                ic,
                                "next_dir",
                                cur_dir,
                            )
                            break

                    if is_wall((y, x + 1), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        print(
                            "Normal stepping - hit wall - made:",
                            j,
                            "steps, ",
                            "@",
                            cur_pos,
                        )
                        break

                    x += 1

            elif cur_dir == 1:
                # +y, down

                for j in range(ic):

                    if y + 1 >= cube_max:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        print(
                            "bound - down (1):",
                            "steps made:",
                            j,
                            "before:",
                            (yc + oy, xc + ox),
                            "after:",
                            (y_ + noy, x_ + nox),
                            "next dir:",
                            next_dir,
                            "cur face:",
                            cur_face,
                            "next face:",
                            next_face,
                        )

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            ic = ic - j - 1
                            print(
                                "move to next face:",
                                cur_face,
                                "next_pos:",
                                cur_pos,
                                "next steps to make:",
                                ic,
                                "next_dir",
                                cur_dir,
                            )
                            break

                    if is_wall((y + 1, x), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        print(
                            "Normal stepping - hit wall - made:",
                            j,
                            "steps, ",
                            "@",
                            cur_pos,
                        )
                        break

                    y += 1

            elif cur_dir == 2:
                # -x, left

                for j in range(ic):

                    if x - 1 < 0:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        print(
                            "bound - left (2):",
                            "steps made:",
                            j,
                            "before:",
                            (yc + oy, xc + ox),
                            "after:",
                            (y_ + noy, x_ + nox),
                            "next dir:",
                            next_dir,
                            "cur face:",
                            cur_face,
                            "next face:",
                            next_face,
                        )

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            ic = ic - j - 1
                            print(
                                "move to next face:",
                                cur_face,
                                "next_pos:",
                                cur_pos,
                                "next steps to make:",
                                ic,
                                "next_dir",
                                cur_dir,
                            )
                            break

                    if is_wall((y, x - 1), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        print(
                            "Normal stepping - hit wall - made:",
                            j,
                            "steps, ",
                            "@",
                            cur_pos,
                        )
                        break

                    x -= 1

            elif cur_dir == 3:
                # -y, up

                for j in range(ic):

                    if y - 1 < 0:
                        # hit the boundary:

                        yc, xc = y, x  # old position
                        y_, x_ = get_pos(cur_dir, next_dir, (y, x))

                        print(
                            "bound - up (3):",
                            "steps made:",
                            j,
                            "before:",
                            (yc + oy, xc + ox),
                            "after:",
                            (y_ + noy, x_ + nox),
                            "next dir:",
                            next_dir,
                            "cur face:",
                            cur_face,
                            "next face:",
                            next_face,
                        )

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            y, x = y_, x_
                            cur_pos = (y, x)
                            ic = ic - j - 1
                            print(
                                "move to next face:",
                                cur_face,
                                "next_pos:",
                                cur_pos,
                                "next steps to make:",
                                ic,
                                "next_dir",
                                cur_dir,
                            )
                            break

                    if is_wall((y - 1, x), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        print(
                            "Normal stepping - hit wall - made:",
                            j,
                            "steps, ",
                            "@",
                            cur_pos,
                        )
                        break
                    y -= 1

            # steps are done - next instruction!
            cur_pos = (y, x)
            if not hit and (j == ic - 1):
                print(
                    "All",
                    j + 1,
                    "steps finished, ",
                    "@",
                    cur_pos,
                )
                break

            continue
    if c == -1:
        print(len(instructions))
        # print(cube)
        exit(0)

print("\nlast_face:", cur_face)

oy, ox = corners[cur_face]
y, x = cur_pos
print("last_pos:", cur_pos)

y, x = cur_pos = oy + y, ox + x

print("direction:", cur_dir, "y-pos:", y + 1, "x-pos:", x + 1)
res = sum([cur_dir, 1000 * (y + 1), 4 * (x + 1)])

print(f"Part 2 result is: {res}, t = {pfc() - start2}")
# 110109 too high -> 107,76 = 108311
