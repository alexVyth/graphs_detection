""" Graph Classed in three different Represantions."""
from collections import defaultdict

import numpy as np
import pandas as pd


class AdjacencyMatrixGraph():
    """Undirected Graph implementation using Adjacency Matrix
    represantation."""
    def __init__(self, datadir):
        data = load_dataset(datadir)
        self.dictionary, self.inv_dictionary = create_dict(data)
        self.adj_matrix = np.zeros([self.num_vertices(), self.num_vertices()], dtype=int)
        for u, v in data:
            self.adj_matrix[self.dictionary[u], self.dictionary[v]] = 1

    def contains_vertex(self, vertex):
        """Check if given vertex belongs to the Graph.
        Return True or false respectively."""
        return vertex in self.dictionary.keys()

    def contains_edge(self, u, v):
        """Check if edge between two given vertices exists.
        Return True or false respectively."""
        return self.adj_matrix[self.dictionary[u], self.dictionary[v]] == 1

    def num_vertices(self):
        """Return the total vertices number."""
        return len(self.dictionary.keys())

    def num_edges(self):
        """Return the total edges number."""
        return int(np.sum(self.adj_matrix) / 2)

    def vertex_set(self):
        """Return set containing Graph vertices."""
        return set(self.dictionary.keys())

    def neighbors(self, vertex):
        """Return set containing all neighbors of the
        given vertex."""
        neighbors = np.where(self.adj_matrix[self.dictionary[vertex]] == 1)[0]
        return set(map(lambda x: self.inv_dictionary[x], list(neighbors)))

    def degree(self, vertex):
        """Return the degree of the given vertex."""
        return np.sum(self.adj_matrix[self.dictionary[vertex]])


class AdjacencyListGraph():
    """Undirected Graph implementation using Adjacency List
    represantation."""
    def __init__(self, datadir):
        data = load_dataset(datadir)
        self.adj_list = defaultdict(set)
        for u, v in data:
            self.adj_list[u].add(v)

    def contains_vertex(self, vertex):
        """Check if given vertex belongs to the Graph.
        Return True or false respectively."""
        return vertex in self.adj_list.keys()

    def contains_edge(self, u, v):
        """Check if edge between two given vertices exists.
        Return True or false respectively."""
        return u in self.adj_list[v]

    def num_vertices(self):
        """Return the total vertices number."""
        return len(self.adj_list.keys())

    def num_edges(self):
        """Return the total edges number."""
        m = 0
        for _, edges in self.adj_list.items():
            m += len(edges)
        return int(m / 2)

    def vertex_set(self):
        """Return set containing Graph vertices."""
        return set(self.adj_list.keys())

    def neighbors(self, vertex):
        """Return set containing all neighbors of the
        given vertex."""
        return set(self.adj_list[vertex])

    def degree(self, vertex):
        """Return the degree of the given vertex."""
        return len(self.neighbors(vertex))


class CompressedSparseRowsGraph():
    """Undirected Graph implementation using Compressed
    Sparse Rows represantation."""
    def __init__(self, datadir):
        data = load_dataset(datadir)
        self.dictionary, self.inv_dictionary = create_dict(data)
        # input data is sorted by rows so columns matrix is ready
        self.columns = list(data[:, 1])
        rows = np.array(data[:, 0], dtype=int)
        # count element on each row
        row_count = np.unique(rows, return_counts=True)[1]
        # add zero in front of the row_count matrix
        row_count = np.insert(row_count, 0, 0)
        # # prefix sum on row_count to obtain row_index matrix
        self.row_index = list(np.cumsum(row_count))

    def contains_vertex(self, vertex):
        """Check if given vertex belongs to the Graph.
        Return True or false respectively."""
        return vertex in self.dictionary.keys()

    def contains_edge(self, u, v):
        """Check if edge between two given vertices exists.
        Return True or false respectively."""
        return u in self.neighbors(v)

    def num_vertices(self):
        """Return the total vertices number."""
        return len(self.dictionary.keys())

    def num_edges(self):
        """Return the total edges number."""
        return int(self.row_index[-1] / 2)

    def vertex_set(self):
        """Return set containing Graph vertices."""
        return self.dictionary.keys()

    def neighbors(self, vertex):
        """Return set containing all neighbors of the
        given vertex."""
        i = self.row_index[self.dictionary[vertex]]
        i_1 = self.row_index[self.dictionary[vertex] + 1]
        return set(self.columns[i: i_1])

    def degree(self, vertex):
        """Return the degree of the given vertex."""
        return len(self.neighbors(vertex))


def load_dataset(directory):
    """Load the dataset given the corresponding directory.
    Dataset should be in text format with 2 columns corresponding
    connected vertices. Output numpy.ndarray with 2 columns."""
    data = pd.read_csv(directory, dtype=int, comment='#', delimiter='\t', header=None)
    data = data.sort_values(by=[0, 1])
    data = data.to_numpy()
    return data


def create_dict(data):
    """Create dictionary to map data vertices to ascending integers
    starting from 0. Also create the inverse dictionary. Return both."""
    vertices = list(np.unique(data))
    dictionary = {vertix: num for num, vertix in enumerate(vertices)}
    inv_dictionary = {value: key for key, value in dictionary.items()}
    return dictionary, inv_dictionary
