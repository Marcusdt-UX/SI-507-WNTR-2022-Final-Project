import json
from models.queue_graph import *


class BaseGraph:
    """A class representing a graph"""

    def __init__(self):
        """Create an empty graph"""
        self.adjList = {}

    def add_vertex(self, vertex):
        """Add a vertex to the graph, associated with the given key (vertex)"""
        if vertex not in self.adjList:
            self.adjList[vertex] = []

    def add_edge(self, vertex1, vertex2):
        """Add an edge from vertex1 to vertex2. If vertex1 or vertex2 is not in the graph, adds it."""
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)

        if vertex2 not in self.adjList[vertex1]:
            self.adjList[vertex1].append(vertex2)

    def is_adjacent(self, vertex1, vertex2):
        """Returns True if there is an edge leading from vertex1 to vertex2"""
        return vertex2 in self.adjList[vertex1]

    def get_adjacent_vertices(self, vertex):
        """Returns a list of vertices adjacent to the given vertex"""
        return self.adjList[vertex]

    def get_vertices(self):
        """Returns a list of the vertices in the graph"""
        return list(self.adjList.keys())

    def get_edges(self):
        """Returns a list of tuples representing edges in the graph. In each tuple the first element is the "from" vertex, the second is the "to" vertex"""
        edgeList = []
        for v in self.adjList:
            for i in range(len(self.adjList[v])):
                edgeList.append((v, self.adjList[v][i]))
        return edgeList


class Graph(BaseGraph):
    """Subclass of Graph that associates data with edges."""

    def __init__(self):
        """Adds new instance variable edgeList, which has tuples as keys and data as values."""
        super().__init__()
        self.edgeList = {}

    def get_edge_data(self, vertex1, vertex2):
        """Returns the data associated with the given vertices, or None if the edge does not exist."""
        if (vertex1, vertex2) in self.edgeList:
            return self.edgeList[(vertex1, vertex2)]
        return None

    def add_edge(self, vertex1, vertex2, data):
        """Adds an edge to graph associated with the given data."""
        super().add_edge(vertex1, vertex2)
        self.edgeList[(vertex1, vertex2)] = data

    def to_json(self):
        print('Converting graph to JSON')
        output = {}

        for k,v in self.adjList.items():

            if k.name not in output:
                neighbors = []
                key = k.name

                for node in self.get_adjacent_vertices(k):
                    neighbors.append(node.__dict__)

                output[key] = neighbors



        with open('output_events.json','w') as f:
            json.dump(output,f)


def find_shortest_path(graph, from_event, to_event):
    q = Queue_()
    added = {} 
    path = {}  
    events = graph.get_vertices()
    for a in events:
        added[a] = False 
    q.enqueue(from_event)
    added[to_event] = True

    while not q.isEmpty():
        evt = q.dequeue()
        if evt == to_event: 
            pathList = []
            pathList.append(to_event)
            vertex = path.get(evt, None)
            while vertex != None:  
                pathList.append(vertex)
                vertex = path.get(vertex, None)
            return pathList[::-1]  # List must be reversed before returning

        for neighbor in graph.get_adjacent_vertices(evt):
            if added[neighbor] == False:
                q.enqueue(neighbor)
                added[neighbor] = True
                path[neighbor] = evt

    return None  

