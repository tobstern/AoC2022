from time import perf_counter as pfc
import re
import numpy as np

day = "15"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
SBs = [
    [
        list(map(int, re.findall(r"[0-9]+", l.split(":")[0]))),
        list(map(int, re.findall(r"[0-9]+", l.split(":")[1]))),
    ]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]
# print(SBs)


def produce_fields(S, B, fields):
    # start at sensor position -> delta = |Sx - Bx| + |Sy - By|
    # fill current line (while loop - as long as delta > 1):
    #   -> delta-i (left) & delta - i (right)
    #   -> up as well as down
    # manhatten distance
    d = abs(S[0] - B[0]) + abs(S[1] - B[1])
    dx, dy = d, d
    # print(f"1st y: {S[1] - dy} and 2nd y: {S[1] + dy}")
    # print("contains!") if (
    #     S[1] + dy >= pos and S[1] - dy <= pos
    # ) else None
    ll = abs(pos - S[1])  # line length
    if ll <= dx:
        # print("Happend!")
        fields |= set(np.arange(S[0] - dx + ll, S[0] + dx - ll + 1, 1))
        # fields.update(
        #     set(np.arange(S[0] - dx + ll, S[0] + dx - ll + 1, 1))
        # )
        # print(len(fields))
    return fields


# Part 1:
start1 = pfc()
# SBs -> [..., [[Sx, Sy], [Bx, By]], ...]
# create all reachable positions by sensors to beacons -> set()
# check the line "2,000,000"
pos = 10 if test else int(2e6)
fields = set()
for (S, B) in SBs:
    # print(S, B)
    fields = produce_fields(S, B, fields)
    if B[1] == pos:
        fields -= {B[0]}
    # fields -= {S[0]}

print(f"Part 1 result is: {len(fields)}, t = {pfc() - start1}")
# 5441344(|5) too low

# Part 2:
start2 = pfc()
print(f"Part 2 result is: {day}, t = {pfc() - start2}")
