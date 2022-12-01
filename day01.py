from time import perf_counter as pfc

#
i = [l for l in open("day01.txt", "r").read().strip().split("\n\n")]
cal_sums = [sum(map(int, cal.splitlines())) for cal in i]
#
# Part 1:
start1 = pfc()
biggest = sorted(cal_sums)[-1]
print(f"Part 1 result is: {biggest}, t = {pfc() - start1}")

#
# Part 2:
start2 = pfc()
big_three = sum(sorted(cal_sums)[-3:])
print(f"Part 2 result is: {big_three}, t = {pfc() - start2}")
