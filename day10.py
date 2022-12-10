from time import perf_counter as pfc
import numpy as np

day = "10"
test = 0
if test:
    # t = "test_"
    t = "test2_"
else:
    t = ""
#
ins = [
    [l.split(" ")[0], int(l.split(" ")[1])] if l != "noop" else l
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]


def is_signal():
    return True if (-20 + cycles) % 40 == 0 else False


def calc_signal():
    return X * cycles


# Part 1:
start1 = pfc()
# count cycles and update the register
# -> calculate the "signal strength"
cycles = 0  # the cycle count
X = 1  # initial value of register X
res1 = 0
for i in ins:
    if i == "noop":
        # -> noop
        cycles += 1
        if is_signal():
            res1 += calc_signal()
    else:
        # it is an operation -> addx
        # it takes 2 cycles,
        # and the register changes after the 2nd cycle
        cycles += 1
        if is_signal():
            res1 += calc_signal()
        cycles += 1
        if is_signal():
            res1 += calc_signal()
        X += i[1]  # change register

print(f"Part 1 result is: {res1}, t = {pfc() - start1}")


def is_lit():
    return True if cycles % 40 in [X - 1, X, X + 1] else False


# Part 2:
start2 = pfc()
# produce message on 6x40 screen (rows x columns)
cycles = -1  # the cycle count
X = 1  # initial value of register X
crt = []
res2 = ""
# len(sprite) is equal to 3 -> ###, mid-point is set by register X
for i in ins:
    if i == "noop":
        # -> noop
        cycles += 1
        crt += [1] if is_lit() else [0]
    else:
        # it is an operation
        # it takes 2 cycles,
        # and the register changes after the 2nd cycle
        cycles += 1
        crt += [1] if is_lit() else [0]
        cycles += 1
        crt += [1] if is_lit() else [0]
        X += i[1]  # change register

res2 = "".join(["#" if d == 1 else "." for d in crt])
res2 = "".join(
    [s + "\n" if (1 + c) % 40 == 0 else s for c, s in enumerate(res2)]
).strip()
print("Part 2 result is:")
print(res2)
print(f"in t = {pfc() - start2}")
