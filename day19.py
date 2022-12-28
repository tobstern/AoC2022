from time import perf_counter as pfc
import re

day = "19"
test = 0
if test:
    test = "test_"
else:
    test = ""
# (help from hyper-neutrino) - part 2: ~70 s (cpython) and ~15 s (pypy3)

# filter robot types and its components:
# robots = C(ore=1, clay=0, obsidian=0)  # one ore robot at beginning
# the count of resources (ore, clay, obsidian, geode)
# factory = C(ore=0, clay=0, obsidian=0, geode=0)
# print(factory["ore"])


def dfs(bp, maxspend, cache, time, amt_bots, amt_resources):
    # if the time is up, give back amount of geodes
    if time == 0:
        return amt_resources[3]

    # preparing key for the cache
    key = tuple([time, *amt_bots, *amt_resources])
    if key in cache:
        return cache[key]

    # 5 options: build ore|clay|obsidian|geode-robot | do nothing
    # maxval of geodes: currently + geode producing bots * remaining time
    maxval = amt_resources[3] + amt_bots[3] * time

    for bot_type, recipe in enumerate(bp):
        # check if more of this bot-type is needed
        if bot_type != 3 and amt_bots[bot_type] >= maxspend[bot_type]:
            continue

        # !optimization! - determine how long it will take
        wait = 0
        # resource amount, resource type
        for ramt, rtype in recipe:
            # see how long to wait
            if amt_bots[rtype] == 0:
                # with no bot - nothing to build
                break
            # ceil division - double negation (rounding towards zero)
            wait = max(
                wait,
                -(-(ramt - amt_resources[rtype]) // amt_bots[rtype]),
            )
        # else statement after loop runs,
        # if loop did not break (else is "last iteration" and skipped if loop breaks:
        else:
            remtime = time - wait - 1
            if remtime <= 0:
                # if there will be no time left - no need to build a robot
                continue
            # clone list
            bots_ = amt_bots[:]
            # amount of material we have after wait minutes
            # skip ahead to wait minutes
            amt_ = [
                x + y * (wait + 1)
                for x, y in zip(amt_resources, amt_bots)
            ]
            # and build the bots and decrease the resources needed:
            for ramt, rtype in recipe:
                amt_[rtype] -= ramt
            bots_[bot_type] += 1

            # !optimization! throw away excess resources (from Jonathan)
            for i in range(3):
                amt_[i] = min(amt_[i], maxspend[i] * remtime)
            # do the dfs():
            maxval = max(
                maxval, dfs(bp, maxspend, cache, remtime, bots_, amt_)
            )

    # at end - save key and maxval(geodes) in cache:
    cache[key] = maxval
    return maxval


# Part 1:
# - Depth First Search (DFS) - #

start1 = pfc()

res = 0

for i, l in enumerate(
    open("./puzzle_inputs/" + test + "day" + day + ".txt", "r")
):
    bp = []
    maxspend = [0, 0, 0]
    for section in l.split(": ")[1].split(". "):
        recipe = []
        # print(section)
        for num, t in re.findall(r"([0-9]+) ([a-z]+)", section):
            num = int(num)
            # t=type ordered by index
            t = ["ore", "clay", "obsidian"].index(t)
            recipe.append((num, t))
        bp.append(recipe)
        maxspend[t] = max(maxspend[t], num)
    # print(bp, maxspend)
    # get amount of g=geodes back of the dsf()
    g = dfs(bp, maxspend, {}, 24, [1, 0, 0, 0], [0, 0, 0, 0])
    res += (i + 1) * g

print(f"Part 1 result is: {res}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()

res = 1

for i, l in enumerate(
    open("./puzzle_inputs/" + test + "day" + day + ".txt", "r")
):
    if i > 2:
        break
    bp = []
    maxspend = [0, 0, 0]
    for section in l.split(": ")[1].split(". "):
        recipe = []
        # print(section)
        for num, t in re.findall(r"([0-9]+) ([a-z]+)", section):
            num = int(num)
            # t=type ordered by index
            t = ["ore", "clay", "obsidian"].index(t)
            recipe.append((num, t))
        bp.append(recipe)
        maxspend[t] = max(maxspend[t], num)
    # print(bp, maxspend)
    # get amount of g=geodes back of the dsf()
    g = dfs(bp, maxspend, {}, 32, [1, 0, 0, 0], [0, 0, 0, 0])
    res *= g

print(f"Part 2 result is: {res}, t = {pfc() - start2}")
