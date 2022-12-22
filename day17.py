from time import perf_counter as pfc

day = "17"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
jets = [
    1 if j == ">" else -1
    for j in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
]

# rocks with complex numbers (imaginary part for the height)
rocks = [
    [0, 1, 2, 3],
    [1, 1j, 1 + 1j, 2 + 1j, 1 + 2j],
    [0, 1, 2, 2 + 1j, 2 + 2j],
    [0, 1j, 2j, 3j],
    [0, 1, 1j, 1 + 1j],
]


solid = {x - 1j for x in range(7)}
height = 0

# Part 1:
start1 = pfc()
rc = 0

ri = 0  # rock index
# rock starts @ x+2 and y+3 (here y is imaginary)
rock = {x + 2 + (height + 3) * 1j for x in rocks[ri]}

while rc < 2022:
    for jet in jets:
        # move the rock by the jet
        moved = {x + jet for x in rock}
        # check bounds -> if move possible: rock = moved
        if all(0 <= x.real < 7 for x in moved) and not (moved & solid):
            rock = moved
        # try to move down:
        moved = {x - 1j for x in rock}
        # is move down possible:
        if moved & solid:
            solid |= rock
            # when rock gets solid -> update rock_count
            rc += 1
            # update the height to highest rock (first layer is row 0)
            height = max(x.imag for x in solid) + 1
            # when reached limit of rocks
            if rc >= 2022:
                break
            ri = (ri + 1) % 5
            # set coordinates of the next rock
            rock = {x + 2 + (height + 3) * 1j for x in rocks[ri]}
        else:
            rock = moved


print(f"Part 1 result is: {int(height)}, t = {pfc() - start1}")


# Part 2:
start2 = pfc()
solid = {x - 1j for x in range(7)}
height = 0


def summarize():
    # look what height the top rock each column is
    o = [-20] * 7

    for x in solid:
        r = int(x.real)
        i = int(x.imag)
        o[r] = max(o[r], i)

    top = max(o)
    return tuple(x - top for x in o)


rc = 0

ri = 0  # rock index
# rock starts @ x+2 and y+3 (here y is imaginary)
rock = {x + 2 + (height + 3) * 1j for x in rocks[ri]}

T = int(1e12)

seen = {}
while rc < T:
    for ji, jet in enumerate(jets):
        # move the rock by the jet
        moved = {x + jet for x in rock}
        # check bounds -> if move possible: rock = moved
        if all(0 <= x.real < 7 for x in moved) and not (moved & solid):
            rock = moved
        # try to move down:
        moved = {x - 1j for x in rock}
        # is move down possible?
        if moved & solid:
            solid |= rock
            # when rock gets solid -> update rock_count
            rc += 1
            # update the height to highest rock (first layer is row 0)
            height = max(x.imag for x in solid) + 1
            # when reached limit of rocks
            if rc >= T:
                break
            ri = (ri + 1) % 5
            # set coordinates of the next rock
            rock = {x + 2 + (height + 3) * 1j for x in rocks[ri]}
            # save a key to memorize + optimize
            key = (ji, ri, summarize())
            if key in seen:
                # get last_rock_count and last_height
                lrc, lh = seen[key]
                rem = T - rc  # remainder, how many rocks to go
                rep = rem // (rc - lrc)  # repetition cycle
                # offset to extrapolate the resulting height
                # (based on current height difference and remainder)
                # if it is the correct one -> could jump to end.
                offset = rep * (height - lh)
                # set rock_count respectively
                rc += rep * (rc - lrc)
                seen = {}  # delete the seen set
            seen[key] = (rc, height)
        else:
            rock = moved
# the current height plus the calculated offset would be the total height,
# with the extrapolation correct.
print(f"Part 2 result is: {int(height + offset)}, t = {pfc() - start2}")
