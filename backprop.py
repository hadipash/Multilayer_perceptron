import random
from data import *

eta = 0         # learning rate
alpha = 0.6     # coefficient of a momentum term
w = []          # matrix of weights
pw = []         # matrix of previous step weights (for a momentum term)
hidden = 2      # number of hidden layers (must be at least one)
nodes = 100     # number of nodes in each hidden layer


def init():
    global w, pw, eta, hidden, nodes

    # create weight matrices for each layer
    w = [[] for _ in range(hidden + 1)]
    pw = [[] for _ in range(hidden + 1)]

    # initialize weight matrices with random entries
    # first, weights between the input layer and the first hidden layer
    w[0] = np.array([[random.uniform(-0.5, 0.5) for _ in range(len(inp[0]))] for _ in range(nodes)])
    pw[0] = np.array([[0] * len(inp[0])] * nodes)

    # then, weights between hidden layers
    for i in range(1, hidden):
        w[i] = np.array([[random.uniform(-0.5, 0.5) for _ in range(nodes)] for _ in range(nodes)])
        pw[i] = np.array([[0] * nodes] * nodes)

    # finally, weights between the last hidden layer and the output layer
    w[hidden] = np.array([[random.uniform(-0.5, 0.5) for _ in range(nodes)] for _ in range(len(out[0]))])
    pw[hidden] = np.array([[0] * nodes] * len(out[0]))

    # set a learning rate
    while eta == 0:
        try:
            eta = float(input('Input a learning rate: '))
            if eta <= 0 or eta > 1:
                print("Learning rate should be within 0 and 1!")
                eta = 0
        except ValueError:
            print('Not a number')


def train():
    print("Training...")
    done = False  # training is finished
    iteration = 0

    while not done:
        iteration += 1
        if iteration % 100 == 0:
            print("Iteration #%d" % iteration)
        done = True

        for i in range(len(inp)):
            # multiply input data by weights
            product = [[] for _ in range(hidden + 1)]
            product[0] = np.dot(inp[i], np.transpose(w[0]))
            # apply activation function (sigmoid)
            product[0] = np.array([1 / (1 + np.exp(-x)) for x in product[0]])
            # calculate remain products for each layer
            for j in range(1, hidden + 1):
                product[j] = np.dot(product[j - 1], np.transpose(w[j]))
                product[j] = np.array([1 / (1 + np.exp(-x)) for x in product[j]])

            # apply step function at the output layer to compare output values with the target values
            step = [(1 if x > 0.5 else 0) for x in product[hidden]]

            # compare actual values to the target values
            for j in range(len(step)):
                if not step[j] == out[i][j]:
                    done = False
                    break

            if not done:
                # starting with delta for the output layer
                # delta = y * (1 - y) * (T - y), where y - actual output, T - target value
                delta = product[hidden] * (1 - product[hidden]) * (out[i] - product[hidden])
                updateWeights(hidden, product[hidden - 1], delta)

                # continuing to hidden layers
                # We perform the actual updates in the neural network after we have the new weights
                # leading into the hidden layer neurons (ie, we use the original weights, not the updated weights,
                # when we continue the backpropagation algorithm below)
                # Therefore we use pw[] matrix for calculation of delta, not w[] matrix
                for j in range(hidden - 1, 0, -1):
                    temp = []
                    for k in range(len(pw[j + 1][0])):
                        dsum = 0
                        for l in range(len(pw[j + 1])):
                            dsum += delta[l] * pw[j + 1][l][k]
                        temp.append(dsum)
                    # delta = z * (1 - z) * sum(D * w), where z - output of an upper layer,
                    # D - delta from an upper layer and w - weights
                    delta = product[j] * (1 - product[j]) * temp
                    updateWeights(j, product[j - 1], delta)

                # and then move to the input layer
                temp = []
                for k in range(len(pw[1][0])):
                    dsum = 0
                    for l in range(len(pw[1])):
                        dsum += delta[l] * pw[1][l][k]
                    temp.append(dsum)
                delta = product[0] * (1 - product[0]) * temp
                updateWeights(0, inp[i], delta)


def updateWeights(layer, inp_in, delta):
    global w, pw, eta, alpha
    # save current weight matrix
    temp = w[layer]
    # update weights
    w[layer] = np.array([w[layer][x] + eta * delta[x] * inp_in + alpha * (w[layer][x] - pw[layer][x])
                        for x in range(len(w[layer]))])
    # update matrix of previous weights
    pw[layer] = temp


def findNum(num):
    # generate output values
    product = [[] for _ in range(hidden + 1)]
    product[0] = np.dot(num, np.transpose(w[0]))
    product[0] = np.array([1 / (1 + np.exp(-x)) for x in product[0]])

    for j in range(1, hidden + 1):
        product[j] = np.dot(product[j - 1], np.transpose(w[j]))
        product[j] = np.array([1 / (1 + np.exp(-x)) for x in product[j]])

    # apply step function on the output layer to compare output values with the target values
    temp = [(1 if x >= 0.5 else 0) for x in product[hidden]]

    # convert the output value into decimal representation
    for i in range(len(out)):
        if (temp == out[i]).all():
            return rep[i]
    return None
