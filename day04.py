from time import perf_counter as pfc

day = "04"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
i = [
    [
        list(map(int, l.split(",")[0].split("-"))),
        list(map(int, l.split(",")[1].split("-"))),
    ]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]

# Part 1:
start1 = pfc()
cont_fully = 0
for sec1, sec2 in i:
    if (sec1[0] >= sec2[0] and sec1[1] <= sec2[1]) or (
        sec2[0] >= sec1[0] and sec2[1] <= sec1[1]
    ):
        cont_fully += 1

print(f"Part 1 result is: {cont_fully}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
overlaps = 0
for sec1, sec2 in i:
    if (
        (sec1[0] >= sec2[0] and sec1[0] <= sec2[1])
        or (sec1[1] >= sec2[0] and sec1[1] <= sec2[1])
        or (sec2[0] >= sec1[0] and sec2[0] <= sec1[1])
        or (sec2[1] >= sec1[0] and sec2[1] <= sec1[1])
    ):
        overlaps += 1

print(f"Part 2 result is: {overlaps}, t = {pfc() - start2}")
