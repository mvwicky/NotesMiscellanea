class AdjacencyList(object):
    def __init__(self, nodes):
        self.adj = [[] for _ in nodes]
        self.nodes = nodes
        self.visited_nodes = []

    def add_edge(self, i, j):
        self.adj[i].append(j)

    def remove_edge(self, i, j):
        del self.adj[i][self.adj[i].index(j)]

    def has_edge(self, i, j):
        return j in self.adj[i]

    def out_edges(self, i):
        return self.adj[i]

    def in_edges(self, i):
        return [ind for ind, j in enumerate(self.adj) if i in j]

    def num_verts(self):
        return len(self.adj)


def main():
    pass

if __name__ == '__main__':
    main()
