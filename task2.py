import matplotlib.pyplot as plt
import numpy as np

k2=0.95
k3=0.0032
k3m=0.002
#k1=0.12
#k1m=0.01
#alk = k3m/(k3m + k3)
num=1000
x=np.linspace(0, 0.999, num)
y=np.zeros(num)
z=np.zeros(num)
k1=np.zeros(num)
k1m=np.zeros(num)
K1=np.zeros(num)
K1m=np.zeros(num)
sp=np.zeros(num)
DI=np.zeros(num)
delta_a=np.zeros(num)
# расчет линии нейтральности
for i in range(num):
    y[i]=(1-x[i])*x[i]*k3/(k3m+2*k3*x[i])
    z[i] = (1-x[i]-2*y[i])
    k1m[i] = -(k2*z[i]*z[i]*(x[i]-z[i])-k3*z[i]*(1+x[i]-2*y[i])+k3m*(3*y[i]+x[i]-1))/(1-2*y[i])
    k1[i]= (k1m[i]*x[i]+k3*x[i]*z[i]-k3m*y[i]+k2*x[i]*z[i]*z[i])/z[i]
    a11 = -k1[i]-k1m[i]-k2*z[i]*z[i]+2*k2*x[i]*z[i]-k3*(1-2*y[i]-2*x[i])
    a12 = -2*k1[i]+2*k3*x[i]+k3m+4*k2*x[i]*z[i]
    a21 = k3*(1-2*x[i]-2*y[i])
    a22 = -2*k3*x[i]-k3m
    sp[i]= a11+a22
    delta_a[i]=a11*a22-a12*a21
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(k1, k1m, label='Линия нейтральности', color='r')
# расчет линии кратности
for i in range(num):
    y[i]=(1-x[i])*x[i]*k3/(k3m+2*k3*x[i])
    z[i] = (1-x[i]-2*y[i])
    K1m[i] = (k3m*k3m*y[i]+k3m*k3*z[i]*(2*y[i]-x[i])-k2*k3m*z[i]*z[i]*(z[i]-x[i]))/(4*k3*x[i]*z[i]+k3m*(x[i]+z[i]))
    K1[i]= (K1m[i]*x[i]+k3*x[i]*z[i]-k3m*y[i]+k2*x[i]*z[i]*z[i])/z[i]
    a11 = -K1[i]-K1m[i]-k2*z[i]*z[i]+2*k2*x[i]*z[i]-k3*(1-2*y[i]-2*x[i])
    a12 = -2*K1[i]+2*k3*x[i]+k3m+4*k2*x[i]*z[i]
    a21 = k3*(1-2*x[i]-2*y[i])
    a22 = -2*k3*x[i]-k3m
    sp[i]= a11+a22
    delta_a[i]=a11*a22-a12*a21
ax1 = fig.add_subplot(111)
ax1.plot(K1, K1m, label='Линия кратности', color='b')
plt.xlabel(u'K1')
plt.ylabel(u'K1m')
plt.legend()
# однопараметрический анализ по параметру k1
k2=0.95
k3=0.0032
k3m=0.002
#k1=0.12
k1m=0.01 
num=1000
x=np.linspace(0, 0.999, num)
yh=np.zeros(num)
xh=np.zeros(num)
k1h=np.zeros(num)
ysn=np.zeros(num)
xsn=np.zeros(num)
k1sn=np.zeros(num)
ydi=np.zeros(num)
xdi=np.zeros(num)
k1di=np.zeros(num)
j1 = 0
j2 = 0
j3 = 0
i=1
y[i]=(1-x[i])*x[i]*k3/(k3m+2*k3*x[i])
z[i] = (1-x[i]-2*y[i])
K1[i]= (k1m*x[i]+k3*x[i]*z[i]-k3m*y[i]+k2*x[i]*z[i]*z[i])/z[i]
a11 = -K1[i]-k1m-k2*z[i]*z[i]+2*k2*x[i]*z[i]-k3*(1-2*y[i]-2*x[i])
a12 = -2*K1[i]+2*k3*x[i]+k3m+4*k2*x[i]*z[i]
a21 = k3*(1-2*x[i]-2*y[i])
a22 = -2*k3*x[i]-k3m
sp[i]= a11+a22
delta_a[i]=a11*a22-a12*a21
DI[i] = sp[i]*sp[i]-4*delta_a[i]
for i in range(2,num):
    y[i]=((1-x[i])*x[i]*k3)/(k3m+2*k3*x[i])
    z[i] = 1-x[i]-2*y[i]
    K1[i]= (k1m*x[i]+k3*x[i]*z[i]-k3m*y[i]+k2*x[i]*z[i]*z[i])/z[i]
    a11 = -K1[i]-k1m-k2*z[i]*z[i]+2*k2*x[i]*z[i]-k3*(1-2*y[i]-2*x[i])
    a12 = -2*K1[i]+2*k3*x[i]+k3m+4*k2*x[i]*z[i]
    a21 = k3*(1-2*x[i]-2*y[i])
    a22 = -2*k3*x[i]-k3m
    sp[i]= a11+a22
    delta_a[i]=a11*a22-a12*a21
    DI[i] = sp[i]*sp[i]-4*delta_a[i]
    if (sp[i]*sp[i-1]<=0):
        j1+=1
        yh[j1]=y[i]
        xh[j1]=x[i]
        k1h[j1]=K1[i]
    if (delta_a[i]*delta_a[i-1]<=0):
        j2+=1
        ysn[j2]=y[i]
        xsn[j2]=x[i]
        k1sn[j2]=K1[i]
    if (DI[i]*DI[i-1]<=0):
        j3+=1
        ydi[j3]=y[i]
        xdi[j3]=x[i]
        k1di[j3]=K1[i]
mh=j1
msn=j2
mdi=j3

fig2 = plt.figure()
k1x_plot = fig2.add_subplot(111)
k1x_plot.plot(K1, x)
k1y_plot = fig2.add_subplot(111)
k1y_plot.plot(K1, y)
k1hxh_plot = fig2.add_subplot(111)
k1hxh_plot.plot(k1h, xh, '*')
k1hyh_plot = fig2.add_subplot(111)
k1hyh_plot.plot(k1h, yh, '*')
k1snxsn_plot = fig2.add_subplot(111)
k1snxsn_plot.plot(k1sn, xsn, 's')
k1snysn_plot = fig2.add_subplot(111)
k1snysn_plot.plot(k1sn, ysn, 's')


plt.show()