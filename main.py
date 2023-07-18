#IMPORTS
from neural_network_library.mulit_layer_perceptron import MultiLayerPerceptron
from automatic_gradient_engine.graph import draw_graph

#EXAMPLE NN WITH 4 LAYERS
# INPUT LAYER: 3 NODES
# HIDDEN LAYER 1: 4 NODES
# HIDDEN LAYER 2: 4 NODES
# OUTPUT LAYER: 1 NODE


#INITIALIZE NETWORK
inputs = [2, 3, -1]

mlp = MultiLayerPerceptron(len(inputs), [4, 4, 1])

xs = [
    [2, 3, -1],
    [3, -1, 0.5],
    [0.5, 1, 1],
    [1, 1, -1]
]

ys = [1, -1, -1, 1]

#TRAINING LOOP
for k in range(10000):
    #FORWARD PASS
	ypred = [mlp(x) for x in xs]
	loss = sum((yout - ygt) ** 2 for ygt, yout in zip(ys, ypred))

	#BACKWARD PASS
	for p in mlp.parameters():
		p.gradient = 0
	loss.backward_propagation()

	#UPDATE (GRADIENT DESCENT)
	for p in mlp.parameters():
		p.data += -0.05 * p.gradient

	print(k, loss.data)

#RESULTS
print(ypred)
loss.backward_propagation()
draw_graph(loss)


