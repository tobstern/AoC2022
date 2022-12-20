from time import perf_counter as pfc
import numpy as np
from collections import defaultdict as dd
import sys

# print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

day = "12"
test = 1
if test:
    t = "test_"
else:
    t = ""
#


def o(li):
    """
    Takes a list of characters.
    Converts to the order (int) in the alphabet.
    Returns list with integers.
    """
    return [
        ord(char) - 97
        if char not in ["S", "E"]
        else "S"
        if char == "S"
        else "E"
        for char in li
    ]


hmap = [
    o(list(l))
    for l in open("./puzzle_inputs/" + t + "day" + day + ".txt", "r")
    .read()
    .strip()
    .splitlines()
]


def add_key(d, key, val):
    if key in d.keys():
        d[key].update(val)
    else:
        d[key] = val


def create_graph():
    """
    Generates graph.
    """
    for i in range(height):
        for j in range(width):
            # position can have all 4 neighbours
            cur = (i, j)
            left, right, up, down = (
                (i, j - 1),
                (i, j + 1),
                (i - 1, j),
                (i + 1, j),
            )
            # test if postion exists:
            if left in flat_pos_map:
                add_key(
                    graph,
                    cur,
                    {left: abs(hmap[left[0]][left[1]] - hmap[i][j])},
                )
            if right in flat_pos_map:
                add_key(
                    graph,
                    cur,
                    {right: abs(hmap[right[0]][right[1]] - hmap[i][j])},
                )
            if up in flat_pos_map:
                add_key(
                    graph,
                    cur,
                    {up: abs(hmap[up[0]][up[1]] - hmap[i][j])},
                )
            if down in flat_pos_map:
                add_key(
                    graph,
                    cur,
                    {down: abs(hmap[down[0]][down[1]] - hmap[i][j])},
                )


def get_path(adj_nodes, node, c):
    # recursively call adjacent nodes till reaching aim:
    # return count
    # print(adj_nodes[node])
    if node == root:  # | adj_nodes[node] == None:
        return c
    c += 1
    c = get_path(adj_nodes, adj_nodes[node], c)
    return c


def dijkstras(graph, root, dest):
    # (i, j) => node = i * width + j
    c = 0  # the count of passed nodes
    paths = {pos: float("inf") for pos in graph.keys()}
    seen = []
    adj_nodes = {i: None for i in list(graph.keys())}
    queue = list(graph.keys())
    # set root elevation to 0
    paths[root] = 0

    # loop through queue with all nodes:
    while queue:
        lowest_n = queue[0]
        min_val = paths[lowest_n]
        # loop through all elements in queue
        for n in range(1, len(queue)):
            if paths[queue[n]] < min_val:
                lowest_n = queue[n]
                min_val = paths[lowest_n]
        cur = lowest_n
        queue.remove(cur)
        # print(cur)

        # now loop through the neighbours and alternate routes:
        # if cur == 27:
        #     break
        for neigh in graph[cur]:
            # print("Current node:", cur)
            # print("Neighbour:", neigh)
            # print("Graph @ cur", graph[cur])
            alternate = paths[cur] + graph[cur][neigh]
            if paths[neigh] > alternate:
                # print(paths[neigh])
                if graph[cur][neigh] < 2:
                    paths[neigh] = alternate
                    adj_nodes[neigh] = cur
                    # c += 1 if cur not in seen else 0
                    # seen += [cur]

    # print(len([v for v in adj_nodes.values() if v != None]))
    # # show the path and count the steps
    # x = dest
    # c = 0  # the count of passed nodes
    # # print("-Started at the top-")
    # while True:
    #     x = adj_nodes[x]
    #     if x == None:
    #         # print("\n-Arrived at the bottom-")
    #         break
    #     # print(x, end="<-")
    #     c += 1 if x != (0, 0) else -1
    # print(adj_nodes)
    return get_path(adj_nodes, dest, 0)


# Part 1:
start1 = pfc()
# input is height-map - coded as: a(lowest) to z(highest) spot (S=start=a, E=aim)
# find shortest path from S to E! - use Dijkstra's algorithm –
# note: you can only step on one level higher,
# but multiple level down?
graph = dd(dict)
height, width = len(hmap), len(hmap[0])
# create position tuples for the neighbour search
# print(width, height)
# print(pos_map)
# print(hmap)
flat_pos_map = [(i, j) for i in range(height) for j in range(width)]
root = [
    (i, j)
    for i in range(height)
    for j in range(width)
    if hmap[i][j] == "S"
][0]
dest = [
    (i, j)
    for i in range(height)
    for j in range(width)
    if hmap[i][j] == "E"
][0]
hmap[root[0]][root[1]] = 0
hmap[dest[0]][dest[1]] = 25
# print(root, dest)

create_graph()
# print(graph)
create_graph_time = pfc()

# through all nodes (position as tuples( ))
c = dijkstras(graph, root, dest)
dijkstras_time = pfc()

print(
    f"Part 1 result is: {c}, whole_t = {pfc() - start1}, "
    + f"graph_creation_time = {pfc() - create_graph_time}, "
    + f"process_dijkstra_time = {pfc() - dijkstras_time}"
)
# 1145 is too high

# Part 2:
start2 = pfc()
print(f"Part 2 result is: {day}, t = {pfc() - start2}")
