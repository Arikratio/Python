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

import test_interface

class Coordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, p):
        return Coordinate(self.x + p.x, self.y + p.y, self.z + p.z)
    
    def __sub__(self, p):
        return Coordinate(self.x - p.x, self.y - p.y, self.z - p.z)
    
    def __mul__(self, alpha):
        return Coordinate(self.x * alpha, self.y * alpha, self.z * alpha)

    def Module(self, coordinate):
        return math.sqrt((self.x - coordinate.x)**2 + (self.y - coordinate.y)**2 + (self.z - coordinate.z)**2)
        
class Velocity:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w
        
    def __add__(self, vel):
        return Velocity(self.u + vel.u, self.v + vel.v, self.w + vel.w)
    
    def __sub__(self, vel):
        return Velocity(self.u - vel.u, self.v - vel.v, self.w - vel.w)
    
    def __mul__(self, alpha):
        return Velocity(self.u * alpha, self.v * alpha, self.w * alpha)

    def __truediv__(self, alpha):
        return Velocity(self.u / alpha, self.v / alpha, self.w / alpha)
    
    
    
class Particle:
    def __init__(self, coordinate, velocity, m, color):
        self.x = coordinate.x
        self.y = coordinate.y
        self.z = coordinate.z
        self.u = velocity.u
        self.v = velocity.v
        self.w = velocity.w
        self.m = m
        self.color = color 
        self.coordinate = coordinate
        self.velocity = velocity
        self.alive = True


