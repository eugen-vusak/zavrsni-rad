import numpy as np


def sigmoid(layer, deriv=False):
    if deriv:
        return np.multiply(layer.A, (1 - layer.A))

    return 1 / (1 + np.exp(-layer.Z))


def tanh(layer, deriv=False):
    if deriv:
        return 1 - layer.A**2

    return np.tanh(-layer.Z)


def identity(layer, deriv=False):
    if deriv:
        return 1
    return layer
