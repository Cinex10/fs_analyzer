# tests/test_graph.py

import unittest
from src.graph.graph_builder import GraphBuilder
from src.graph.graph_utils import GraphUtils

class TestGraphBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = GraphBuilder()

    def test_build_initial_graph(self):
        tokens = ["le", "chat", "mange"]
        graph = self.builder.build_initial_graph(tokens)
        
        self.assertIn("_START", graph)
        self.assertIn("_END", graph)
        self.assertEqual(graph["_START"]["r_succ"], "le")
        self.assertEqual(graph["le"]["r_succ"], "chat")
        self.assertEqual(graph["chat"]["r_succ"], "mange")
        self.assertEqual(graph["mange"]["r_succ"], "_END")

    def test_add_node(self):
        self.builder.add_node("test", {"attr": "value"})
        self.assertIn("test", self.builder.graph)
        self.assertEqual(self.builder.graph["test"]["attr"], "value")

    def test_add_relation(self):
        self.builder.add_node("A")
        self.builder.add_node("B")
        self.builder.add_relation("A", "r_test", "B")
        self.assertEqual(self.builder.graph["A"]["r_test"], "B")

    def test_remove_node(self):
        self.builder.add_node("A")
        self.builder.add_node("B")
        self.builder.add_relation("A", "r_test", "B")
        self.builder.remove_node("B")
        self.assertNotIn("B", self.builder.graph)
        self.assertNotIn("r_test", self.builder.graph["A"])

    def test_remove_relation(self):
        self.builder.add_node("A")
        self.builder.add_node("B")
        self.builder.add_relation("A", "r_test", "B")
        self.builder.remove_relation("A", "r_test")
        self.assertNotIn("r_test", self.builder.graph["A"])

class TestGraphUtils(unittest.TestCase):
    def setUp(self):
        self.builder = GraphBuilder()
        self.utils = GraphUtils()

    def test_find_paths(self):
        graph = {
            "A": {"r": "B"},
            "B": {"r": "C"},
            "C": {"r": "D"},
            "D": {}
        }
        paths = self.utils.find_paths(graph, "A", "D", "r")
        self.assertEqual(paths, [["A", "B", "C", "D"]])

    def test_find_nodes_with_relation(self):
        graph = {
            "A": {"r": "B"},
            "B": {"r": "C"},
            "C": {"r": "D"},
            "D": {}
        }
        pairs = self.utils.find_nodes_with_relation(graph, "r")
        self.assertEqual(set(pairs), {("A", "B"), ("B", "C"), ("C", "D")})

    def test_get_subgraph(self):
        graph = {
            "A": {"r": "B"},
            "B": {"r": "C"},
            "C": {"r": "D"},
            "D": {}
        }
        subgraph = self.utils.get_subgraph(graph, ["A", "B", "C"])
        self.assertEqual(subgraph, {
            "A": {"r": "B"},
            "B": {"r": "C"},
            "C": {}
        })

    def test_merge_graphs(self):
        graph1 = {"A": {"r1": "B"}}
        graph2 = {"B": {"r2": "C"}}
        merged = self.utils.merge_graphs(graph1, graph2)
        self.assertEqual(merged, {
            "A": {"r1": "B"},
            "B": {"r2": "C"}
        })

    def test_get_node_degree(self):
        graph = {
            "A": {"r1": "B", "r2": "C"},
            "B": {"r3": "C"},
            "C": {}
        }
        in_degree, out_degree = self.utils.get_node_degree(graph, "C")
        self.assertEqual(in_degree, 2)
        self.assertEqual(out_degree, 0)

if __name__ == '__main__':
    unittest.main()