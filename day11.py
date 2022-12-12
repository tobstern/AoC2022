from time import perf_counter as pfc
from collections import defaultdict as dd
import re
import numpy as np

day = "11"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
ins = [
    l.splitlines()
    for l in [
        m.strip()
        for m in open(
            "./puzzle_inputs/" + t + "day" + day + ".txt", "r"
        )
        .read()
        .strip()
        .split("\n\n")
    ]
]
# print(ins)


class Monkeys:
    """
    The behavior of stuff-slinging simian shenanigans:
    + monkeys hold items -> list(worry levels),
    + they operate the item -> algebraic worry level operation (-> new worry level),
    + (the current operated item gets boring -> int(worry level / 3)),
    + they throw the item to another monkey -> if new worry level % integer == 0 (divisible?)
    leads to decision between 2 monkeys -> i.e.: append the item to the items list of that monkey.
    """

    # initialize all monkeys
    def __init__(self, m_description):
        # initialize dictionaries
        self.mnkys, self.ops, self.tests, self.total_items = (
            dd(list),
            dd(str),
            dd(list),
            dd(int),
        )
        for m in m_description:
            # save the items to each monkey
            num = int(re.search(r"[0-9]", m[0]).group(0))
            self.mnkys[num] += list(
                map(int, re.findall(r"[0-9]+", m[1]))
            )
            # parse operation (op=string) later
            self.ops[num] = m[2].split(": ")[1]
            # the test has structure:
            # [int for divisible test,
            # dict(True:int of monkey, False:int of monkey)]
            self.tests[num] += [
                int(re.search(r"[0-9]+", m[3]).group(0)),
                {True: int(m[4][-1]), False: int(m[5][-1])},
            ]
            self.total_items[num] = 0
        # -> monkeys have been parsed by now!
        self.worry_divisor = np.prod(
            [n[0] for n in self.tests.values()]
        )

    def parse_op(self, name, old_level):
        # parse the operation instruction of monkey (num)
        op = self.ops[name]
        is_number = re.search(r"[0-9]+", op)
        num = int(is_number.group()) if is_number != None else is_number
        if num == None:
            # the worry level must be squared
            new_level = old_level * old_level
        elif "+" in op:
            new_level = old_level + num
        elif "*" in op:
            new_level = old_level * num
        return new_level

    def play(self, rounds, part):
        # each r in the loop is 1 round of the game (play till r=20),
        # each m is one monkey:
        for r in range(1, rounds + 1):
            # print(f"Round: {r}")
            for m in self.mnkys.keys():
                # print(f"Monkey: {m}")
                if len(self.mnkys[m]) < 1:
                    # there is no item - skip this monkey
                    continue
                self.total_items[m] += len(self.mnkys[m])
                for i in self.mnkys[m]:
                    # process all items:
                    new_level = self.parse_op(m, i)
                    # we need to worry less, monkey gets bored
                    # -> by 3
                    new_level = (
                        int(new_level / 3)
                        if part == 1
                        else int(new_level % self.worry_divisor)
                    )
                    # check where to throw
                    t = self.tests[m]
                    if new_level % t[0] == 0:
                        # it is divisible be the number t[0]
                        b = True
                    else:
                        # it is not divisible
                        b = False
                    aim = t[1][b]
                    self.mnkys[aim] += [new_level]
                    # cut-off old worry level of current monkey
                    self.mnkys[m] = self.mnkys[m][:-1].copy()
        # all rounds have been played
        # find most active monkeys -> level of monkey business
        order = list(sorted(self.total_items.values()))[-2:]
        # there should be only 2 top-ranking monkeys selected
        return order[0] * order[1]


# Part 1:
start1 = pfc()
KeepAway = Monkeys(ins)
monkey_business = KeepAway.play(rounds=20, part=1)
print(f"Part 1 result is: {monkey_business}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
KeepAway = Monkeys(ins)
monkey_business = KeepAway.play(rounds=10000, part=2)
print(f"Part 2 result is: {monkey_business}, t = {pfc() - start2}")
