import Neural_Networks as nn
from Neural_Networks.layers import InputLayer, Layer
from Neural_Networks.ActivationFunctions import sigmoid
from Data import Data


l1 = InputLayer(360, nn.predprocess, "L1")
l2 = Layer(360, 120, sigmoid, "L2")
l3 = Layer(120, 12, sigmoid, "L3")

net = nn.FeedForwardNeuralNetwork([l1, l2, l3])

data = Data("Data/Datasets/gestures_train.csv", 360)

net.train(data, epochs=120, learning_rate=0.1)
net.plotCostFunction()

nn.saveToFile(net, "Neural_Networks/.neuralnetwork.pkl")
