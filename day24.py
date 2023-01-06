from time import perf_counter as pfc
from collections import deque
import math

day = "24"
test = 0
if test:
    t = "test2_"
else:
    t = ""

# positions as complex numbers (y=imaginary, x=real)

blizzards = tuple(set() for _ in range(4))

arrows = "^v<>"

for y, l in enumerate(
    open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .splitlines()[1:]
):
    for x, tile in enumerate(l[1:]):
        pos = x + y * 1j

        # save initial positions of blizzards
        if tile in arrows:
            for p, arrow in enumerate(arrows):
                if tile == arrow:
                    blizzards[p].add(pos)

# the values (max_col and max_row) of the last iteration of the for loops
Mx, My = (x, y)

S = 1  # start position
E = (Mx - 1) + My * 1j  # end position

y, x = My, Mx
lcm = x * y // math.gcd(y, x)

# Part 1:
start1 = pfc()

finished = False

q = deque()
q.append((0, S))  # (time, position)

seen = set()

neighbours = (-1j, 1j, -1, 1, 0)

while q:
    time, cur = q.popleft()

    time += 1

    for neigh in neighbours:
        ne = cur + neigh

        if ne == E:
            # aim is a neighbour:
            print(
                f"Finished! -> Part 1 result is: {time}, t = {pfc() - start1}"
            )

            finished = True
            break

        if (
            ne.real < 0 or ne.imag < 0 or ne.real >= Mx or ne.imag >= My
        ) and not (ne == S):
            continue

        # -> move yourself (by the time) - instead of the blizzards
        # arrows = "^v<>"
        for i, di, dr in ((0, -1, 0), (1, 1, 0), (2, 0, -1), (3, 0, 1)):
            if ((ne.imag - di * time) % My) * 1j + (
                ne.real - dr * time
            ) % Mx in blizzards[i]:
                break
        else:
            # can move there

            key = (ne, time % lcm)

            if key in seen:
                continue

            seen.add(key)

            ele = (time, ne)
            if ele not in q:
                q.append(ele)

    if finished:
        break

# Part 2:
start2 = pfc()

# bring the elf its snacks, rescue him (there, back, there)!
start = (S, E, S)
end = (E, S, E)
time = 0
for r in range(3):

    finished = False

    q = deque()
    q.append((time, start[r]))  # (time, position)

    seen = set()

    neighbours = (-1j, 1j, -1, 1, 0)

    while q:
        time, cur = q.popleft()

        time += 1

        for neigh in neighbours:
            ne = cur + neigh

            if ne == end[r]:
                # aim is a neighbour:
                print(
                    f"Finished! -> Part 2 -> way: {r}, needed time is: {time}, t = {pfc() - start2}"
                )

                finished = True
                break

            if (
                ne.real < 0 or ne.imag < 0 or ne.real >= Mx or ne.imag >= My
            ) and not (ne == S):
                continue

            # -> move yourself (by the time) - instead of the blizzards
            # arrows = "^v<>"
            for i, di, dr in ((0, -1, 0), (1, 1, 0), (2, 0, -1), (3, 0, 1)):
                if ((ne.imag - di * time) % My) * 1j + (
                    ne.real - dr * time
                ) % Mx in blizzards[i]:
                    break
            else:
                # can move there

                key = (ne, time % lcm)

                if key in seen:
                    continue

                seen.add(key)

                ele = (time, ne)
                if ele not in q:
                    q.append(ele)

        if finished:
            break
