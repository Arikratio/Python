import sys
import math
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cython
import numpy as np
import math
import time
import os
import task_1_interface
import scipy.integrate
import copy
from multiprocessing import Barrier
import threading
import cythv

class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def module(self, coordinate):
        return math.sqrt((self.x - coordinate.x)**2 + (self.y - coordinate.y)**2 + (self.z - coordinate.z)**2)
        
class Velocity:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w
    
class Particle:
    def __init__(self, coordinate, velocity, m, color, time):
        self.coordinate = coordinate
        self.x = self.coordinate.x
        self.y = self.coordinate.y
        self.z = self.coordinate.z
        self.velocity = velocity
        self.u = self.velocity.u
        self.v = self.velocity.v
        self.w = self.velocity.w
        self.m = m
        self.color = color   
        self.alive = time


class Interface(QMainWindow, task_1_interface.Ui_MainWindow, QOpenGLWidget):
   
    part_list = []
    dt = 1000

    def __init__(self):
        super().__init__()
        global dt
        self.Angle_x = 0
        self.Angle_y = 0
        self.zoom = 1000
        self.lastPos = QPoint()
        self._color = QColor(255, 0, 0)
        #self.dt = 1000
        dt=1000
        self.setupUi(self) 
        self.timer = QTimer() 
        self.timer.timeout.connect(self.draw)
        self.timer.start(dt)
        self.color_button.clicked.connect(self.button_selectColor) 
        self.add_button.clicked.connect(self.button_add)
        self.add_random_button.clicked.connect(self.button_add_random)
        self.count_combo.currentIndexChanged.connect(self.combobox_numberChoice)
        
    
    def button_selectColor(self):
        qcolor = QColorDialog.getColor()
        p = self.color_test.palette()
        self._color = QColor(qcolor)
        p.setColor(QPalette.Background, QColor(qcolor))
        self.color_test.setPalette(p)
        self.color_test.show()
        
    def button_add(self):
        global part_list  
        global dt
        emit = Coordinate(float(self.c_x.toPlainText()), float(self.c_y.toPlainText()), float(self.c_z.toPlainText())) 
        vel = Velocity(float(self.v_x.toPlainText())/10000, float(self.v_y.toPlainText())/10000, float(self.v_z.toPlainText())/10000)
        part_list.append(Particle(emit, vel, float(self.mass.toPlainText()), self._color.getRgbF(), dt*int(self.time.toPlainText())))  
        print(dt*int(self.time.toPlainText()))   
        self.gl_sys.update()

    def button_add_random(self):
        global part_list
        global dt
        part_list.append(Particle(Coordinate(random.randint(-500, 500), random.randint(-500, 500), random.randint(-500, 500)), Velocity(random.randint(-5, 5) / 10000.0, random.randint(-5, 5) / 10000.0, random.randint(-5, 5) / 10000.0), random.randint(100, 1000), [random.randint(0, 255)/255.0, random.randint(0, 255)/255.0, random.randint(0, 255)/255.0], dt*random.randint(10, 1000)))     
        self.gl_sys.update()
        
    def combobox_numberChoice(self):
        global part_list 
        global dt       
        self.zoom = 1000
        part_count = 0
        
        if self.count_combo.currentIndex() == 0:
            part_count = 100
        elif self.count_combo.currentIndex() == 1:
            part_count = 200
        elif self.count_combo.currentIndex() == 2:
            part_count = 500
        elif self.count_combo.currentIndex() == 3:
            part_count = 1000
        elif self.count_combo.currentIndex() == 4:
            part_count = 0
        if self.count_combo.currentIndex() != 5:  
            dt=1000     
            part_list = []  
            part_list.append(Particle(Coordinate(0,0,0), Velocity(0,0,0), 10000, (1,0,1), dt*1000))   
            for i in range(1, part_count):
                part_list.append(Particle(Coordinate(random.randint(-500, 500), random.randint(-500, 500), random.randint(-500, 500)), Velocity(random.randint(-5, 5) / 2000.0, random.randint(-5, 5) / 2000.0, random.randint(-5, 5) / 2000.0), random.randint(100, 1000), [random.randint(0, 255)/255.0, random.randint(0, 255)/255.0, random.randint(0, 255)/255.0], dt*random.randint(10, 1000)))
        else:
            self.zoom = 300
            dt=100000
            part_count = 10
            part_list = []
            part_list.append(Particle(Coordinate(0, 0, 0), Velocity(0, 0, 0), 332900, [1, 1, 0], dt**2))
            part_list.append(Particle(Coordinate(0.387, 0, 0), Velocity(0, 47870, 0), 0.055, [139/255.0,69/255.0,19/255.0], dt**2))
            part_list.append(Particle(Coordinate(0.7233, 0, 0), Velocity(0, 35020, 0), 0.815, [255/255.0,160/255.0,122/255.0], dt**2))
            part_list.append(Particle(Coordinate(1, 0, 0), Velocity(0, 29760, 0), 1, [30/255.0,144/255.0,255/255.0], dt**2))
            part_list.append(Particle(Coordinate(1.524, 0, 0), Velocity(0, 24130, 0), 0.107, [255/255.0, 127/255.0, 0], dt**2))
            part_list.append(Particle(Coordinate(5.2, 0, 0), Velocity(0, 13070, 0), 318, [233/255.0,150/255.0,122/255.0], dt**2))
            part_list.append(Particle(Coordinate(10.0, 0, 0), Velocity(0, 9670, 0), 95.0, [255/255.0,222/255.0,173/255.0], dt**2))
            part_list.append(Particle(Coordinate(19.23, 0, 0), Velocity(0, 6840, 0), 14.6, [0, 0, 127/255.0], dt**2))
            part_list.append(Particle(Coordinate(30.07, 0, 0), Velocity(0, 5480, 0), 17.1, [30/255.0, 100/255.0, 255/255.0], dt**2))
            part_list.append(Particle(Coordinate(39.48, 0, 0), Velocity(0, 4750, 0), 0.002, [255/255.0,218/255.0,185/255.0], dt**2))
        self.timer.start(dt)    
        self.gl_sys.update()
            
    def mousePressEvent(self, event):
        self.lastPos = event.pos()
        if event.buttons() & Qt.RightButton:           
            self.set_angle_x(0)
            self.set_angle_y(0)
            self.gl_sys.update()  

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            dx = event.x() - self.lastPos.x()
            dy = event.y() - self.lastPos.y()            
            self.set_angle_x(self.Angle_x + dy / 100)
            self.set_angle_y(self.Angle_y - dx / 100)

            self.lastPos = event.pos()
            self.gl_sys.update()  
            
            
    def set_angle_x(self, angle):
        if angle != self.Angle_x:
            self.Angle_x = angle

    def set_angle_y(self, angle):
        if angle != self.Angle_y:
            self.Angle_y = angle
            
            
    def wheelEvent(self, event):  
        if (self.zoom >= 5) & (self.zoom <= 2500):
            self.zoom -= event.angleDelta().y() / 10
            self.gl_sys.update()
        elif self.zoom < 5:
            self.zoom = 5
        else:
            self.zoom = 2500      

   

    def calculate(self):
        global dt
        G = 6.67408 * (10 ** -11)
        AEM=149.6*10**9
        Earth_mass=5.974*10**24
        dt = 1000
        timerStep = dt
        global part_list
        x_n = []
        y_n = []
        z_n = []
        u_n = []
        v_n = []
        w_n = []
        m_n = []
        col_n = []  
        t_n=[]      
        if self.count_combo.currentIndex() != 5: 
            G = 6.67408 * (10 ** -8)
            for partic in part_list:
                for par in part_list:
                    if (partic.coordinate.module(par.coordinate) > 0) & (partic.coordinate.module(par.coordinate) < (partic.m + par.m) / 100.0):
                        if partic.m >= par.m:
                            partic.m += par.m
                        else:
                            partic.alive = 0          
                if (partic.alive>0):
                    x_n.append(partic.x)
                    y_n.append(partic.y)
                    z_n.append(partic.z)
                    coordinate = [Coordinate(x, y, z) for x, y, z in zip(x_n, y_n, z_n)]
                    u_n.append(partic.u)
                    v_n.append(partic.v)
                    w_n.append(partic.w)
                    m_n.append(partic.m)
                    col_n.append(partic.color)
                    t_n.append(int(partic.alive)-timerStep)
        else:
            x_n = [p.x * AEM for p in part_list]
            y_n = [p.y * AEM for p in part_list]
            z_n = [p.z * AEM for p in part_list]
            coordinate = [Coordinate(x, y, z) for x, y, z in zip(x_n, y_n, z_n)]
            u_n = [p.u for p in part_list]
            v_n = [p.v for p in part_list]
            w_n = [p.w for p in part_list]
            m_n = [p.m * Earth_mass for p in part_list]
            col_n = [p.color for p in part_list]  
            timerStep=100000
            t_n=[p.alive-timerStep for p in part_list]         
        length = len(x_n) 

        

        if self.method_combo.currentIndex()==0:
            ax_n = []
            ay_n = []
            az_n = []
            for cx, cy, cz in zip(x_n, y_n, z_n):            
                part = Coordinate(cx, cy, cz)
                ax = []
                ay = []
                az = []
                for c,m in zip(coordinate, m_n):
                    module = part.module(c)
                    if module > 0:
                        ax.append(G*m * (c.x - cx) / module / module / module )
                        ay.append(G*m * (c.y - cy) / module / module / module )
                        az.append(G*m * (c.z - cz) / module / module / module )

                ax_n.append(sum(ax))
                ay_n.append(sum(ay))
                az_n.append(sum(az))
            start_time = time.clock()  
            x_n1 = [x + u*timerStep + 0.5*a*timerStep**2 
                    for x, u, a in zip(x_n, u_n, ax_n)]
            y_n1 = [y + v*timerStep + 0.5*a*timerStep**2 
                    for y, v, a in zip(y_n, v_n, ay_n)]
            z_n1 = [z + w*timerStep + 0.5*a*timerStep**2 
                    for z, w, a in zip(z_n, w_n, az_n)]
            
            ax_n1 = []
            ay_n1 = []
            az_n1 = []
            for cx, cy, cz in zip(x_n1, y_n1, z_n1):
                part = Coordinate(cx, cy, cz)
                ax = []
                ay = []
                az = []
                for x, y, z, m in zip(x_n1, y_n1, z_n1, m_n):
                    c = Coordinate(x, y, z) 
                    module = part.module(c)
                    if module > 0:
                        ax.append(G*m * (x - cx) / module / module / module )
                        ay.append(G*m * (y - cy) / module / module / module )
                        az.append(G*m * (z - cz) / module / module / module )
                        
                ax_n1.append(sum(ax))
                ay_n1.append(sum(ay))
                az_n1.append(sum(az))
                
            u_n1 = [u + 0.5*(an + an1)*timerStep
                    for u, an, an1 in zip(u_n, ax_n, ax_n1)]
            v_n1 = [v + 0.5*(an + an1)*timerStep
                    for v, an, an1 in zip(v_n, ay_n, ay_n1)]
            w_n1 = [w + 0.5*(an + an1)*timerStep
                    for w, an, an1 in zip(w_n, az_n, az_n1)]
            
            part_list = []
            if self.count_combo.currentIndex() != 5: 
                for i in range(length):
                    coordinate = Coordinate(x_n1[i], y_n1[i], z_n1[i])
                    velocity = Velocity(u_n1[i], v_n1[i], w_n1[i])
                    part_list.append(Particle(coordinate, velocity, m_n[i], col_n[i], t_n[i]))
            else:
                for i in range(length):
                    coordinate = Coordinate(x_n1[i]/AEM, y_n1[i]/AEM, z_n1[i]/AEM)
                    velocity = Velocity(u_n1[i], v_n1[i], w_n1[i])
                    part_list.append(Particle(coordinate, velocity, m_n[i]/Earth_mass, col_n[i], t_n[i]))
            computing_time = time.clock()-start_time
            print(time.clock()-start_time)






        if  self.method_combo.currentIndex()==1:
            start_time = time.clock()
            mass = []
            xyz = []
            Vxyz = []
            color_ = []
            res = []
            time_span=np.linspace(0,timerStep, 7) 
            n_ = len(part_list)
            for p in part_list:
                    time.sleep(1)
                    xyz.append(p.x)
                    xyz.append(p.y)
                    xyz.append(p.z)
                    Vxyz.append(p.u)
                    Vxyz.append(p.v)
                    Vxyz.append(p.w)
                    mass.append(p.m)
                    color_.append(p.color)
            init_cond = sum([list(map(float, xyz)), list(map(float, Vxyz))], [])
            
            del res [:]
            res = scipy.integrate.odeint(self.for__scipy, init_cond, time_span, args=(n_,list(map(float,mass))))
            x_n1 =[]
            y_n1 =[]
            z_n1 = []
            vx_n1 =[]
            vy_n1 = []
            vz_n1 = []
            for i in range(1,len(res)):
                for j in range(n_):
                    x_n1.append(res[i][j*3])
                    y_n1.append(res[i][j*3+1])
                    z_n1.append(res[i][j*3+2])
                    vx_n1.append(res[i][j*3 + 3*n_])
                    vy_n1.append(res[i][j*3 + 3*n_ + 1])
                    vz_n1.append(res[i][j*3 + 3*n_ + 2])
            
            part_list=[]
            if self.count_combo.currentIndex() != 5: 
                for i in range(n_):
                    coordinate = Coordinate(x_n1[i], y_n1[i], z_n1[i])
                    velocity = Velocity(vx_n1[i], vy_n1[i], vz_n1[i])
                    part_list.append(Particle(coordinate, velocity, m_n[i], col_n[i], t_n[i]))
            else:
                for i in range(n_):
                    coordinate = Coordinate(x_n1[i]/AEM, y_n1[i]/AEM, z_n1[i]/AEM)
                    velocity = Velocity(vx_n1[i], vy_n1[i], vz_n1[i])
                    part_list.append(Particle(coordinate, velocity, m_n[i]/Earth_mass, col_n[i], t_n[i]))
            computing_time = time.clock()-start_time
            print(time.clock()-start_time)
            





        if  self.method_combo.currentIndex()==2:
            start_time = time.clock()
            print('VERLET_THREADING')
            mass = []
            xyz = []
            Vxyz = []
            color_ = []
            res = []
            n_ = len(x_n)
            print('тут', n_)
            if (n_!=0):
                x = np.zeros(n_)
                y = np.zeros(n_)
                z = np.zeros(n_)
                vx = np.zeros(n_)
                vy = np.zeros(n_)
                vz = np.zeros(n_)
                mass=np.zeros(n_)
                for i in range(n_):
                    x[i] = x_n[i]
                    y[i] = y_n[i]
                    z[i] = z_n[i]
                    vx[i] = u_n[i]
                    vy[i] = v_n[i]
                    vz[i] = w_n[i]
                    mass[i]=m_n[i]
                axm = np.zeros(n_)
                aym = np.zeros(n_)
                azm = np.zeros(n_)
                for j in range(n_):
                    ax_ = 0
                    ay_ = 0
                    az_ = 0
                    for k in range(n_):
                        if k != j:
                            ax_ += mass[k] * G * (x[k] - x[j]) / math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)/ math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)/ math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)
                            ay_ += mass[k] * G * (y[k] - y[j]) / math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)/ math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)/ math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)
                            az_ += mass[k] * G * (z[k] - z[j]) / math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)/ math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)/ math.sqrt((x[k]-x[j])**2 + (y[k]-y[j])**2 + (z[k]-z[j])**2)
                    axm[j] = ax_
                    aym[j] = ay_
                    azm[j] = az_
                for j in range(n_):
                    thread = self.MyThread(n_, j, timerStep, G, x, vx, mass, axm, y, vy, aym, z, vz, azm)
                    thread.start()  
                computing_time = time.clock()-start_time
                print(time.clock()-start_time)
                part_list = []
                if self.count_combo.currentIndex() != 5: 
                    for i in range(length):
                        coordinate = Coordinate(x[i], y[i], z[i])
                        velocity = Velocity(vx[i], vy[i], vz[i])
                        part_list.append(Particle(coordinate, velocity, m_n[i], col_n[i], t_n[i]))
                else:
                    for i in range(length):
                        coordinate = Coordinate(x[i]/AEM, y[i]/AEM, z[i]/AEM)
                        velocity = Velocity(vx[i], vy[i], vz[i])
                        part_list.append(Particle(coordinate, velocity, m_n[i]/Earth_mass, col_n[i], t_n[i]))

        
        if  self.method_combo.currentIndex()==3:
            n_ = len(part_list)
            mass = []
            xyz = []
            Vxyz = []
            color_ = []
            res = []
            x = np.zeros(n_)
            y = np.zeros(n_)
            z = np.zeros(n_)
            vx = np.zeros(n_)
            vy = np.zeros(n_)
            vz = np.zeros(n_)
            axm = np.zeros(n_)
            aym = np.zeros(n_)
            azm = np.zeros(n_)
            i = 0
            for p in part_list:
                x[i] = p.x
                y[i] = p.y
                z[i] = p.z
                vx[i] = p.u
                vy[i] = p.v
                vz[i] = p.w
                mass.append(p.m)
                color_.append(p.color)
                i = i+1
            m1 = np.array(mass)
            import pyximport
            pyximport.install(setup_args={'include_dirs': np.get_include()})
            
            start_time = time.clock()
            result = cythv.cython_solver(n_, G, timerStep, mass, x, y, z, vx, vy, vz, axm, aym, azm)
            time.sleep(1)
            print(result)

            computing_time = time.clock() - start_time
            print(time.clock()-start_time)
            part_list=[]
            if self.count_combo.currentIndex() != 5: 
                for i in range(length):
                    coordinate = Coordinate(result[0][i], result[1][i], result[2][i])
                    velocity = Velocity(result[3][i], result[4][i], result[5][i])
                    part_list.append(Particle(coordinate, velocity, m_n[i], col_n[i], t_n[i]))
            else:
                for i in range(length):
                    coordinate = Coordinate(result[0][i]/AEM, result[1][i]/AEM, result[2][i]/AEM)
                    velocity = Velocity(result[3][i], result[4][i], result[5][i])
                    part_list.append(Particle(coordinate, velocity, m_n[i]/Earth_mass, col_n[i], t_n[i]))

 
        if (self.timer.isActive()):
            self.gl_sys.update()  

    def for__scipy(self,init,t,n,mass):
        G = 6.67408e-11
        x_0 = []
        y_0 = []
        z_0 = []
        vx_0 = []
        vy_0 = []
        vz_0 = []
        #m = []
        color_ = []

        ax_n = []
        ay_n = []
        az_n = []
        ax_n1 = []
        ay_n1 = []
        az_n1 = []

        del x_0 [:] 
        del y_0 [:]
        del z_0 [:]
        del vx_0 [:]
        del vy_0 [:]
        del vz_0 [:]
        #del m [:]
        del color_ [:]

        del ax_n [:]
        del ay_n [:]
        del az_n [:]
        del ax_n1 [:]
        del ay_n1 [:]
        del az_n1 [:] 

        module = 0
        for i in range(n):
            x_0.append(init[i*3])
            y_0.append(init[i*3 + 1])
            z_0.append(init[i*3 + 2])
            vx_0.append(init[i*3 + 3*n])
            vy_0.append(init[i*3 + 3*n + 1])
            vz_0.append(init[i*3 + 3*n + 2])
        result = []
        del result [:]
        n_ = n
        for i in range(n_):
            result.append(vx_0[i])
            result.append(vy_0[i])
            result.append(vz_0[i])
        for j in range(n_):
            ax_ = 0
            ay_ = 0
            az_ = 0
            for k in range(n_):
                if k != j:
                    ax_ += mass[k] * G * (x_0[k] - x_0[j]) / math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)/ math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)/ math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)
                    ay_ += mass[k] * G * (y_0[k] - y_0[j]) / math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)/ math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)/ math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)
                    az_ += mass[k] * G * (z_0[k] - z_0[j]) / math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)/ math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)/ math.sqrt((x_0[k]-x_0[j])**2 + (y_0[k]-y_0[j])**2 + (z_0[k]-z_0[j])**2)
            result.append(ax_)
            result.append(ay_)
            result.append(az_)
        return result

    class MyThread(threading.Thread):
        def __init__(self,n, j, dt, G, x, vx, m, axm, y, vy, aym, z, vz, azm):
            threading.Thread.__init__(self)
            self.n = n
            self.j = j
            self.dt = dt
            self.G = G
            self.vx = vx
            self.x = x
            self.m = m
            self.axm = axm
            self.y = y
            self.vy = vy
            self.aym = aym
            self.z = z
            self.vz = vz
            self.azm = azm
        
        def run(self):
            msg = "%s is running" % self.name
            
            self.x[self.j] = self.x[self.j] + self.vx[self.j] * self.dt + 1.0 / 2 * self.axm[self.j] * self.dt ** 2
            self.y[self.j] = self.y[self.j] + self.vy[self.j] * self.dt + 1.0 / 2 * self.aym[self.j] * self.dt ** 2
            self.z[self.j] = self.z[self.j] + self.vz[self.j] * self.dt + 1.0 / 2 * self.azm[self.j] * self.dt ** 2
            ax = 0
            ay = 0
            az = 0
            for f in range(self.n):
                if f != self.j:
                    ax += self.m[f] * self.G * (self.x[f] - self.x[self.j]) / \
                            math.sqrt((self.x[f] - self.x[self.j])**2 + (self.y[f] - self.y[self.j])**2 + (self.z[f] - self.z[self.j])**2) ** 3
                    ay += self.m[f] * self.G * (self.y[f] - self.y[self.j]) /\
                            math.sqrt((self.x[f] - self.x[self.j])**2 + (self.y[f] - self.y[self.j])**2 + (self.z[f] - self.z[self.j])**2) ** 3
                    az += self.m[f] * self.G * (self.z[f] - self.z[self.j]) /\
                            math.sqrt((self.x[f] - self.x[self.j])**2 + (self.y[f] - self.y[self.j])**2 + (self.z[f] - self.z[self.j])**2) ** 3
            
            self.vx[self.j] = self.vx[self.j] + 1.0 / 2 * self.dt * (self.axm[self.j] + ax)
            self.vy[self.j] = self.vy[self.j] + 1.0 / 2 * self.dt * (self.aym[self.j] + ay)
            self.vz[self.j] = self.vz[self.j] + 1.0 / 2 * self.dt * (self.azm[self.j] + az)
            self.axm[self.j] = ax
            self.aym[self.j] = ay
            self.azm[self.j] = az 

    def setupGL(self):

        self.gl_sys.initializeGL()
        self.gl_sys.initializeGL = self.initializeGL
        self.gl_sys.paintGL = self.paintGL        

    def paintGL(self):
        self.loadScene()
        x_cam =  self.zoom * math.sin(self.Angle_y) * math.cos(self.Angle_x)
        y_cam =  self.zoom * math.sin(self.Angle_y) * math.sin(self.Angle_x)
        z_cam =  self.zoom * math.cos(self.Angle_y) 
        gluLookAt(x_cam, y_cam, z_cam, 0, 0, 0, 0, 1, 0)
        
        if self.timer.isActive():
            self.draw()
            self.calculate()
        
    def draw(self):
        global part_list
        global dt
        part_list = [p for p in part_list if int(p.alive) > 0]
        if self.count_combo.currentIndex() != 5: 
            for i in range(len(part_list)):
                if (abs(part_list[i].x) < 2500)&(abs(part_list[i].y) < 2500)&(abs(part_list[i].z) < 2500):
                    #glMaterialfv(GL_FRONT, GL_AMBIENT, [0.8, 0.8, 0.0])
                    #glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.2, 0.2])
                    #glMaterialfv(GL_FRONT, GL_SPECULAR, [0.6, 0.6, 0.6])
                    #glMaterialfv(GL_FRONT, GL_SHININESS, 0.5*128)
                    glPushMatrix()
                    sphere = gluNewQuadric()  
                    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, part_list[i].color)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, part_list[i].color)
                    glTranslatef(part_list[i].x, part_list[i].y, part_list[i].z)
                    gluQuadricDrawStyle(sphere, GLU_FILL)        
                    gluSphere(sphere, part_list[i].m / 100.0, 16, 16) 
                    glTranslatef(-part_list[i].x, -part_list[i].y, -part_list[i].z)
                    glPopMatrix()
                    gluDeleteQuadric(sphere)   
                else:
                    part_list[i].alive = 0
        else:
            for i in range(len(part_list)):
                if (abs(part_list[i].x) < 2500)&(abs(part_list[i].y) < 2500)&(abs(part_list[i].z) < 2500):
                    glPushMatrix()
                    sphere = gluNewQuadric()  
                    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, part_list[i].color)
                    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, part_list[i].color)
                    glTranslatef(50*part_list[i].x, 50*part_list[i].y, 50*part_list[i].z)
                    gluQuadricDrawStyle(sphere, GLU_FILL)        
                    if i==0:
                        gluSphere(sphere, part_list[i].m / 24000.0, 16, 16) 
                    elif i==1:
                        gluSphere(sphere, part_list[i].m*10, 16, 16) 
                    elif i==2:
                        gluSphere(sphere, part_list[i].m , 16, 16) 
                    elif i==3:
                        gluSphere(sphere, part_list[i].m , 16, 16) 
                    elif i==4:
                        gluSphere(sphere, part_list[i].m * 7, 16, 16) 
                    elif i==5:
                        gluSphere(sphere, part_list[i].m / 30.0, 16, 16) 
                    elif i==6:
                        gluSphere(sphere, part_list[i].m / 12.0, 16, 16) 
                    elif i==7:
                        gluSphere(sphere, part_list[i].m / 2.3, 16, 16) 
                    elif i==8:
                        gluSphere(sphere, part_list[i].m / 3.2, 16, 16) 
                    elif i==9:
                        gluSphere(sphere, part_list[i].m *200, 16, 16) 

                    glTranslatef(-50*part_list[i].x, -50*part_list[i].y, -50*part_list[i].z)
                    glPopMatrix()
                    gluDeleteQuadric(sphere)   
                else:
                    part_list[i].alive = 0
                    
        label = str(len(part_list))
        self.cur_count.setText(label)

    def initializeGL(self):
        glEnable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)        
        glEnable(GL_NORMALIZE) 
        glEnable(GL_COLOR_MATERIAL)
        global part_list
        part_list = []
        

    def loadScene(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        x, y, width, height = glGetDoublev(GL_VIEWPORT)
        gluPerspective(90, width / float(height or 1), .25, 5000)     
        #glOrtho(-2500., 2500., -2500., 2500., -2500., 2500.)

def main():
    app = QApplication(sys.argv)
    window = Interface()
    window.setupGL()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()