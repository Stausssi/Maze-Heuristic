from Open import OpenHeap

test = OpenHeap()

test.push("Node 1", 1.0)
test.push("Node 2", 30.1)
test.push("Node 3", 10.5)
test.push("Node 4", 2.0)

for i in range(4):
    print(test.pop_smallest())

ff = [(1, "r"), (2, "s"), (4, "v")]

