# src/graph/graph_utils.py

from typing import Dict, Any, List, Tuple

class GraphUtils:
    @staticmethod
    def find_paths(graph: Dict[str, Dict[str, Any]], start: str, end: str, relation: str) -> List[List[str]]:
        """
        Finds all paths between two nodes following a specific relation.

        Args:
        graph (Dict[str, Dict[str, Any]]): The graph structure.
        start (str): The starting node.
        end (str): The ending node.
        relation (str): The relation to follow.

        Returns:
        List[List[str]]: A list of paths, where each path is a list of node names.
        """
        def dfs(current: str, path: List[str]):
            if current == end:
                paths.append(path)
                return
            
            if current in graph and relation in graph[current]:
                next_node = graph[current][relation]
                if next_node not in path:  # Avoid cycles
                    dfs(next_node, path + [next_node])

        paths: List[List[str]] = []
        dfs(start, [start])
        return paths

    @staticmethod
    def find_nodes_with_relation(graph: Dict[str, Dict[str, Any]], relation: str) -> List[Tuple[str, str]]:
        """
        Finds all pairs of nodes connected by a specific relation.

        Args:
        graph (Dict[str, Dict[str, Any]]): The graph structure.
        relation (str): The relation to search for.

        Returns:
        List[Tuple[str, str]]: A list of (source, target) pairs connected by the relation.
        """
        pairs = []
        for source, relations in graph.items():
            if relation in relations:
                pairs.append((source, relations[relation]))
        return pairs

    @staticmethod
    def get_subgraph(graph: Dict[str, Dict[str, Any]], nodes: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Extracts a subgraph containing only the specified nodes and their relations.

        Args:
        graph (Dict[str, Dict[str, Any]]): The original graph structure.
        nodes (List[str]): The list of nodes to include in the subgraph.

        Returns:
        Dict[str, Dict[str, Any]]: The subgraph.
        """
        subgraph = {}
        for node in nodes:
            if node in graph:
                subgraph[node] = {
                    rel: target for rel, target in graph[node].items()
                    if target in nodes
                }
        return subgraph

    @staticmethod
    def merge_graphs(graph1: Dict[str, Dict[str, Any]], graph2: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Merges two graphs into a single graph.

        Args:
        graph1 (Dict[str, Dict[str, Any]]): The first graph.
        graph2 (Dict[str, Dict[str, Any]]): The second graph.

        Returns:
        Dict[str, Dict[str, Any]]: The merged graph.
        """
        merged = graph1.copy()
        for node, relations in graph2.items():
            if node in merged:
                merged[node].update(relations)
            else:
                merged[node] = relations.copy()
        return merged

    @staticmethod
    def get_node_degree(graph: Dict[str, Dict[str, Any]], node: str) -> Tuple[int, int]:
        """
        Calculates the in-degree and out-degree of a node.

        Args:
        graph (Dict[str, Dict[str, Any]]): The graph structure.
        node (str): The node to calculate degrees for.

        Returns:
        Tuple[int, int]: A tuple of (in_degree, out_degree).
        """
        if node not in graph:
            return (0, 0)

        out_degree = len(graph[node])
        in_degree = sum(1 for relations in graph.values() if node in relations.values())
        return (in_degree, out_degree)