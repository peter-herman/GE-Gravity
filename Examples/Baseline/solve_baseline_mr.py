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
    x1 = x[0:(0 + N - 1)]  # x1 is IMR
    x2 = x[N:] * 1000  # x2 is OMR; multiplication by 1000 is done to correct the scaling problem
    T1 = params.trade_costs[0:(0 + N - 1), :]  # trade costs for IMR
    T2 = params.trade_costs[N:, :]  # trade costs for OMR
    out = [1 - mult(x1[i], sum(mult(mult(T1[i, :], params.y1), x2))) for i in range(0, (0 + N - 1))]
    out.append(1 - x[N - 1])  # this asks the algorithm to optimize a constant and makes convergence harder
    x1 = x[0:(0 + N)]  # x1 is IMR
    out.extend([1 - mult(x2[i], sum(mult(mult(T2[i, :], params.y2), x1))) for i in range(0, (0 + N))])
    # if min(x)<=0:
    #    out=[i+1000 for i in out]
    return out


# output_pd=pd.read_csv('output.csv',names=['output'])
output = np.genfromtxt('output.csv', delimiter=',')
phi = np.genfromtxt('phis.csv', delimiter=',')
T = np.genfromtxt('trade_costs_bsln.csv', delimiter=',')
params = parameters(T, output / sum(output), mult(phi, output) / sum(mult(phi, output)), 41)
x0 = [0.1] * (2 * 41)
# test=func_base_mr(x0,params)
# x = fsolve(func_base_mr, x0, args=params)
# print("The solution is",x)
tic = tictoc()
res = root(func_base_mr, x0, args=params, method='lm', tol=1e-15, options={'xtol': 1e-15, 'maxfev': 1400})
toc = tictoc()
# print("The solution is",res.x)
print(toc - tic)
