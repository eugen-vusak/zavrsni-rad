import Neural_Networks as nn
from Data import Data
import Data.gestures as gestures

net = nn.loadFromFile("Neural_Networks/.neuralnetwork.pkl")

# load testing data
testing_data = Data("Data/Datasets/gestures_test.csv", 360)


total_tests = 0
correct_tests = 0

# iterate over every data in data set
for current_data in testing_data.data_set:

    input_data, expected_output = current_data
    total_tests += 1

    expected_gesture = gestures.from_vector(expected_output)
    predicted_gesture = gestures.from_vector(net.feedforward(input_data))

    if expected_gesture == predicted_gesture:
        correct_tests += 1
    else:
        print('{:>15} --> {:<10}'.format(
            expected_gesture, str(predicted_gesture)
        ))

print(str(correct_tests / total_tests * 100) + "% tocnih primjera")
