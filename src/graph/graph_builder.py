from typing import List, Dict, Any

class GraphBuilder:
    def __init__(self):
        self.graph: Dict[str, Dict[str, Any]] = {}

    def build_initial_graph(self, tokens: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Builds the initial graph structure from a list of tokens.

        Args:
        tokens (List[str]): A list of tokenized words from the input text.

        Returns:
        Dict[str, Dict[str, Any]]: The constructed graph.
        """
        self.graph = {"_START": {"r_succ": tokens[0]}}

        for i in range(len(tokens)):
            current_token = tokens[i]
            
            if current_token not in self.graph:
                self.graph[current_token] = {}
            
            if i < len(tokens) - 1:
                next_token = tokens[i + 1]
                self.graph[current_token]["r_succ"] = next_token
            else:
                self.graph[current_token]["r_succ"] = "_END"

        self.graph["_END"] = {}

        self._add_predecessor_relations()

        return self.graph

    def _add_predecessor_relations(self):
        """
        Adds reverse 'r_pred' (predecessor) relations to the graph.
        """
        for token, relations in self.graph.items():
            if "r_succ" in relations:
                successor = relations["r_succ"]
                if successor not in self.graph:
                    self.graph[successor] = {}
                self.graph[successor]["r_pred"] = token

    def add_node(self, node: str, attributes: Dict[str, Any] = None):
        """
        Adds a new node to the graph.

        Args:
        node (str): The node to add.
        attributes (Dict[str, Any], optional): Attributes of the node.
        """
        if node not in self.graph:
            self.graph[node] = attributes if attributes else {}

    def add_relation(self, source: str, relation: str, target: str):
        """
        Adds a new relation between two nodes in the graph.

        Args:
        source (str): The source node.
        relation (str): The type of relation.
        target (str): The target node.
        """
        if source not in self.graph:
            self.graph[source] = {}
        self.graph[source][relation] = target

    def get_node(self, node: str) -> Dict[str, Any]:
        """
        Retrieves a node and its relations from the graph.

        Args:
        node (str): The node to retrieve.

        Returns:
        Dict[str, Any]: The node's relations and attributes.
        """
        return self.graph.get(node, {})

    def get_relation(self, source: str, relation: str) -> str:
        """
        Retrieves the target of a specific relation from a source node.

        Args:
        source (str): The source node.
        relation (str): The type of relation.

        Returns:
        str: The target node of the relation.
        """
        return self.graph.get(source, {}).get(relation)

    def remove_node(self, node: str):
        """
        Removes a node and all its relations from the graph.

        Args:
        node (str): The node to remove.
        """
        if node in self.graph:
            del self.graph[node]
        
        # Remove any relations pointing to this node
        for source, relations in self.graph.items():
            self.graph[source] = {rel: target for rel, target in relations.items() if target != node}

    def remove_relation(self, source: str, relation: str):
        """
        Removes a specific relation from a source node.

        Args:
        source (str): The source node.
        relation (str): The type of relation to remove.
        """
        if source in self.graph and relation in self.graph[source]:
            del self.graph[source][relation]

    def get_all_nodes(self) -> List[str]:
        """
        Retrieves all nodes in the graph.

        Returns:
        List[str]: A list of all nodes in the graph.
        """
        return list(self.graph.keys())

    def get_all_relations(self) -> List[tuple]:
        """
        Retrieves all relations in the graph.

        Returns:
        List[tuple]: A list of tuples (source, relation, target) for all relations in the graph.
        """
        relations = []
        for source, attrs in self.graph.items():
            for relation, target in attrs.items():
                relations.append((source, relation, target))
        return relations

    def print_graph(self):
        """
        Prints the graph structure for visualization and debugging purposes.
        """
        for node, relations in self.graph.items():
            print(f"Node: {node}")
            for relation, target in relations.items():
                print(f"  -{relation}-> {target}")
            print()

# Example usage
if __name__ == "__main__":
    builder = GraphBuilder()
    sample_text = "Le petit chat boit du lait"
    tokens = sample_text.lower().split()  # Simple tokenization for this example
    graph = builder.build_initial_graph(tokens)
    builder.print_graph()

    # Add a new relation
    builder.add_relation("chat", "r_agent", "boit")
    
    print("\nAfter adding new relation:")
    builder.print_graph()