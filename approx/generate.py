from math import *
import numpy as np

def f(x, a=1):
    return sin(exp(a * x))

def generate(fileName, start=0, end=2, n=20):
    X = np.linspace(start, end, n)
    Y = list()
    for a in range(1, n+1):
        Y.append([f(x, a) for x in X])

    with open('test/X.csv', 'w') as fs:
        line = X.join(',')
        fs.write(line)
    
    with open('test/Y.csv', 'w') as fs:
        for y in Y:
            line = y.join(',')
            fs.write(line)
        