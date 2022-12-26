from time import perf_counter as pfc

# using doubly linked list
class Node:
    #
    def __init__(self, n):
        # backward and forward pointer
        self.left = None
        self.right = None
        self.number = n


day = "20"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
numbers = [
    Node(int(l.strip()))
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]


# Part 1:
# cyclic right(positive), left(negative) shifts
# input in a list (needs to be ordered)
# result is the 1000, 2000, 3000 step - number after the 0.
start1 = pfc()

L = len(numbers)
m = L - 1

for i in range(L):
    numbers[i].right = numbers[(i + 1) % L]
    numbers[i].left = numbers[(i - 1) % L]

for o in numbers:
    # take position of zero
    if o.number == 0:
        z = o
        continue

    node = o
    if o.number > 0:
        for _ in range(o.number % m):
            node = node.right
        # will not work if o == node
        if o == node:
            continue
        # delete old elem - change pointer of both sides
        o.right.left = o.left
        o.left.right = o.right
        # add the elem to the right of the next index
        node.right.left = o
        # pointer of last node to the next node (next index)
        o.right = node.right
        node.right = o
        o.left = node
    else:
        for _ in range(-o.number % m):
            node = node.left
        # will not work if o == node
        if o == node:
            continue
        # delete old elem - change pointer of both sides
        o.left.right = o.right
        o.right.left = o.left
        # add the elem to the right of the next index
        node.left.right = o
        # pointer of last node to the next node (next index)
        o.left = node.left
        node.left = o
        o.right = node

res = 0

for _ in range(3):
    for _ in range(1000):
        # right node of the zero
        z = z.right
    res += z.number

print(f"Part 1 result is: {res}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
dec_key = 811589153
numbers = [
    Node(int(l.strip()) * dec_key)
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]

for i in range(L):
    numbers[i].right = numbers[(i + 1) % L]
    numbers[i].left = numbers[(i - 1) % L]

for _ in range(10):
    for o in numbers:
        # take position of zero
        if o.number == 0:
            z = o
            continue

        node = o
        if o.number > 0:
            for _ in range(o.number % m):
                node = node.right
            # will not work if o == node
            if o == node:
                continue
            # delete old elem - change pointer of both sides
            o.right.left = o.left
            o.left.right = o.right
            # add the elem to the right of the next index
            node.right.left = o
            # pointer of last node to the next node (next index)
            o.right = node.right
            node.right = o
            o.left = node
        else:
            for _ in range(-o.number % m):
                node = node.left
            # will not work if o == node
            if o == node:
                continue
            # delete old elem - change pointer of both sides
            o.left.right = o.right
            o.right.left = o.left
            # add the elem to the right of the next index
            node.left.right = o
            # pointer of last node to the next node (next index)
            o.left = node.left
            node.left = o
            o.right = node

res2 = 0

for _ in range(3):
    for _ in range(1000):
        # right node of the zero
        z = z.right
    res2 += z.number
    print(z.number)

print(f"Part 2 result is: {res2}, t = {pfc() - start2}")
