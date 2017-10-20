from time import time as tictoc

import numpy as np
from numpy import multiply as mult
from scipy.optimize import root

__all__ = ["parameters", "func_base_mr"]
__author__ = "Serge Shikher"
__project__ = "Baseline"
__created__ = "8-31-2017"
__altered__ = "9-28-2017"
__version__ = "1.0.0"

__description__ = "This program will solve for the baseline multilateral resistances. Note that the last IMR is normalized to 1"


class parameters(object):
    def __init__(self, trade_costs, y1, y2, number_of_countries):
        self.trade_costs = trade_costs
        self.y1 = y1
        self.y2 = y2
        self.number_of_countries = number_of_countries


def func_base_mr(x, params):
    # params includes T, y1, y2, N
    # T is trade cost, 2NxN
    # y1=q/sum(q), y2=(phi*q)/sum(phi*q), both are Nx1
    # N is the number of countries
    N = params.number_of_countries
    x1 = x[0:(0 + N - 1)]  # x1 is IMR, N-1 elements
    x2 = x[(N - 1):] * 1000  # x2 is OMR, N elements; multiplication by 1000 is done to correct the scaling problem
    T1 = params.trade_costs[0:(0 + N - 1), :]  # trade costs for IMR
    T2 = params.trade_costs[N:, :]  # trade costs for OMR
    out = [1 - mult(x1[i], sum(mult(mult(T1[i, :], params.y1), x2))) for i in range(0, (0 + N - 1))]
    x1 = np.append(x1, 1)  # last IMR is normalized
    out.extend([1 - mult(x2[i], sum(mult(mult(T2[i, :], params.y2), x1))) for i in range(0, (0 + N))])
    # if min(x)<=0: # this is not needed with a properly written function and starting values
    #    out=[i+1000 for i in out]
    return out


# output_pd=pd.read_csv('output.csv',names=['output'])
output = np.genfromtxt('output.csv', delimiter=',')  # import output vector
phi = np.genfromtxt('phis.csv', delimiter=',')  # input vector of phis=E/Y
T = np.genfromtxt('trade_costs_bsln.csv', delimiter=',')  # input the matrix of trade costs
N = 41  # number of countries
params = parameters(T, output / sum(output), mult(phi, output) / sum(mult(phi, output)), N)  # set parameter vales
x0 = [1] * (2 * 41 - 1)  # set starting values
# test=func_base_mr1(x0,params) # this is used to test the function if needed
# x = fsolve(func_base_mr1, x0, args=params) # fsolve is a wrapper for root with 'hybr', but root provides more information
# print("The solution is",x)
tic = tictoc()  # get the initial clock value
res = root(func_base_mr, x0, args=params, method='hybr', tol=1e-8, options={'xtol': 1e-8, 'maxfev': 1400})
# algorithms that can be used: hybr, lm, broyden2, krylov, and possibly others
toc = tictoc()  # get the final clock value
# print("The solution is",x)
print(toc - tic)  # print execution time

imr_baseline = res.x[0:(0 + N - 1)]  # inverse of IMR
imr_baseline = np.append(imr_baseline, 1)  # last IMR is normalized
omr_baseline = res.x[(N - 1):] * 1000  # inverse of OMR
