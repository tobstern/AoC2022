from time import perf_counter as pfc
from collections import defaultdict as dd

day = "07"
test = 0
if test:
    t = "test_"
else:
    t = ""
#
# parse the commands and create a dictionary of directories
# and their files:
path = ""
dirs = dd(list)
ls_executed = False
with open("./puzzle_inputs/" + t + "day" + day + ".txt", "r") as txt:
    for line in txt:
        cmd = line.strip().split(" ")
        if line[0] == "$":
            ls_executed = False
            # it is a command
            if cmd[1] == "cd":
                if cmd[2] != "..":
                    # go into directory
                    if cmd[2] != "/":
                        path += cmd[-1] + "/"
                    else:
                        path = "/"
                else:
                    # go out of directory
                    # here is an empty string occuring
                    # - select [:-2]
                    path = "/".join(path.split("/")[:-2]) + "/"
            elif cmd[1] == "ls":
                # second occuring command - ls:
                ls_executed = True
        elif ls_executed:
            # now see, if there are more directories and/or files
            if cmd[0] == "dir":
                # there is a directory
                dirs[path] += [cmd[1]]
            else:
                # there is a file
                fname = cmd[1]
                dirs[path] += [[int(cmd[0]), fname]]


def count_size(d, fs, s):
    # count the sizes of all files and containing directories
    # recursively
    # return list of sizes of those directories
    for f in fs:
        # print(f"for dir: {d} and the files: {fs} and the size: {s}")
        if len(f) == 2:
            # it is a file
            s += [f[0]]
        else:
            # it is a directory -> go into it and sum up its files
            new_d = d + f + "/"
            count_size(new_d, dirs[new_d], s)

    return s


# Part 1:
start1 = pfc()
# find all directories that are: size <= 100,000
siz = []
for d, fs in dirs.items():
    siz += [sum(count_size(d, fs, []))]

res1 = sum([s for s in siz if s <= 100000])

print(f"Part 1 result is: {res1}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
# find "smallest" directory that frees up enough space
# to have > 30,000,000:
max_space = int(70e6)
least_space = int(30e6)
used_space = siz[0]
available_space = max_space - used_space
needed_space = least_space - available_space
for d, fs in dirs.items():
    # find size of all directories (reuse siz of part 1)
    dsize = min([s for s in siz if s > needed_space])

print(f"Part 2 result is: {dsize}, t = {pfc() - start2}")
