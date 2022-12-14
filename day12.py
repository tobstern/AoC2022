from time import perf_counter as pfc
import numpy as np

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
        ord(char) - 96
        if char not in ["S", "E"]
        else 0
        if char == "S"
        else 27
        for char in li
    ]


hmap = np.array(
    [
        o(list(l))
        for l in open(
            "./puzzle_inputs/" + t + "day" + day + ".txt", "r"
        )
        .read()
        .strip()
        .splitlines()
    ]
)


def create_graph():
    """
    Generates graph.
    """
    c = 0
    for l in pos_map:
        for (i, j) in l:
            # position can have all 4 neighbours
            current = (i, j)
            left, right, up, down = (
                (i, j - 1),
                (i, j + 1),
                (i - 1, j),
                (i + 1, j),
            )
            # test if postion exists:
            if left not in flat_pos_map:
                left = []
            if right not in flat_pos_map:
                right = []
            if up not in flat_pos_map:
                up = []
            if down not in flat_pos_map:
                down = []
            neighbours_elevation = [
                {
                    left[0] * width
                    + left[1]: abs(hmap[left] - hmap[current]),
                }
                if left != []
                else None,
                {
                    right[0] * width
                    + right[1]: abs(hmap[right] - hmap[current]),
                }
                if right != []
                else None,
                {up[0] * width + up[1]: abs(hmap[up] - hmap[current])}
                if up != []
                else None,
                {
                    down[0] * width
                    + down[1]: abs(hmap[down] - hmap[current]),
                }
                if down != []
                else None,
            ]
            graph[c] = {
                k: v
                for ele in neighbours_elevation
                if ele != None
                for k, v in ele.items()
            }
            c += 1


def dijkstras(graph, root, dest):
    # (i, j) => node = i * width + j
    paths = [float("inf")] * (width * height)
    # visited = [False] * (width * height)
    adj_nodes = {i: None for i in list(graph.keys())}
    queue = list(graph.keys())
    # set root elevation to 0
    paths[root] = 0

    # loop through queue with all nodes:
    while queue:
        lowest_n = queue[root]
        min_val = paths[lowest_n]
        # loop through all elements in queue
        for n in range(1, len(queue)):
            if (
                paths[queue[n]] <= min_val
                or paths[queue[n]] == min_val + 1
            ):
                lowest_n = queue[n]
                min_val = paths[lowest_n]
        cur = lowest_n
        queue.remove(cur)
        print(cur)

        # now loop through the neighbours and alternate routes:
        for neigh in graph[cur]:
            print("Current node:", cur)
            print("Neighbour:", neigh)
            print("Graph @ cur", graph[cur])
            alternate = graph[cur][neigh] + paths[cur]
            if paths[neigh] > alternate and paths[neigh]:
                paths[neigh] = alternate
                adj_nodes[neigh] = cur

    # show the path and count the steps
    x = dest
    c = 0  # the count of passed nodes
    while True:
        x = adj_nodes[x]
        if x == None:
            print("-Arrived at the top-")
            break
        print(x, end="<-")
        c += 1


# Part 1:
start1 = pfc()
# input is height-map - coded as: a(lowest) to z(highest) spot (S=start=a, E=aim)
# find shortest path from S to E! - use Dijkstra's algorithm –
# note: you can only step on one level higher,
# but multiple level down?
graph = {}
height, width = hmap.shape
# create position tuples for the neighbour search
pos_map = []
for i in range(height):
    help = []
    for j in range(width):
        help += [(i, j)]
    pos_map += [help]
# print(width, height)
print(pos_map)
print(hmap)
flat_pos_map = [pos for l in pos_map for pos in l]
flat_hmap = [h for l in hmap for h in l]
root = list(flat_hmap).index(0)
dest = list(flat_hmap).index(27)

create_graph()
print(graph)

# through all nodes (position as tuples( ))
# (i, j) => node = i * width + j
dijkstras(graph, root, dest)

print(f"Part 1 result is: {day}, t = {pfc() - start1}")

# Part 2:
start2 = pfc()
print(f"Part 2 result is: {day}, t = {pfc() - start2}")
