import numpy as np
import pandas as pd
from scipy.linalg import solve

def operator(X, Y):
    return np.matmul(Y, np.linalg.inv(X))

def MSE(X, Y):
    return sum((x - y)**2 for x, y in zip(X, Y))

outputs = np.array(pd.read_csv('D.csv').values)
inputs = np.array(pd.read_csv('T.csv').values)

transpose_outputs = np.transpose(outputs)
b = transpose_outputs[0]

a = solve(inputs, b)

print(inputs.dot(a))
print(transpose_outputs[0])
A = operator(inputs, outputs)                   # solution      

for i in range(len(outputs)):
    print(outputs[i][0])

print(inputs[0])
test_outputs = pd.read_csv('_D.csv').values
test_inputs = pd.read_csv('_T.csv').values

z = [test_inputs[1]]
z = np.transpose(z)

new_outputs = np.matmul(A, z)#np.transpose(np.matmul(A, z))[0]
# print(new_outputs)

sample = np.matmul(A, inputs)

for i in range(len(outputs)):
    for j in range(len(outputs[0])):
        print("{0}:{1}\t{2}".format(i, j, outputs[i][j] - sample[i][j]))

for i in range(len(test_inputs[1])):
    print("{0}\t{1}\t{2}".format(new_outputs[i], test_outputs[1][i], - test_outputs[1][i] + new_outputs[i]))

print("\nMSE: {0}", MSE(test_outputs[1], new_outputs))

# import numpy as np
# import pandas as pd

# a = np.array(pd.read_csv('T.csv').values)
# b = np.array(pd.read_csv('D.csv').values)
# x = np.linalg.solve(a,b)
# print(a[0])
# print(np.dot(a[0], x))
# print(b[0])