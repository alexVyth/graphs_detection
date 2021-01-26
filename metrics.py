"""Perfomance metrics for set similarity."""
from math import log
from itertools import combinations
import heapq


def common_neighbors(set_1, set_2):
    """Calculate the number of common elements (intersection) in two sets."""
    return len(set_1.intersection(set_2))


def jaccard(set_1, set_2):
    """Calculate Jaccard Similarity of two sets S1, S1.
    Jaccard(S1, S2) = |Intersection(S1, S2)| / |Union(S1, S2)|"""
    intersection = len(set_1.intersection(set_2))
    union = len(set_1.union(set_2))
    return intersection / union


def adamic_adar(graph, set_1, set_2):
    """Calculate Adamic/Adar of two sets S1, S1 as the sum of 1 / log(N(u))
    for every 'u' common element of the two sets."""
    intersection = set_1.intersection(set_2)
    sums = [1 / log(len(graph.neighbors(element))) for element in intersection]
    return sum(sums)


def top_k_similar_nodes(graph, metric, k):
    """Return top k edges of most similar vertices and
    the corresponding scores of given metric."""
    # Initialize best scores
    scores = [(-1, None)] * k
    # Iterate over all posible vertix pairs
    for pair in combinations(graph.vertex_set(), 2):
        # Skip connected vertices
        if not graph.contains_edge(*pair):
            # Calculate metric score for pair neighbors
            if metric is adamic_adar:
                score = metric(graph, graph.neighbors(pair[0]), graph.neighbors(pair[1]))
            else:
                score = metric(graph.neighbors(pair[0]), graph.neighbors(pair[1]))
            # Keep top-k scores with heap
            if score > scores[0][0]:
                heapq.heappop(scores)
                heapq.heappush(scores, (score, pair))
    return sorted(scores, reverse=True)
