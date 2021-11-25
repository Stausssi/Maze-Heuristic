import heapq
from Node import Node


class OpenHeap:
    def __init__(self):
        # list of tuples with (f(x), x)
        self._nodes = []

        heapq.heapify(self._nodes)

    def push(self, node, f):
        """

        Args:
            node:
            f:

        Returns:

        """

        heapq.heappush(self._nodes, (f, node))

    def pop_smallest(self) -> Node:
        """

        Returns:

        """

        return heapq.heappop(self._nodes)

    def replace_or_push(self, node, new_f):
        """

        Replace the f for a node if it exists or else insert the node

        Args:
            node:
            new_f:

        Returns:

        """

        for i, (_, iter_node) in enumerate(self._nodes):
            if iter_node == node:
                self._nodes[i] = new_f, node
                heapq.heapify(self._nodes)
                break
        else:
            self.push(node, new_f)

    def isNotEmpty(self):
        """

        Returns:

        """

        return self._nodes != []

    def contains(self, contains_node):
        """

        Args:
            contains_node:

        Returns:

        """

        for _, node in self._nodes:
            if node == contains_node:
                return True
        else:
            return False
