#IMPORTS
from .layer import Layer

class MultiLayerPerceptron:
    def __init__(self, num_inputs, num_outputs):
        size = [num_inputs] + num_outputs
        self.layers = [Layer(size[i], size[i + 1]) for i in range(len(num_outputs))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]