from time import perf_counter as pfc

day = ""
#
i = [l for l in open("day" + day + ".txt", "r").read().strip().split()]
print(i)
#
def p1():
    return


#
def p2():
    return


#
# Part 1:
start1 = pfc()
print(f"Part 1 result is: {p1()}, t = {pfc() - start1}")
# Part 2:
start2 = pfc()
print(f"Part 2 result is: {p2()}, t = {pfc() - start2}")
