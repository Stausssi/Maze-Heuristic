import heapq


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

    def pop(self):
        """

        Returns:
            tuple[int,str]: Node with smallest f

        """

        return heapq.heappop(self._nodes)

    def replace(self, node, new_f):
        """

        Replace the f for a node if it exists

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

    def isNotEmpty(self):
        """

        Returns:

        """

        return self._nodes != []

    def contains(self, contains_node):
        """

        Args:
            contains_node(str) :

        Returns:

        """

        for _, node in self._nodes:
            if node == contains_node:
                return True
        else:
            return False

    def size(self):
        """

        Returns:

        """

        return len(self._nodes)
