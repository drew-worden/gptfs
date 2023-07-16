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
        self.operation = operation
        self.label = label

    def __repr__(self):
        return f"Value(data = {self.data}, operation = {self.operation}, label = {self.label})"

    def __add__(self, other):
        return Node(self.data + other.data, (self, other), "+")

    def __mul__(self, other):
        return Node(self.data * other.data, (self, other), "*")


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
            name=uid, label="{%s | data %.4f}" % (node.label, node.data), shape="record"
        )
        if node.operation:
            graph.node(name=uid + node.operation, label=node.operation)
            graph.edge(uid + node.operation, uid)

    for node1, node2 in edges:
        graph.edge(str(id(node1)), str(id(node2)) + node2.operation)

    graph.render(directory="./automatic-gradient-engine")


a = Node(2, label="a")
b = Node(1, label="b")
c = Node(34, label="c")
d = a * b + c
e = a * b
e.label = "e"
d = e + c
d.label = "d"
f = Node(-2, label="f")
L = d * f; L.label = "L"

draw_graph(L)
