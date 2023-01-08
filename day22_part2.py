from time import perf_counter as pfc

d = "./puzzle_inputs/day22.txt"
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
cube_max = 50

fd = {i: [] for i in range(1, 7)}

for i, line in enumerate(grid):

    for j in range(0, len(line), cube_max):

        if grid[i][j] != " ":
            # print(i, j)
            if i < 50 and j == 50:
                fd[1].append(line[j : j + cube_max])
            elif i < 50 and j == 100:
                fd[6].append(line[j : j + cube_max])
            elif 50 <= i < 100 and j == 50:
                fd[4].append(line[j : j + cube_max])
            elif 100 <= i < 150 and j == 0:
                fd[3].append(line[j : j + cube_max])
            elif 100 <= i < 150 and j == 50:
                fd[5].append(line[j : j + cube_max])
            elif 150 <= i < 200 and j == 0:
                fd[2].append(line[j : j + cube_max])


# print([len(fd[i]) for i in range(1, 7)])
# exit()


def is_wall(next_pos, face):
    # check if wall is next
    if fd[face][next_pos[0]][next_pos[1]] == "#":
        return True
    else:
        return False


def get_pos(next_dir, cur_pos):
    y, x = cur_pos

    if next_dir == 0:
        return y, 0

    if next_dir == 1:
        return 0, x

    if next_dir == 2:
        return y, cube_max - 1

    if next_dir == 3:
        return cube_max - 1, x


# Part 2:
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
    1: (0, 50),
    2: (150, 0),
    3: (100, 0),
    4: (50, 50),
    5: (100, 50),
    6: (0, 100),
}

# slice each cube face and save as list of faces (each its grid)
# loop through grid @(cur_dir, cur_face) - watch out for "#" or limit of face
# -> wrap to next_face, next_dir
# at end of instructions -> get "real" position of original grid

for i in instructions:
    # start at (top left -> get pos after empty space), facing right
    if type(i) == str:
        # change direction by "90°" - select next direction in directions list
        cur_dir = directions[(cur_dir + 1 if i == "R" else cur_dir - 1) % 4]

    else:
        # type is int -> steps to go:
        hit = False
        ic = i

        while not hit:
            y, x = cur_pos

            # if ic <= 0:
            #    break

            if cur_dir == 0:
                # +x, right
                for j in range(ic):

                    if x + 1 >= cube_max:
                        # hit the boundary:
                        next_face, next_dir = cube[cur_face][cur_dir]

                        yc, xc = y, x  # old position
                        if abs(cur_dir - next_dir) % 2 != 0:
                            # swap the coordinates (y, x)
                            temp_ = y
                            y = x
                            x = temp_
                        y_, x_ = get_pos(next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            cur_pos = (y_, x_)
                            ic -= j
                            break

                    if is_wall((y, x + 1), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break

                    x += 1

                else:
                    # steps are done - next instruction!
                    cur_pos = (y, x)
                    break

            elif cur_dir == 1:
                # +y, down
                for j in range(ic):

                    if y + 1 >= cube_max:
                        # hit the boundary:
                        next_face, next_dir = cube[cur_face][cur_dir]

                        yc, xc = y, x  # old position
                        if abs(cur_dir - next_dir) % 2 != 0:
                            # swap the coordinates (y, x)
                            temp_ = y
                            y = x
                            x = temp_
                        y_, x_ = get_pos(next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            cur_pos = (y_, x_)
                            ic -= j
                            break

                    if is_wall((y + 1, x), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break

                    y += 1

                else:
                    # steps are done - next instruction!
                    cur_pos = (y, x)
                    break

            elif cur_dir == 2:
                # -x, left
                for j in range(ic):

                    if x - 1 < 0:
                        # hit the boundary:
                        next_face, next_dir = cube[cur_face][cur_dir]

                        yc, xc = y, x  # old position
                        if abs(cur_dir - next_dir) % 2 != 0:
                            # swap the coordinates (y, x)
                            temp_ = y
                            y = x
                            x = temp_
                        y_, x_ = get_pos(next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            cur_pos = (y_, x_)
                            ic -= j
                            break

                    if is_wall((y, x - 1), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break

                    x -= 1

                else:
                    # steps are done - next instruction!
                    cur_pos = (y, x)
                    break

            elif cur_dir == 3:
                # -y, up
                for j in range(ic):

                    if y - 1 < 0:
                        # hit the boundary:
                        next_face, next_dir = cube[cur_face][cur_dir]

                        yc, xc = y, x  # old position
                        if abs(cur_dir - next_dir) % 2 != 0:
                            # swap the coordinates (y, x)
                            temp_ = y
                            y = x
                            x = temp_
                        y_, x_ = get_pos(next_dir, (y, x))

                        if is_wall((y_, x_), next_face):
                            cur_pos = (yc, xc)
                            hit = True
                            break
                        else:
                            cur_face = next_face
                            cur_dir = next_dir
                            cur_pos = (y_, x_)
                            ic -= j
                            break

                    if is_wall((y - 1, x), cur_face):
                        # stop @ previous
                        cur_pos = (y, x)
                        hit = True
                        break

                    y -= 1

                else:
                    # steps are done - next instruction!
                    cur_pos = (y, x)
                    break

print("cur_face:", cur_face)

oy, ox = corners[cur_face]
y, x = cur_pos

cur_pos = oy + y, ox + x

print("direction:", cur_dir, "y-pos:", cur_pos[0] + 1, "x-pos:", cur_pos[1] + 1)
res = sum([cur_dir, 1000 * (cur_pos[0] + 1), 4 * (cur_pos[1] + 1)])

print(f"Part 2 result is: {res}, t = {pfc() - start2}")
# 110109 too high -> 107,76 = 108311
