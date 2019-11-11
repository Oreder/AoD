import numpy as np
import pandas as pd

outputs = pd.read_csv('src/divF.csv').values
inputs = pd.read_csv('src/U.csv').values

'''
    Guest that: divF = M * U
    Here,   divF: 192 x 81
            U:    192 x 81
            M:    n x n
'''

__SCALE_DB__ = 1e+10

from random import sample
def select(population, n):
    """
    Select random n members among population without duplicates
    """
    return sample(population, n)

def getInputs(inputs, indexes):
    """
    Get n samples of inputs by given indexes
    """
    X = list()
    for index in indexes:
        X.append(inputs[index] * __SCALE_DB__)
    return X 

def getOutputs(outputs, indexes):
    """
    Get n samples of outputs by given indexes
    """
    Y = list()
    for index in indexes:
        Y.append(outputs[index])
    return Y

def operator(X, Y):
    A = list()
    for p in range(len(Y)):
        Yp = [y[p] for y in Y]          # p-th column
        Ap = np.linalg.solve(X, Yp)     # test scale by 1e-8
        A.append(Ap)
    return A

def MSE(X, Y):
    return sum((x - y)**2 for x, y in zip(X, Y))

def dot(A, X):
    Y = list()
    for k in range(len(A)):
        y = sum(a * x for a, x in zip(A[k], X))
        Y.append(y)
    return np.array(Y)

def processError(indexes, inputs, outputs, A):
    error = 0.0
    for index in indexes:
        x = inputs[index] * __SCALE_DB__
        y = dot(A, x)                   # test scale back by 1e+8
        error += MSE(y, outputs[index])
    return error

def process(indexes):
    X = getInputs(inputs, indexes)      # inputs
    Y = getOutputs(outputs, indexes)    # outputs    
    A = operator(X, Y)                  # solution      
    
    Q = set(range(kMax)) - set(indexes) # backtrack-range
    e = processError(Q, inputs, outputs, A)     # MSE
    return e, A

import time
if __name__ == "__main__":
    k    = len(inputs[0])   # rank(A)
    kMax = len(inputs)      # max population's shape

    startTime = time.clock()
    indexes = range(k)      # begining k-sample
    Est, A = process(indexes)
    # print('Begining error of k sample is {:.5f}'.format(Est))

    for i in range(20):
        indexes = select(range(kMax), k)    # get sample
        e, a = process(indexes)
        # print('#{:2d} Error={:.5f}'.format(i, e))
        if e < Est:
            Est, A = e, a
    elapsed_time = time.clock() - startTime
    print('Time excution: {:5f}\nMSE of k sample is {:5f}'.format(elapsed_time, Est))
    # print('Operator:')
    # print(A)    
    np.savetxt('exp/k={:d}.csv'.format(k), A, delimiter=',', fmt='%f')