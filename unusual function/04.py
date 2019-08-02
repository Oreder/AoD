from math import *
import numpy as np

x = np.arange(0, 1, 0.05)
# y = np.sin(x)
split = int(len(x) / 2)
m1 = np.max(x[:split])
y = [1 - 0.45 * pow(xt / m1, 8) for xt in x[:split]]
v = y[-1]
m1 = np.max(x[split:])
y = y + [0.8 * v - 0.35 * pow(xt / m1, 6.5) for xt in x[split:]]
y[split] = y[split] * 1.123
y[split+1] = y[split+1] * 1.01

# Tests
newX = np.arange(0.05, 0.93, 0.01)

# Spline
from scipy import interpolate
tck = interpolate.splrep(x, y, s=0)
Y_spline = interpolate.splev(newX, tck)

# Bline
from blib import Bline2
b = Bline2(x, y)
b.execute()
# print(b.A)
Y_Bline = b.interp(newX)

# WNN
from blib import WNN
wnn = WNN(Nh_wnn=len(x))#, plot_flag=True)
wnn.load_first_function(x, y)
wnn.train()
Y_wnn = wnn.d

# Plotting
import matplotlib.pyplot as plt
plt.figure()

d, =plt.plot(x, y, '.', label='Desired')

sp, = plt.plot(newX, Y_spline, label='Spline')
# plt.legend([d, sp], ['Desired', 'Spline'])

bi, = plt.plot(newX, Y_Bline, label='Bline')
# plt.legend([d, bi], ['Desired', 'Bline'])

wn, = plt.plot(x, Y_wnn, label='WNN')
# plt.legend([d, wn], ['Desired', 'WNN'])

plt.legend([d, sp, bi, wn], ['Desired', 'Spline', 'Bline', 'WNN'])
plt.show()