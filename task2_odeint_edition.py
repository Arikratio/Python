from sympy import Symbol, solve, lambdify, Matrix
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import sympy

def TwoParam(k1val, k1mval, k2val, k3val, k3mval):
    solution = solve([eq1, eq2], k1, y)
    k1_sol = solution[0][0]
    y_sol = solution[0][1]
    A = Matrix([eq1, eq2])
    var_vector = Matrix([x, y])
    jacA = A.jacobian(var_vector)
    detA = jacA.det()
    traceA = jacA.trace()

    k1_trace_sol = solve(traceA.subs(y,y_sol),k1)[0]
    k1m_trace_sol = solve(k1_trace_sol - k1_sol,k1m)[0]
    true_k1_trace_sol = k1_sol.subs(k1m,k1m_trace_sol)
    k1m_trace_y = lambdify((x, k1, k1m, k2, k3, k3m),k1m_trace_sol)
    k1_trace_y = lambdify((x, k1, k1m, k2, k3, k3m),true_k1_trace_sol)

    k1_det_sol = solve(detA.subs(y,y_sol),k1)[0]
    k1m_det_sol = solve(k1_det_sol - k1_sol,k1m)[0]
    true_k1_det_sol = k1_sol.subs(k1m,k1m_det_sol)
    k1m_det_y = lambdify((x, k1, k1m, k2, k3, k3m),k1m_det_sol)
    k1_det_y = lambdify((x, k1, k1m, k2, k3, k3m),true_k1_det_sol)

    plt.plot(k1_trace_y(X, k1val, k1mval, k2val, k3val, k3mval), k1m_trace_y(X, k1val, k1mval, k2val, k3val, k3mval),label='Линия нейтральности', color='r')
    plt.plot(k1_det_y(X, k1val, k1mval, k2val, k3val, k3mval), k1m_det_y(X, k1val, k1mval, k2val, k3val, k3mval),label='Линия кратности', color='b')
    plt.xlabel('k1')
    plt.ylabel('k1m')
    plt.xlim([0.0, 0.15])
    plt.ylim([0.0, 0.02])
    plt.legend()
    plt.show()
    return


def solveSystem(init, k1val, k1mval, k2val, k3val, k3mval, dt, iterations):

    f1 = lambdify((x, y, k1, k1m, k2, k3, k3m), eq1)
    f2 = lambdify((x, y, k3, k3m), eq2)
    def rhs(xy, times):
        return [f1(xy[0], xy[1], k1val, k1mval, k2val, k3val, k3mval), f2(xy[0], xy[1], k3val, k3mval)]
    times = np.arange(iterations) * dt
    return odeint(rhs, init, times), times


def autocol():
    res, times = solveSystem([0.5, 0.25], 0.12, 0.01, 0.95, 0.0032, 0.002, 0.01, 1e6)
    ax = plt.subplot(211)
    plt.plot(times, res[:, 0], 'b')
    plt.title('Релаксационные колебания')
    plt.ylabel('x')
    plt.xlabel('t')
    plt.grid()
    ax1 = plt.subplot(212)
    plt.plot(times, res[:, 1], 'r')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.grid()
    plt.show()
    return
def streamplot(k1val, k1mval, k2val, k3val, k3mval):
    f1 = lambdify((x, y, k1, k1m, k2, k3, k3m), eq1)
    f2 = lambdify((x, y, k3, k3m), eq2)
    Y, X = np.mgrid[0:0.5:5000j, 0:1:5000j]
    U = f1(X, Y, k1val, k1mval, k2val, k3val, k3mval)
    V = f2(X, Y, k3val, k3mval)
    velocity = np.sqrt(U*U+V*V)
    plt.streamplot(X, Y, U, V, density = [2, 2], color=velocity)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Фазовый портрет системы')
    plt.show()
    
    return

k1 = Symbol('k1', Positive=True)
k1m = Symbol('k1m', Positive=True)
k2 = Symbol('k2', Positive=True)
k3 = Symbol('k3', Positive=True)
k3m = Symbol('k3m', Positive=True)
x = Symbol("x", Positive=True)
y = Symbol("y", Positive=True)
eq1 = k1 * (1 - x - 2*y)- k1m*x - k3*x*(1-x-2*y)+k3m*y-k2*x*(1-x-2*y)*(1-x-2*y)
eq2 = k3*x*(1-x-2*y)-k3m*y

X = np.arange(0, 1, 1e-3)
streamplot(0.12, 0.01, 0.95, 0.0032, 0.002)
TwoParam(0.12, 0.01, 0.95, 0.0032, 0.002)
autocol()