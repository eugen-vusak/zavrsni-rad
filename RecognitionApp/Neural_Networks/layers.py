import numpy as np


# class layer used to model standard layer
class Layer:

    Z = None
    A = None

    error = None
    delta = None

    pC_pW = 0
    pC_pB = 0

    def __init__(self, input_size, output_size, function, name=None):
        self.name = name

        self.input_size = input_size
        self.output_size = output_size

        self.function = function

        self.weights = np.random.random((output_size, input_size))
        self.biases = np.random.random((output_size, 1))

    def output(self, input):

        self.Z = np.dot(self.weights, input) + self.biases
        self.A = self.function(self)

        return self.A

    def updateParametars(self, batch_size, learning_rate):

        self.weights = self.weights - learning_rate * self.pC_pW / batch_size
        self.biases = self.biases - learning_rate * self.pC_pB / batch_size

        self.pC_pW = self.pC_pB = 0

    def __repr__(self):
        return "{}({})".format(self.name, self.output_size)


# special type of layer
class InputLayer():

    Z = None
    A = None

    def __init__(self, output_size, function, name=None):
        self.name = name
        self.output_size = output_size
        self.function = function

    def output(self, input):
        self.Z = input
        self.A = self.function(self)
        return self.A

    def __repr__(self):
        return "{}({})".format(self.name, self.output_size)

    def updateParametars(self, batch_size, learning_rate):
        pass
