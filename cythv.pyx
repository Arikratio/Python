from libc.math cimport sqrt
import numpy as np

def cython_solver(int n, double G, double dt, m, x, y, z, vx, vy, vz, axm, aym, azm):
    cdef int j, f
    cdef double ax, ay, az
    for j in range(n):
        ax = 0
        ay = 0
        az = 0
        for f in range(n):
            if f != j:
                ax += m[f] * G * (x[f] - x[j]) / sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)
                ay += m[f] * G * (y[f] - y[j]) / sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)
                az += m[f] * G * (y[f] - y[j]) / sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)
        axm[j] = ax
        aym[j] = ay
        azm[j] = az
    for j in range(n):
        x[j] = x[j] + vx[j] * dt + 1.0 / 2 * axm[j] * dt ** 2
        y[j] = y[j] + vy[j] * dt + 1.0 / 2 * aym[j] * dt ** 2
        z[j] = z[j] + vz[j] * dt + 1.0 / 2 * azm[j] * dt ** 2
    for j in range(n):
        ax = 0
        ay = 0
        az = 0
        for f in range(n):
            if f != j:
                ax += m[f] * G * (x[f] - x[j]) / sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)
                ay += m[f] * G * (y[f] - y[j]) / sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)
                ay += m[f] * G * (z[f] - z[j]) / sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)/ sqrt((x[f] - x[j])**2 + (y[f] - y[j])**2 + (z[f] - z[j])**2)
        vx[j] = vx[j] + 1.0 / 2 * dt * (axm[j] + ax)
        vy[j] = vy[j] + 1.0 / 2 * dt * (aym[j] + ay)
        vz[j] = vz[j] + 1.0 / 2 * dt * (azm[j] + az)
        axm[j] = ax
        aym[j] = ay
        azm[j] = az
    return x, y, z, vx, vy, vz, axm, aym, azm