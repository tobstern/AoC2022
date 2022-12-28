from time import perf_counter as pfc
import sympy

day = "21"
test = 0
if test:
    t = "test_"
else:
    t = ""
#

monkeys = {
    l.split(": ")[0]: int(l.split(": ")[1].strip())
    if l.split(": ")[1].strip().isdigit()
    else tuple(l.split(": ")[1].split(" "))
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
}


def get_res(m, op):
    # give back the number if it is one
    if type(op) == int or type(op) == float:
        numbers[m] = op
        return int(op)
    # cover the symbolic object for part 2
    elif type(op) != tuple:
        numbers[m] = op
        return op

    # recall the function -> to get the numbers
    monkey1 = get_res(op[0], monkeys[op[0]])
    monkey2 = get_res(op[2], monkeys[op[2]])

    # parse the operation
    if op[0] in numbers and op[2] in numbers:
        if part2 and m == "root":
            exit(
                f"Part 2 result is: {sympy.solve(monkeys[op[0]] - monkeys[op[2]])[0]}, t = {pfc() - start2}"
            )

        if op[1] == "*":
            # multiply monkey numbers
            monkeys[m] = monkey1 * monkey2
        elif op[1] == "/":
            # divide monkey numbers
            monkeys[m] = monkey1 / monkey2
        elif op[1] == "+":
            # add monkey numbers
            monkeys[m] = monkey1 + monkey2
        elif op[1] == "-":
            # subtract monkey numbers
            monkeys[m] = monkey1 - monkey2

    # one monkey or both have to wait -> process later again
    else:
        jobs.append(m)


# Part 1:
part2 = False
jobs = [k for k in monkeys.keys() if type(k) != int]
start1 = pfc()

numbers = {m: d for m, d in monkeys.items() if type(d) == int}

for m in jobs:
    get_res(m, monkeys[m])

print(f"Part 1 result is: {monkeys['root']}, t = {pfc() - start1}")

# Part 2:
monkeys = {
    l.split(": ")[0]: int(l.split(": ")[1].strip())
    if l.split(": ")[1].strip().isdigit()
    else tuple(l.split(": ")[1].split(" "))
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
}

start2 = pfc()
part2 = True

jobs = [k for k in monkeys.keys() if type(k) != int]

numbers = {
    m: d for m, d in monkeys.items() if type(d) == int and m != "humn"
}

# use symbolic function sympy to find the value for "humn"
# for the equality at "root"
numbers["humn"] = sympy.Symbol("x")
monkeys["humn"] = sympy.Symbol("x")

for m in jobs:
    if m in numbers:
        continue
    get_res(m, monkeys[m])