class InterfaceEditor(QMainWindow, test_interface.Ui_MainWindow, QOpenGLWidget):
   
    part_list = []
       
    def __init__(self):
        super().__init__()

        self.Angle_x = 0
        self.Angle_y = 0
        self.zoom = 1000
        self.lastPos = QPoint()
        self._color = QColor(255, 0, 0)
        self.dt = 1000
        self.setupUi(self) 
        self.timer = QTimer() 
        self.timer.timeout.connect(self.draw)
        self.timer.start(self.dt)
        self.color_button.clicked.connect(self.button_selectColor) 
        self.add_button.clicked.connect(self.button_add)
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
        x = float(self.c_x.toPlainText())
        y = float(self.c_y.toPlainText())
        z = float(self.c_z.toPlainText())
        emit = Coordinate(x, y, z)
        
        u = float(self.v_x.toPlainText()) 
        v = float(self.v_y.toPlainText())
        w = float(self.v_z.toPlainText())
        vel = Velocity(u, v, w)/100
        part_list.append(Particle(emit, vel, float(self.mass.toPlainText()), self._color.getRgbF()))     
        self.gl_sys.update()
        
    def combobox_numberChoice(self):
        global part_list        
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
        part_list = []     
        for i in range(1, part_count):
            part_list.append(Particle(Coordinate(random.randint(-500, 500), random.randint(-500, 500), random.randint(-500, 500)), Velocity(random.randint(-5, 5) / 1000.0, random.randint(-5, 5) / 1000.0, random.randint(-5, 5) / 1000.0), random.uniform(100, 1000), [random.uniform(0.3, 0.9), random.uniform(0.3, 0.9), random.uniform(0.3, 0.9)]))
        self.timer.start(self.dt)    
        self.gl_sys.update()
            
    def mousePressEvent(self, event):
        self.lastPos = event.pos()

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
            
    def calculateParticles(self):
        print("calculateParticles")
        G = 6.67408 * (10 ** -9)
        self.dt = 5000
        timerStep = self.dt
        global part_list
        
        x_n = []
        y_n = []
        z_n = []
        u_n = []
        v_n = []
        w_n = []
        m_n = []
        col_n = []        
        
        for partic in part_list:
            for par in part_list:
                if (partic.coordinate.Module(par.coordinate) > 0) & (partic.coordinate.Module(par.coordinate) < (partic.m + par.m) / 100.0):
                    if partic.m >= par.m:
                        partic.m += par.m
                    else:
                        partic.alive = False

                        
            if (partic.alive):
                x_n.append(partic.x)
                y_n.append(partic.y)
                z_n.append(partic.z)
                u_n.append(partic.u)
                v_n.append(partic.v)
                w_n.append(partic.w)
                m_n.append(partic.m)
                col_n.append(partic.color)
                
        length = len(x_n) 
                    
        ax_n = []
        ay_n = []
        az_n = []
        for px, py, pz in zip(x_n, y_n, z_n):            
            part = Coordinate(px, py, pz)
            ax = []
            ay = []
            az = []
            for p in part_list:
                module = part.Module(p.coordinate)**3
                if module > 0:
                    ax.append(G*p.m * (p.x - px) / module)
                    ay.append(G*p.m * (p.y - py) / module)
                    az.append(G*p.m * (p.z - pz) / module)

            ax_n.append(sum(ax))
            ay_n.append(sum(ay))
            az_n.append(sum(az))
            
        x_n1 = [x + u*timerStep + 0.5*a*timerStep**2 
                for x, u, a in zip(x_n, u_n, ax_n)]
        y_n1 = [y + v*timerStep + 0.5*a*timerStep**2 
                for y, v, a in zip(y_n, v_n, ay_n)]
        z_n1 = [z + w*timerStep + 0.5*a*timerStep**2 
                for z, w, a in zip(z_n, w_n, az_n)]
        
        ax_n1 = []
        ay_n1 = []
        az_n1 = []
        for px, py, pz in zip(x_n1, y_n1, z_n1):
            part = Coordinate(px, py, pz)
            ax = []
            ay = []
            az = []
            for x, y, z, m in zip(x_n1, y_n1, z_n1, m_n):
                p = Coordinate(x, y, z) 
                module = part.Module(p)**3
                if module > 0:
                    ax.append(G*m * (x - px) / module)
                    ay.append(G*m * (y - py) / module)
                    az.append(G*m * (z - pz) / module)
                    
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
        for i in range(length):
            coordinate = Coordinate(x_n1[i], y_n1[i], z_n1[i])
            velocity = Velocity(u_n1[i], v_n1[i], w_n1[i])
            part_list.append(Particle(coordinate, velocity, m_n[i], col_n[i]))
                    
        
        if (self.timer.isActive()):
            self.gl_sys.update()  
            
    def setupGL(self):
        print("setupGL")

        self.gl_sys.initializeGL()
        self.gl_sys.initializeGL = self.initializeGL
        self.gl_sys.paintGL = self.paintGL        

    def paintGL(self):
        print("paintGL")
        self.loadScene() 
        rad = self.zoom
        x_cam = rad * math.sin(self.Angle_y) * math.cos(self.Angle_x)
        y_cam = rad * math.sin(self.Angle_y) * math.sin(self.Angle_x)
        z_cam = rad * math.cos(self.Angle_y) 
        gluLookAt(x_cam, y_cam, z_cam, 0, 0, 0, 0, 1, 0)
        
        if self.timer.isActive():
            self.draw()
            self.calculateParticles()
        
    def draw(self):
        global part_list

        part_list = [p for p in part_list if p.alive == True]
        for i in range(len(part_list)):
            if ((part_list[i].x > -2000)&(part_list[i].x < 2000)
                &(part_list[i].y > -2000)&(part_list[i].y < 2000)
                &(part_list[i].z > -2000)&(part_list[i].z < 2000)):
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
                part_list[i].alive = False
                    
        label = str(len(part_list))
        self.cur_count.setText(label)

    def initializeGL(self):
        print("initializeGL")
        glEnable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)        
        glEnable(GL_NORMALIZE) 

        glLightfv(GL_LIGHT0, GL_POSITION, [100,100,100,1])
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0,1,1])
        glLighti(GL_LIGHT0, GL_SPOT_EXPONENT, 1)
        glLighti(GL_LIGHT0, GL_SPOT_CUTOFF, 45)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        global part_list
        part_list = []
        

    def loadScene(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        x, y, width, height = glGetDoublev(GL_VIEWPORT)
        gluPerspective(90, width / float(height or 1), .25, 2000)     

def main():
    app = QApplication(sys.argv)
    window = InterfaceEditor()
    window.setupGL()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()