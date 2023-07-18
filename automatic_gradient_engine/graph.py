# IMPORTS
from graphviz import Digraph


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
            name=uid,
            label="{%s | w = %.4f | g = %.4f}" % (node.label, node.data, node.gradient),
            shape="record",
        )
        if node.operation:
            graph.node(name=uid + node.operation, label=node.operation)
            graph.edge(uid + node.operation, uid)

    for node1, node2 in edges:
        graph.edge(str(id(node1)), str(id(node2)) + node2.operation)

    graph.render(directory=".")
