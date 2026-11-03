"""Constrained causal graph estimation and stabilized IPTW utilities.

Graph discovery is delegated to a declared conditional-independence backend.
The resulting graph is an observational structure estimate, not proof of causality.
"""
import numpy as np
import networkx as nx

class StructuralCausalInterventionGraph:
    def __init__(self, allowed_edges=None, forbidden_edges=None):
        self.allowed_edges = set(map(tuple, allowed_edges or []))
        self.forbidden_edges = set(map(tuple, forbidden_edges or []))
        self.graph = nx.DiGraph()

    def set_graph(self, nodes, directed_edges):
        graph = nx.DiGraph()
        graph.add_nodes_from(nodes)
        for source, target in directed_edges:
            if (source, target) in self.forbidden_edges:
                continue
            if self.allowed_edges and (source, target) not in self.allowed_edges:
                continue
            graph.add_edge(source, target)
        if not nx.is_directed_acyclic_graph(graph):
            raise ValueError("Constrained graph contains a directed cycle.")
        self.graph = graph
        return graph

    def export_edges(self):
        return list(self.graph.edges())

def stabilized_iptw(treatment, propensity, marginal_probability, lower, upper, epsilon):
    """Compute stabilized weights and clip using training-derived bounds."""
    propensity = np.clip(propensity, epsilon, 1.0)
    marginal_probability = np.clip(marginal_probability, epsilon, 1.0)
    weights = marginal_probability / propensity
    return np.clip(weights, lower, upper)
