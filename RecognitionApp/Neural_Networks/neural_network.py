import numpy as np
import matplotlib.pyplot as plt
from layers import InputLayer
import pickle


# function for predprocessing data in input layer
def predprocess(layer):
    return layer.Z / 32768


# class for modeling simple feedforward neural network w/ backpropagation
class FeedForwardNeuralNetwork:

    def __init__(self, layers=[]):
        self.layers = layers
        self.ErrorAxis = []
        self.E = 0

    def addLayer(self, layer):
        self.layers.append(layer)

    def removeLayer(self, index):
        self.pop(index)

    def feedforward(self, input):
        for layer in self.layers:
            input = layer.output(input)
        return input

    def backpropagate(self, output, desired_output):

        # calculate for the last layer first
        output_layer = self.layers[-1]
        output_layer.error = output - desired_output

        self.E += (output_layer.error**2 / 2).sum()

        deriv = np.multiply(output_layer.A, 1 - output_layer.A)

        output_layer.delta = np.multiply(output_layer.error, deriv)

        # from penultimate layer to second layer
        for l in reversed(range(1, len(self.layers) - 1)):

                layer = self.layers[l]

                layer_plus_one = self.layers[l + 1]

                layer.error = np.dot(
                    layer_plus_one.weights.T,
                    layer_plus_one.delta
                )

                deriv = layer.function(layer, deriv=True)

                layer.delta = np.multiply(layer.error, deriv)

    def gradientDescent(self):

        for l in range(1, len(self.layers)):

            layer = self.layers[l]
            layer_minus_one = self.layers[l - 1]

            layer.pC_pW += np.dot(layer.delta, layer_minus_one.A.T)
            layer.pC_pB += layer.delta

            # layer.weights = layer.weights - self.learning_rate * layer.pC_pW
            # layer.biases = layer.biases - self.learning_rate * layer.pC_pB

    def train(self, training_data, epochs=200, learning_rate=0.5):

        for i in range(epochs):
            print("epoch", i)
            for data in training_data.data_set:
                input, desired_output = data

                output = self.feedforward(input)

                self.backpropagate(output, desired_output)

                self.gradientDescent()

                for layer in self.layers:
                    layer.updateParametars(1, learning_rate)

            self.ErrorAxis.append(self.E / 745)
            self.E = 0

            # print(i)

    def batch_train(
        self,
        training_data,
        batch_size=32,
        epochs=200,
        learning_rate=0.5
    ):
        data_set_size = len(training_data.data_set)

        for i in range(epochs):
            print("epoch", i)

            training_data.resetToBegining()
            miniBatch = training_data.getNextMiniBatch(batch_size)

            while(miniBatch):

                for data in miniBatch:

                    input, desired_output = data
                    # 1. FeedForwardNeuralNetwork
                    output = self.feedforward(input)
                    # 2. backpropagation
                    self.backpropagate(output, desired_output)
                    # 3. gradientDescent
                    self.gradientDescent()

                    # update parametars for each layer
                    # after every mini batch
                    for layer in self.layers:
                        if type(layer) is InputLayer:
                            continue
                        layer.updateParametars(batch_size, learning_rate)

                miniBatch = training_data.getNextMiniBatch(batch_size)

                self.ErrorAxis.append(self.E / batch_size / data_set_size)
                self.E = 0

    def plotCostFunction(self):
        plt.plot([x for x in range(len(self.ErrorAxis))], self.ErrorAxis)
        plt.show()

    def __str__(self):
        string = ""
        first = True
        for layer in self.layers:
            if first:
                string += str(layer.output_size)
                first = False
            else:
                string += "->" + str(layer.output_size)

        return string


def saveToFile(o, file):
    with open(file, "wb") as output_file:
        pickle.dump(o, output_file, pickle.HIGHEST_PROTOCOL)


def loadFromFile(file):
    with open(file, "rb") as input_file:
        return pickle.load(input_file)


np.random.seed()
