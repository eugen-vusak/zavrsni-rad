import numpy as np
import Data.gestures as gestures


class Data:
    def __init__(self, csv_file, input_size=0):

        self.data_set = []
        self.index = 0

        # open file
        with open(csv_file, "r") as file:

            for line in file:
                line = line.strip()

                # skip empty lines
                if not line:
                    continue

                parts = line.split(",")

                if input_size + 1 > len(parts):
                    print("ERROR: line doesn't have enough data", line)
                    exit(1)

                try:
                    output = np.array(
                        gestures.to_vector(parts[0])
                    ).reshape(12, 1)
                except Exception as e:
                    print(e)
                    print("ERROR: not possible to make array from", parts[0])
                    exit(1)

                try:
                    input = np.asfarray(
                        parts[1:]).reshape(input_size, 1)

                except Exception as e:
                    print(e)
                    print("ERROR: not possible to make float array from", line)
                    exit(1)

                data = (input, output)
                self.data_set.append(data)

    def __str__(self):
        string = ""
        first = True
        for data in self.data_set:
            if first:
                string += "\ninput\n{}\noutput\n{}".format(data[0], data[1])
                first = False
            else:
                string += "\n" + \
                    "\ninput\n{}\noutput\n{}".format(data[0], data[1])
        return string

    # gets sublist of data set, called mini batch, of specificied size
    def getNextMiniBatch(self, batch_size):
        minibatch = self.data_set[self.index:self.index + batch_size]
        self.index += batch_size
        return minibatch

    # sets pointer to begining of data
    def resetToBegining(self):
        self.index = 0

    # shuffles data set, for miniBatch
    def shuffle(self):
        np.random.shuffle(self.data_set)
