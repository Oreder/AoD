import matplotlib.pyplot as plt
import numpy as np
from math  import sqrt, pi, pow, fabs

#======== how to use ==========
# wnn = WNN()
# wnn.load_function()
# wnn.train()

class WNN(object):
    def __init__(self, eta_wnn=0.008, epoch_max=20000, Ni_wnn=1, Nh_wnn=40, Ns=1, plot_flag=False):
        self.Ni_wnn = Ni_wnn
        self.eta_wnn = eta_wnn
        self.Nh_wnn = Nh_wnn
        self.Aini = 0.01

        self.epoch_max = epoch_max
        self.Ns = Ns
        self.plot_flag = plot_flag

    def load_function(self, X, Y):
        self.N = X.shape[0]
        xmax = fabs(np.max(X))
        # self.ymax = fabs(np.max(Y))
        self.X_train = X / xmax
        self.d = Y #/ ymax

    def sig_dev2(self, theta):
        return  2 * (1 / (1 + np.exp(-theta)))**3 - 3 * (1 / (1 + np.exp(-theta)))**2 + (1 / (1 + np.exp(-theta)))

    def sig_dev3(self, theta):
        return -6 * (1 / (1 + np.exp(-theta)))**4 + 12 * (1 / (1 + np.exp(-theta)))**3 - 7 * (1 / (1 + np.exp(-theta)))**2 + (1 / (1 + np.exp(-theta)))
    
    def train(self):
        # Initializing the weights
        self.A = np.random.rand(self.Ns, self.Nh_wnn) * self.Aini

        # Initializing the centers
        self.t = np.zeros((1, self.Nh_wnn))

        idx = np.random.permutation(self.Nh_wnn)
        for j in range(self.Nh_wnn):
            self.t[0,j] = self.d[idx[j]]
        
        # Initializing widths
        self.R = abs(np.max(self.t) - np.min(self.t)) / 2.0

        MSE_wnn = np.zeros(self.epoch_max)

        if self.plot_flag:
            plt.ion()

        for epoca in range(self.epoch_max):
            z_wnn = np.zeros(self.N)
            E_wnn = np.zeros(self.N)

            index = np.random.permutation(self.N)

            for i in index:
                xi = self.X_train[i] #np.array([self.X_train[i]]).reshape(1, -1)
                theta = (xi - self.t) / self.R
                yj = self.sig_dev2(theta)
                z_wnn[i] = np.dot(self.A, yj.T)[0][0]

                e = self.d[i] - z_wnn[i]
                self.A = self.A + (self.eta_wnn * e * yj)
                self.t = self.t - (self.eta_wnn * e * self.A / self.R * self.sig_dev3(theta))
                self.R = self.R - (((self.eta_wnn * e * self.A * (xi - self.t)) / self.R**2) * self.sig_dev3(theta))

                E_wnn[i] = 0.5 * e**2

            # MSE of WNN
            MSE_wnn[epoca] = np.sum(E_wnn) / self.N

            if self.plot_flag:
                if (epoca % 200 == 0 or epoca == self.epoch_max - 1):
                    if (epoca != 0):
                        plt.cla()
                        plt.clf()
                    
                    self.plot(z_wnn, epoca)
        
        print('MSE WNN: ', MSE_wnn[-1])

        if self.plot_flag:
            plt.ioff()
            plt.figure(1)
            mse_wnn, = plt.plot(np.arange(0, MSE_wnn.size), MSE_wnn, label="mse_wnn")
            plt.legend([mse_wnn], ['MSE of WNN'])
            plt.xlabel('Training Epochs')
            plt.ylabel('MSE')
            plt.show()

    def plot(self, Y_train, epoca):
        plt.figure(0)
        y_wnn, = plt.plot(self.X_train, Y_train, label="y_wnn")
        d, = plt.plot(self.X_train, self.d, '.', label="d")
        plt.legend([y_wnn, d], ['WNN', 'Desired Value'])
        plt.xlabel('x')
        plt.ylabel('f(x)')
        
        txtX = np.min(self.X_train) - np.max(self.X_train) * 0.17
        txtY = np.min(self.d) - np.max(self.d) * 0.17
        plt.text(txtX, txtY, 'Progress: ' + str(round(float(epoca) / self.epoch_max * 100, 2)) + '%')
        
        Xmin = np.min(self.X_train) - np.max(self.X_train) * 0.2
        Xmax = np.max(self.X_train) * 1.2
        Ymin = np.min(self.d) - np.max(self.d) * 0.2
        Ymax = np.max(self.d) * 1.4
        plt.axis([Xmin, Xmax, Ymin, Ymax])
        plt.show()
        fname = 'www/' + str(round(float(epoca) / self.epoch_max * 100, 2)) + '.png'
        plt.savefig(fname=fname, quality=95)
        plt.pause(1e-100)

    def show_function(self):
        plt.figure(0)
        plt.title('Function')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.plot(self.X_train, self.d)
        plt.show()


