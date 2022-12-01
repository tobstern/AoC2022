from time import perf_counter as pfc

day = ""
#
i = [l for l in open("day" + day + ".txt", "r").read().strip().split()]
print(i)

# Part 1:
start1 = pfc()
print(f"Part 1 result is: {day}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
print(f"Part 2 result is: {day}, t = {pfc() - start2}")
