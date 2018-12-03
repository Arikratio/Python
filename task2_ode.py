from sympy import Symbol, solve, lambdify, Matrix
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


k1m = Symbol('k1m', Positive=True)
k3m = Symbol('k3m', Positive=True)
k3 = Symbol('k3', Positive=True)
k1 = Symbol('k1', Positive=True)
k2 = Symbol('k2', Positive=True)
x = Symbol("x", Positive=True)
y = Symbol("y", Positive=True)

eq1 = k1 * (1 - x - 2*y)- k1m*x - k3*x*(1-x-2*y)+k3m*y-k2*x*(1-x-2*y)*(1-x-2*y)
eq2 = k3*x*(1-x-2*y)-k3m*y


solution = solve([eq1, eq2], x, k1)
xSolution = solution[0][0]
k1Solution = solution[0][1]


A = Matrix([eq1, eq2])
var_vector = Matrix([x, y])
jacA = A.jacobian(var_vector)
detA = jacA.det()
traceA = jacA.trace()

Y = np.arange(0, 1, 1e-3)

def solveSystem(init, k1val, k1mval, k2val, k3val, k3mval, dt, iterations):

    f1 = lambdify((x, y, k1, k1m, k2, k3, k3m), eq1)
    f2 = lambdify((x, y, k3, k3m), eq2)
    def rhs(xy, times):
        return [f1(xy[0], xy[1], k1val, k1mval, k2val, k3val, k3mval), f2(xy[0], xy[1], k3val, k3mval)]
    times = np.arange(iterations) * dt
    return odeint(rhs, init, times), times
def autocol():
    res, times = solveSystem([0.38, 0.22], 0.12, 0.01, 0.95, 0.0032, 0.002, 1e-2, 1e6)

    ax = plt.subplot(211)
    plt.plot(times, res[:, 0])
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.ylabel('x')
    plt.grid()
    ax1 = plt.subplot(212, sharex=ax)
    plt.plot(times, res[:, 1], color='red')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.grid()
    fig=plt.figure()
    ax2 = fig.add_subplot(111)
    plt.plot(res[:, 0], res[:, 1], color='green')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.show()
    return
def streamplot(k1val, k1mval, k2val, k3val, k3mval):
    f1 = lambdify((x, y, k1, k1m, k2, k3, k3m), eq1)
    f2 = lambdify((x, y, k3, k3m), eq2)
    Y, X = np.mgrid[0:1:10j, 0:1:20j]
    U = f1(X, Y, k1val, k1mval, k2, k3, k3m)
    V = f2(X, Y, k3, k3m)
    velocity = np.sqrt(U*U+V*V)
    plt.streamplot(X, Y, U, V, density = [2.5, 0.8], color=velocity)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

#streamplot(0.12, 0.01, 0.95, 0.0032, 0.002)
#AnalysisK1K2()
autocol()
#AnalysisK1K2()
#AnalysisK2(0.03,0.01,0.01,10,16,1e-12)