class Bline3(object):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.N = len(self.X) - 2
        self.A = np.zeros(self.N)
        self.B = np.zeros(self.N)
        self.C = np.zeros(self.N)
        self.D = np.zeros(self.N)

    def __g3(self, x, i, ai, bi, ci, di):
        return ai * (x - self.X[i]) * (x - self.X[i+1]) * (x - self.X[i+2]) + bi * (x - self.X[i]) * (x - self.X[i+1]) + ci * (x - self.X[i]) + di
    def __g2(self, x, i, bi, ci, di):
        return bi * (x - self.X[i]) * (x - self.X[i+1]) + ci * (x - self.X[i]) + di

    def execute(self):
        for i in range(self.N):
            self.D[i] = self.Y[i]
            self.C[i] = (self.Y[i+1] - self.Y[i]) / (self.X[i+1] - self.X[i])
            self.B[i] = 1.0 / (self.X[i+2] - self.X[i+1]) * ( (self.Y[i+2] - self.Y[i])/(self.X[i+2] - self.X[i]) - (self.Y[i+1] - self.Y[i])/(self.X[i+1] - self.X[i]) )
        
        dx = 0
        dy = 0
        for i in range(self.N-1):
            dx = (self.X[i+1] + self.X[i+2]) / 2
            y1 = self.__g2(dx, i+1,   self.B[i],   self.C[i],   self.D[i])
            y2 = self.__g2(dx, i+1, self.B[i+1], self.C[i+1], self.D[i+1])

            dy = (y1 + y2) / 2
            self.A[i] = (y2 - y1) / 2.0 / (dx - self.X[i]) / (dx - self.X[i+1]) / (dx - self.X[i+2])

        # the last segment
        self.A[-1] = self.A[-2]

    def index(self, x):
        left  = 0
        right = len(self.X) - 3

        if x < self.X[left]:
            return left
        elif x >= self.X[right]:
            return right
        else:         
            while right - left != 1:
                i = left + int((right - left) / 2)
                if x >= self.X[i]:
                    left = i
                else:
                    right = i
            
            return left
    
    def interp(self, newX):
        newY = np.zeros(len(newX))
        for i in range(len(newX)):
            j = self.index(newX[i])
            newY[i] = self.__g3(newX[i], j, self.A[j], self.B[j], self.C[j], self.D[j])

        return newY

class Bline2(object):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.N = len(self.X) - 2
        self.A = np.zeros(self.N)
        self.B = np.zeros(self.N)
        self.C = np.zeros(self.N)

    def __g2(self, x, i):
        return self.A[i] * (x - self.X[i]) * (x - self.X[i+1]) + self.B[i] * (x - self.X[i]) + self.C[i]

    def execute(self):
        for i in range(self.N):
            self.C[i] = self.Y[i]
            self.B[i] = (self.Y[i+1] - self.Y[i]) / (self.X[i+1] - self.X[i])
            self.A[i] = 1.0 / (self.X[i+2] - self.X[i+1]) * ( (self.Y[i+2] - self.Y[i])/(self.X[i+2] - self.X[i]) - (self.Y[i+1] - self.Y[i])/(self.X[i+1] - self.X[i]) )

    def index(self, x):
        left  = 0
        right = self.N - 1

        if x < self.X[left]:
            return left
        elif x >= self.X[right]:
            return right
        else:         
            while right - left != 1:
                i = left + int((right - left) / 2)
                if x >= self.X[i]:
                    left = i
                else:
                    right = i
            
            return left
    
    def interp(self, newX):
        newY = np.zeros(len(newX))
        for i in range(len(newX)):
            j = self.index(newX[i])
            newY[i] = self.__g2(newX[i], j)

        return newY