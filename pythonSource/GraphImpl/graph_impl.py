import os
import sys
import random
import argparse

from node import Node
from adjacency_matrix import AdjacencyMatrix
from adjacency_list import AdjacencyList


def main():
    random.seed()
    num_nodes = 10
    x = [random.randint(-10000, 10000) for _ in range(num_nodes)]
    y = [random.randint(-10000, 10000) for _ in range(num_nodes)]
    nodes = [Node(i, j) for i, j in zip(x, y)]

    graph = AdjacencyMatrix(nodes)
    for elem in graph.mat:
        while True:
            i = random.randrange(0, len(graph.mat))
            j = random.randrange(0, len(graph.mat))
            if i != j and not graph.has_edge(i, j):
                break
        graph.add_edge(i, j)
        graph.add_edge(j, i)
    graph.depth_first_search(random.randrange(0, len(graph.mat)))
    graph.show_graph(draw_edges=False)

if __name__ == '__main__':
    main()
