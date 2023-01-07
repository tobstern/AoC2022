from time import perf_counter as pfc

day = "25"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
snafus = [
    [int(d) if d.isdigit() else d for d in list(l)]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]


def snafu2dec(fu):
    return sum(
        5**i * d
        if type(d) == int
        else -1 * 5**i
        if d == "-"
        else -2 * 5**i
        for i, d in enumerate(list(reversed(fu)))
    )


def dec2snafu(dec):
    snafu = []

    while dec:
        r = dec % 5
        dec //= 5

        # convert to snafu representation
        if r <= 2:
            snafu.append(r)
            continue

        if r == 4:
            snafu.append("-")
        elif r == 3:
            snafu.append("=")
        dec += 1

    return "".join(list(map(str, reversed(snafu))))


# Part 1:
start1 = pfc()
res_dec = []
for fu in snafus:
    res_dec.append(snafu2dec(fu))

res_dec = sum(res_dec)

print(f"Part 1 result is: {dec2snafu(res_dec)}, t = {pfc() - start1}")
