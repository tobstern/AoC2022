from time import perf_counter as pfc
import numpy as np
from collections import defaultdict as dd

day = "05"
test = 1
if test:
    t = "test_"
else:
    t = ""
#
i = [
    l.splitlines()
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .split("\n\n")
]
# select first and second part of puzzle input
crates, instr = i[0], i[1]

# edit input - crates - to obtain table
crates = np.array([list(c) for c in crates])
# clean it up
crates[(crates == " ") | (crates == "[") | (crates == "]")] = ""
# print(crates)
# get the column numbers of the crates
cols = [j for j, col in enumerate(crates[-1]) if col != ""]
# print(cols)
# rearrange and filter them out
crates = crates[:-1, cols].T
crates_ini = dd(list)
# create dictionary, bacause list are not equal in their length
for j, stack in enumerate(crates):
    crates_ini[j + 1] = list(reversed(list(stack[stack != ""])))
# print(crates_ini)

# edit input - instructions (instr) -
instr = [
    [
        int(
            ins.strip().split(" from ")[0].strip().replace("move ", "")
        ),
        list(
            map(
                int,
                ins.strip().split(" from ")[1].strip().split(" to "),
            )
        ),
    ]
    for ins in instr
]
# print(instr)

# Part 1:
start1 = pfc()
crates1 = crates_ini.copy()
for j, l in enumerate(instr):
    # move x times a crate from start to aim
    x, start, aim = l[0], l[1][0], l[1][1]
    # before adding, reverse the list of crates that are to be
    # transferred
    crates1[aim] += list(reversed(crates1[start][-x:]))
    crates1[start] = crates1[start][:-x]
# print(crates1)
message1 = "".join([vals[-1] for vals in crates1.values()])
print(f"Part 1 result is: {message1}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
print(f"Part 2 result is: {day}, t = {pfc() - start2}")
