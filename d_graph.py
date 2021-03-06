# Course: CS261 - Data Structures
# Author: Jonathan Nichols
# Assignment: 6
# Description: Implementation of a directed graph

from typing import Dict
import heapq


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph
        """
        # add the new column
        self.adj_matrix.append([])
        for i in range(self.v_count):
            self.adj_matrix[i].append(0)
        self.v_count += 1
        # add the new row
        for i in range(self.v_count):
            self.adj_matrix[self.v_count - 1].append(0)
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a new edge to the graph
        """
        # guard clauses
        if (self._is_out_of_bounds(src) or
            self._is_out_of_bounds(dst) or
            src == dst or
                weight < 1):
            return
        # add the edge
        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove the edge from the graph
        """
        if self._is_out_of_bounds(src) or self._is_out_of_bounds(dst):
            return
        self.adj_matrix[src][dst] = 0

    def get_vertices(self):
        """
        Returns a list of vertices from the graph
        """
        return [*range(self.v_count)]

    def get_edges(self):
        """
        Returns a list of the edges in the graph
        """
        edges = []
        # iterate through the matrix
        for i in range(self.v_count):
            for j in range(self.v_count):
                # check for weight and add the edge
                weight = self.adj_matrix[i][j]
                if weight:
                    edges.append((i, j, weight))
        return edges

    def is_valid_path(self, path) -> bool:
        """
        Returns true if the sequence of vertices represents a valid path in the graph
        """
        # check for empty path
        if not path:
            return True
        # check if path vertices are in bounds
        for vertex in path:
            if self._is_out_of_bounds(vertex):
                return False
        # iterate over path and check for missing edges
        for i in range(len(path) - 1):
            x, y = path[i], path[i + 1]
            if not self.adj_matrix[x][y]:
                return False
        return True

    def dfs(self, v_start, v_end=None):
        """
        Performs depth-first search in the graph 
        Returns an ordered list of vertices visited
        """
        # check if v_start exists
        if self._is_out_of_bounds(v_start):
            return []
        # perform the dfs
        visited = []
        v_stack = [v_start]
        while v_stack:
            vertex = v_stack.pop()
            # process the vertex
            if vertex not in visited:
                visited.append(vertex)
            if vertex == v_end:
                break
            # iterate backwards to sort the adjacent nodes in the stack
            for i in range(self.v_count - 1, -1, -1):
                # check for edge
                if self.adj_matrix[vertex][i]:
                    # add adjacent nodes to the stack
                    if i not in visited:
                        v_stack.append(i)
        return visited

    def bfs(self, v_start, v_end=None):
        """
        Performs a breadth-first search in the graph
        Returns an ordered list of vertices visited
        """
        # check if v_start exists
        if self._is_out_of_bounds(v_start):
            return []
        # perform the dfs
        visited = []
        v_queue = [v_start]
        while v_queue:
            vertex = v_queue.pop()
            # process the vertex
            if vertex not in visited:
                visited.append(vertex)
            if vertex == v_end:
                break
            for i in range(self.v_count):
                # check for edge
                if self.adj_matrix[vertex][i]:
                    # add adjacent nodes to the queue
                    if i not in visited:
                        v_queue.insert(0, i)
        return visited

    def has_cycle(self):
        """
        Returns true if there is at least one cycle in the graph
        """
        for v_start in range(self.v_count):
            # perform dfs
            visited = []
            v_stack = [v_start]
            while v_stack:
                vertex = v_stack.pop()
                # process the vertex
                if vertex not in visited:
                    visited.append(vertex)
                # find the child nodes
                for i in range(self.v_count):
                    # check for edge
                    if self.adj_matrix[vertex][i]:
                        # current vertex points back to start
                        if v_start == i:
                            return True
                        # add adjacent nodes to the queue
                        if i not in visited:
                            v_stack.append(i)
        return False

    def dijkstra(self, src: int):
        """
        Implements the Dijkstra algorithm to compute length of the 
        shortest path from a given vertex to all other vertices in the graph
        """
        distances = dict()
        queue = [(0, src)]
        # perform djikstra algorithm using heapq
        while queue:
            distance, vertex = heapq.heappop(queue)
            if vertex not in distances:
                distances[vertex] = distance
                for i in range(self.v_count):
                    weight = self.adj_matrix[vertex][i]
                    if weight:
                        heapq.heappush(queue, (distance + weight, i))
        # fill in missing data
        for v in range(self.v_count):
            if v not in distances:
                distances[v] = float('inf')
        # convert and return as list
        return [val for key, val in sorted(distances.items())]

    def _is_out_of_bounds(self, index: int) -> bool:
        """Helper function to check if given vertex exists"""
        return index < 0 or index > self.v_count - 1


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
