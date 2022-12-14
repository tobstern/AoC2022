from time import perf_counter as pfc
import ast

day = "13"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
packets = [
    [
        ast.literal_eval(l.split("\n")[0]),
        ast.literal_eval(l.split("\n")[1]),
    ]
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .split("\n\n")
]


def compare(outer_left, outer_right):
    """
    This function compares the packets of each group (2 each).
    + left value == right value -> continue to next | if left < right -> right order
        -> else (it is not in right order)
    + left value || right value having different type -> list & int:
        -> replace int by list(int) and call compare function again
    + both values are list -> go in and compare 1st to 1st, 2nd to 2nd...
    + if left list == [] before right list -> right order
        -> else not right order
    """
    listlen = max(len(outer_left), len(outer_right))
    for i in range(listlen):
        # reached the limit of either left or right
        if i >= len(outer_left):
            return 1
        if i >= len(outer_right):
            return 0
        left = outer_left[i]
        right = outer_right[i]
        # test on element type and do required steps
        ordered = -1
        if type(left) == int and type(right) == int:
            # both are integer - compare them
            if left < right:
                # has right order
                ordered = 1
            elif left > right:
                # does not have right order
                ordered = 0
            else:
                # no difference - can not make decision - continue
                ordered = -1
                continue
        elif type(left) == list and type(right) == list:
            # both are lists - go in, call own function (recursion)
            ordered = compare(left, right)
        elif type(left) == list and type(right) == int:
            # has different type (list|int)
            right = [right]
            # print(f"Mixed types - retry!")
            ordered = compare(left, right)
        elif type(left) == int and type(right) == list:
            # has different type (int|list)
            left = [left]
            # print(f"Mixed types - retry!")
            ordered = compare(left, right)
        if ordered != -1:
            return ordered
    # if end of list is reached:
    return -1


# Part 1:
start1 = pfc()
p1, res1 = 0, 0
all_pairs = []
for pair in packets:
    p1 += 1
    # print(f"\n# -- Current pair is: {p1} -- #")
    is_right = compare(pair[0], pair[1])
    res1 += p1 if is_right else 0
    all_pairs += [pair[0], pair[1]] if is_right else [pair[0], pair[1]]
    # print("Is it right?:", "yes" if is_right else "no")
print(f"Part 1 result is: {res1}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
decoder_key = (
    1 + sum(1 for item in all_pairs if compare(item, [[2]]) == 1)
) * (2 + sum(1 for item in all_pairs if compare(item, [[6]]) == 1))
print(f"Part 2 result is: {decoder_key}, t = {pfc() - start2}")
