from time import perf_counter as pfc

day = "06"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
i = list(
    open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
)


def has_doubli(li):
    """
    Takes list of characters.
    Checks if contains doublicates.
    Returns bool.
    """
    if len(li) < 1:
        return
    seen = []
    for char in li:
        if char not in seen:
            seen += char
    return 1 if len(seen) < len(li) else 0


# Part 1:
start1 = pfc()
last_four = i[:4].copy()
for pos in range(4, len(i)):
    last_four += i[pos]
    last_four.pop(0)
    if not has_doubli(last_four):
        marker1 = pos + 1
        break

print(f"Part 1 result is: {marker1}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
last_fourteen = i[:14].copy()
for pos in range(14, len(i)):
    last_fourteen += i[pos]
    last_fourteen.pop(0)
    if not has_doubli(last_fourteen):
        marker2 = pos + 1
        break

print(f"Part 2 result is: {marker2}, t = {pfc() - start2}")
