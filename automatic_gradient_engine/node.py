# IMPORTS
import math

#NODE DATA STRUCTURE
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
        other = other if isinstance(other, Node) else Node(other)
        output = Node(self.data + other.data, (self, other), "+")

        def backward():
            self.gradient += 1 * output.gradient
            other.gradient += 1 * output.gradient

        output.backward = backward
        return output
    
    def __radd__(self, other):
        return self * other
    
    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        other = other if isinstance(other, Node) else Node(other)
        output = Node(self.data * other.data, (self, other), "*")

        def backward():
            self.gradient += other.data * output.gradient
            other.gradient += self.data * output.gradient

        output.backward = backward
        return output
    
    def __rmul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        return self * other ** -1
    
    def __pow__(self, other):
        assert isinstance(other, (int, float))
        output = Node(self.data ** other, (self, ), f"^{other}")

        def backward():
            self.gradient += other * (self.data ** (other - 1)) * output.gradient

        output.backward = backward
        return output
    
    def __neg__(self):
        return self * -1

    def exp(self):
        x = self.data
        output = Node(math.exp(x), (self, ), "exp")

        def backward():
            self.gradient = output.data * output.gradient

        output.backward = backward
        return output

    def tanh(self):
        x = self.data
        tanh = (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)
        output = Node(tanh, (self,), "tanh")

        def backward():
            self.gradient += (1 - tanh**2) * output.gradient

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
