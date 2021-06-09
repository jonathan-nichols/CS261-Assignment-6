# Course: CS261 Data Structures
# Author: Jonathan Nichols
# Assignment: 6
# Description: Implementation of undirected


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        # add to the dict if the key does not exist
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        # same vertex
        if u == v:
            return
        # edge already exists
        if u in self.adj_list and v in self.adj_list:
            if u in self.adj_list[v] and v in self.adj_list[u]:
                return
        # make the vertices exist in the graph
        self.add_vertex(u)
        self.add_vertex(v)
        # add the edge
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # same vertex
        if u == v:
            return
        # at least one vertex does not exist
        if u not in self.adj_list or v not in self.adj_list:
            return
        # edge does not exist
        if u not in self.adj_list[v] or v not in self.adj_list[u]:
            return
        # remove the edge
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # vertex does not exist
        if v not in self.adj_list:
            return
        # remove edges from connected vertices
        for vertex in self.adj_list[v]:
            self.adj_list[vertex].remove(v)
        # remove the vertex
        self.adj_list.pop(v)

    def get_vertices(self):
        """
        Return list of vertices in the graph (any order)
        """
        return [*self.adj_list]

    def get_edges(self):
        """
        Return list of edges in the graph (any order)
        """
        edges = []
        # iterate through all edges
        for vertex_a in self.adj_list:
            for vertex_b in self.adj_list[vertex_a]:
                # require alphabetical order to avoid duplicates
                if vertex_b > vertex_a:
                    edges.append((vertex_a, vertex_b))
        return edges

    def is_valid_path(self, path) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        # check for empty path
        if not path:
            return True
        # check if first vertex exists
        current_vertex, *path = path
        if current_vertex not in self.adj_list:
            return False
        # iterate through remaining path
        for vertex in path:
            if vertex not in self.adj_list[current_vertex]:
                return False
            current_vertex = vertex
        return True

    def dfs(self, v_start, v_end=None):
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        # check if start vertex exists
        if v_start not in self.adj_list:
            return []
        # initialize data containers
        # simulating a stack by only using append and pop list methods
        visited = []
        v_stack = []
        v_stack.append(v_start)
        # process the vertices
        while v_stack:
            vertex = v_stack.pop()
            # store the visited vertex
            if vertex not in visited:
                visited.append(vertex)
            # check for end vertex
            if vertex == v_end:
                break
            # store the successor vertices
            direct_successors = sorted(self.adj_list[vertex], reverse=True)
            for v in direct_successors:
                if v not in visited:
                    v_stack.append(v)
        return visited

    def bfs(self, v_start, v_end=None):
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        # check if start vertex exists
        if v_start not in self.adj_list:
            return []
        # initialize data containers
        # simulating a queue with a list
        visited = []
        v_queue = []
        v_queue.append(v_start)
        # process the vertices
        while v_queue:
            vertex = v_queue.pop()
            # store the visited vertex
            if vertex not in visited:
                visited.append(vertex)
            # check for end vertex
            if vertex == v_end:
                break
            # store the successor vertices
            direct_successors = sorted(self.adj_list[vertex])
            for v in direct_successors:
                if v not in visited:
                    v_queue[:0] = v
        return visited

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()

    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #     'add FG', 'remove GE')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print('{:<10}'.format(case), g.has_cycle())
