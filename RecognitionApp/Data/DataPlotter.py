import matplotlib.pyplot as plt


# plots data on one graph with set names
def plot(data_set, names):
    for data, name in zip(data_set, names):
        plt.plot(
            [x for x in range(len(data))],
            data,
            label=name
        )
    plt.legend()
    plt.show()
