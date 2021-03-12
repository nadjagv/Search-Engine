class Vertex:
    """Lightweight vertex structure for a graph."""
    __slots__ = '_element'
    def __init__(self, x):
        """Do not call constructor directly.
        Use Graph's insert_vertex(x).
        """
        self._element = x
    def element(self):
        """Return element associated with this vertex."""
        return self._element
    def __hash__(self): # will allow vertex to be a map/set key
        return hash(id(self))
    def __str__(self):
        return str(self._element)


class Edge:
    __slots__ = '_origin', '_destination', '_element'
    def __init__(self, u, v, x):
        self._origin = u
        self._destination = v
        self._element = x

    def endpoints(self):
        return (self._origin, self._destination)

    def opposite(self, v):
        if not isinstance(v, Graph.Vertex):
            raise TypeError('v must be a Vertex')
        return self._destination if v is self._origin else self._origin

    def element(self):
        return self._element

    def __hash__(self): # will allow edge to be a map/set key
        return hash((self._origin, self._destination))

    def __str__(self):
        return '({0},{1},{2})'.format(self._origin,self._destination,self._element)


class Graph():
    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    # def _validate_vertex(self, v):
    #     if not isinstance(v, self.vertex):
    #         raise TypeError('Vertex expected')
    #     if v not in self._outgoing:
    #         raise ValueError('Vertex does not belong to this graph.')
    #
    def is_directed(self):
        return self._incoming is not self._outgoing
    #
    # def vertex_count(self):
    #     return len(self._outgoing)
    #
    # def vertices(self):
    #     return self._outgoing.keys()
    #
    # def edge_count(self):
    #     total = sum(len(self._outgoing[v]) for v in self._outgoing)
    #     return total if self.is_directed() else total // 2

    def edges(self):
        result = set() # avoid double-reporting edges of undirected graph
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values()) # add edges to resulting set
        return result

    def get_edge(self, u, v):
        # self._validate_vertex(u)
        # self._validate_vertex(v)
        return self._outgoing[u].get(v) # returns None if v not adjacent
    #
    # def degree(self, v, outgoing=True):
    #     self._validate_vertex(v)
    #     adj = self._outgoing if outgoing else self._incoming
    #     return len(adj[v])
    #
    # def incident_edges(self, v, outgoing=True):
    #     self._validate_vertex(v)
    #     adj = self._outgoing if outgoing else self._incoming
    #     for edge in adj[v].values():
    #         yield edge

    def insert_vertex(self, x=None):
        self.vertex = Vertex(x)
        v = self.vertex
        self._outgoing[x] = {}
        if self.is_directed():
            self._incoming[x] = {} # need distinct map for incoming edges
        return x

    def insert_edge(self, u, v, x=None):
        # if self.get_edge(u, v) is not None: # includes error checking
        #     raise ValueError('u and v are already adjacent')
        self.edge = Edge(u, v, x)
        e = self.edge
        # print("u" + str(u) + "   vvvv" + str(v))
        self._outgoing[u][v] = u
        self._incoming[v][u] = v
