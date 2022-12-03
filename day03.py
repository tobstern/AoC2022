from time import perf_counter as pfc

day = "03"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
i = [
    [list(l[: int(len(l) / 2)]), list(l[int(len(l) / 2) :])]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]


def alph_prio(doublicates):
    return [
        ord(char) - 96 if char.islower() else ord(char) - 38
        for char in doublicates
    ]


# Part 1:
start1 = pfc()
prios = []
for com1, com2 in i:
    double = []
    for char in com2:
        if char in com1 and char not in double:
            double += char
    prios += alph_prio(double)

print(f"Part 1 result is: {sum(prios)}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
i = [com1 + com2 for com1, com2 in i]
prios2 = []
for c in range(0, len(i) - 2, 3):
    common = [
        char for char in i[c] if char in i[c + 1] and char in i[c + 2]
    ][0]
    prios2 += alph_prio(common)

print(f"Part 2 result is: {sum(prios2)}, t = {pfc() - start2}")
