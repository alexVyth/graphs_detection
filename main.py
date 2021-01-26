#!/usr/bin/env python3
"""Graph top-k link prediction"""
import argparse
import sys
import time

from graph_representations import (AdjacencyListGraph, AdjacencyMatrixGraph,
                                   CompressedSparseRowsGraph)
from metrics import adamic_adar, common_neighbors, jaccard, top_k_similar_nodes

start = time.time()

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dir', help='path of data text file')
parser.add_argument('-r', '--represantation',
                    help='type of graph representation. '
                         'Options: "AM" for Adjacency Matrix,'
                         '"AL" for Adjacency List and'
                         '"CSR" for Compressed Sparse Matrix')
parser.add_argument('-m', '--metric',
                    help='type of performance metric. '
                    'Options: "neighbors", "jaccard", "adamic/adar"')
parser.add_argument('-k', '--kedges', help='k number of k-top edges')
args = parser.parse_args()
data_dir = args.dir
represantation_type = args.represantation
metric_type = args.metric
k = int(args.kedges)

# Choose graph represantation
if represantation_type == 'AL':
    Graph = AdjacencyListGraph
elif represantation_type == 'AM':
    Graph = AdjacencyMatrixGraph
elif represantation_type == 'CSR':
    Graph = CompressedSparseRowsGraph
else:
    sys.exit('Wrong graph represantation type')

# Choose metric
if metric_type == 'neighbors':
    metric = common_neighbors
elif metric_type == 'jaccard':
    metric = jaccard
elif metric_type == 'adamic-adar':
    metric = adamic_adar
else:
    sys.exit('Wrong metric type')

# Main Process
graph = Graph(data_dir)
results = top_k_similar_nodes(graph, metric, k)

print(f'Reprasantation={represantation_type}, Metric={metric_type}, k={k}\n')
print('Top-k Results:')
print('#\tScore\tEdge')
for i in range(k):
    print(f'{i+1}\t{results[i][0]}\t{results[i][1]}')
print(f'\nFinished in {time.time() - start} seconds.')
