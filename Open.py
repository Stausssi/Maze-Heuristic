import heapq


class OpenHeap:
    """
    Represents the heap for the open nodes.
    """

    def __init__(self):
        # list of tuples with (f(x), x)
        self._nodes = []

        heapq.heapify(self._nodes)

    def push(self, node, f):
        """
        Push a graphical node with a given f value on the heap.

        Args:
            node (str): The key of the new board
            f (float): The f value of the new board

        Returns:
            None: Nothing
        """

        heapq.heappush(self._nodes, (f, node))

    def pop(self):
        """
        Removes the smallest element of the heap and returns it.

        Returns:
            tuple[int,str]: Node with smallest f
        """

        return heapq.heappop(self._nodes)

    def replace(self, node, new_f):
        """
        Replace the f for a node if it exists

        Args:
            node (str): The board to replace the f value of
            new_f (float): The new f value

        Returns:
            None: Nothing
        """

        for i, (_, iter_node) in enumerate(self._nodes):
            if iter_node == node:
                self._nodes[i] = new_f, node
                heapq.heapify(self._nodes)
                break

    def isNotEmpty(self):
        """
        Checks whether the heap is empty.

        Returns:
            bool: True, if the heap is not empty
        """

        return self._nodes != []

    def contains(self, contains_node):
        """
        Checks whether a given node is in the heap.

        Args:
            contains_node (str): The key of the node to search for

        Returns:
            bool: True, if the given node is in the heap.
        """

        for _, node in self._nodes:
            if node == contains_node:
                return True
        else:
            return False

    def size(self):
        """
        Gets the size of the heap.

        Returns:
            int: The size of the heap.
        """

        return len(self._nodes)
