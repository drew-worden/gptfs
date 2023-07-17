# IMPORTS
import math
import numpy as np
import matplotlib.pyplot as plt
from graphviz import Digraph


# LOWEST LEVEL DATA STRUCTURE
class Node:
    def __init__(self, data, children=(), operation="", label=""):
        self.data = data
        self.children = set(children)
        self.backward = lambda: None
        self.operation = operation
        self.label = label
        self.gradient = 0

    def __repr__(self):
        return f"Value(data = {self.data}, operation = {self.operation}, label = {self.label})"

    def __add__(self, other):
        output =  Node(self.data + other.data, (self, other), "+")

        def backward():
            self.gradient += 1 * output.gradient
            other.gradient += 1 * output.gradient

        output.backward = backward
        return output

    def __mul__(self, other):
        output = Node(self.data * other.data, (self, other), "*")

        def backward():
            self.gradient += other.data * output.gradient
            other.gradient += self.data * output.gradient

        output.backward = backward
        return output

    def tanh(self):
        x = self.data
        tanh = (math.exp(2*x) - 1)/(math.exp(2*x) + 1)
        output = Node(tanh, (self, ), "tanh")

        def backward():
            self.gradient += (1 - tanh **2) * output.gradient

        output.backward = backward
        return output
    
    def backward_propagation(self):
        topological_list = []
        visited = set()

        def topological_sort(node):
            if node not in visited:
                visited.add(node)
                for child in node.children:
                    topological_sort(child)
                topological_list.append(node)
            
        topological_sort(self)

        self.gradient = 1

        for node in reversed(topological_list):
            node.backward()

# RECURSIVELY TRACE GRAPH OF NODES
def trace_graph(root_node):
    nodes = set()
    edges = set()

    def recursive_build(node):
        if node not in nodes:
            nodes.add(node)
            for child in node.children:
                edges.add((child, node))
                recursive_build(child)

    recursive_build(root_node)

    return nodes, edges


# DRAW GRAPH
def draw_graph(root_node):
    graph = Digraph(format="png", graph_attr={"rankdir": "LR"})

    nodes, edges = trace_graph(root_node)

    for node in nodes:
        uid = str(id(node))
        graph.node(
            name=uid, label="{%s | w = %.4f | g = %.4f}" % (node.label, node.data, node.gradient), shape="record"
        )
        if node.operation:
            graph.node(name=uid + node.operation, label=node.operation)
            graph.edge(uid + node.operation, uid)

    for node1, node2 in edges:
        graph.edge(str(id(node1)), str(id(node2)) + node2.operation)

    graph.render(directory="./automatic-gradient-engine")


