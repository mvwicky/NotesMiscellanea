import numpy as np
import matplotlib.pyplot as plt


class AdjacencyMatrix(object):
    def __init__(self, nodes):
        self.mat = []
        self.nodes = nodes
        self.visited_nodes = []
        for i in nodes:
            self.mat.append([False for _ in nodes])

    def print_mat(self):
        for elem in self.mat:
            print(list(map(int, elem)))

    def add_edge(self, i, j):
        self.mat[i][j] = True

    def remove_edge(self, i, j):
        self.mat[i][j] = False

    def has_edge(self, i, j):
        return self.mat[i][j]

    def out_edges(self, i):
        return [ind for ind, j in enumerate(self.mat[i]) if j]

    def in_edges(self, i):
        ret = []
        for ind, j in enumerate(self.mat):
            if ind == i:
                continue
            for ind2, j2 in enumerate(j):
                if j2:
                    ret.append(ind)
        return ret

    def breadth_first_search(self, start):
        print('Starting at: {}'.format(self.nodes[start]))
        visited_nodes = [start]
        self.nodes[start].visited = True
        while visited_nodes:
            c_node = visited_nodes.pop(0)
            print('Visiting: {}'.format(self.nodes[c_node]))
            edges = self.out_edges(c_node)
            for n in edges:
                print('Adjacent Nodes: {}'.format(self.nodes[n]))
                if not self.nodes[n].visited:
                    visited_nodes.append(n)
                    self.nodes[n].visited = True

    def depth_first_search(self, start):
        pass

    def num_verts(self):
        return len(self.mat)

    def show_graph(self, draw_edges=False):
        visited_x = [n.x for n in self.nodes if n.visited]
        visited_y = [n.y for n in self.nodes if n.visited]
        uvisit_x = [n.x for n in self.nodes if not n.visited]
        uvisit_y = [n.y for n in self.nodes if not n.visited]

        edges = []
        for i, sub in enumerate(self.mat):
            for j, elem in enumerate(sub):
                if elem and i != j:
                    edges.append((i, j))

        range_tup = [abs(min([n.x for n in self.nodes])),
                     abs(max([n.x for n in self.nodes])),
                     abs(min([n.y for n in self.nodes])),
                     abs(max([n.y for n in self.nodes]))]

        r = max(range_tup) + (0.1 * max(range_tup))
        plt.plot(visited_x, visited_y, 'ro')
        plt.plot(uvisit_x, uvisit_y, 'go')
        if draw_edges:
            for edge in edges:
                x0 = self.nodes[edge[0]].x
                y0 = self.nodes[edge[0]].y
                x1 = self.nodes[edge[1]].x
                y1 = self.nodes[edge[1]].y
                plt.annotate('', xy=(x1, y1), xytext=(x0, y0),
                             arrowprops=dict(facecolor='black',
                                             shrink=0.01,
                                             width=0.2,
                                             headwidth=3))
        plt.axis([-r, r, -r, r])
        plt.grid()
        plt.show()


def main():
    pass

if __name__ == '__main__':
    main()
