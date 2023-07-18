#IMPORTS
from automatic_gradient_engine.node import Node
import random

# NEURON DATA STRUCTURE
class Neuron:
    def __init__(self, num_inputs):
        self.weights = [Node(random.uniform(-1, 1)) for _ in range(num_inputs)]
        self.bias = Node(random.uniform(-1, 1))

    def __call__(self, x):
        activation = sum((wi * xi for wi, xi in zip(self.weights, x)), self.bias)
        output = activation.tanh()
        return output
    
    def parameters(self):
        return self.weights + [self.bias]
    

