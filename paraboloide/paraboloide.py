from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

x0 = -1
xn = 1

y0 = -1
yn = 1

n = 50
dx = (xn - x0)/n
dy = (yn - y0)/n

def f(x,y):
    z=(x**2)+(y**2)
    return z

def desenhaSuperficie():
    y = y0
    for _ in range(n):
        x = x0
        
        glBegin(GL_TRIANGLE_STRIP)
        
        for __ in range(n): 

            glColor3fv([.1,.9,.3])

            glVertex3f(x, y, f(x, y))
            glVertex3f(x, y + dy, f(x, y + dy))
            
            x += dx
        
        glEnd()
        
        y += dy


a = 0
def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    glTranslate(0, 0, 0)
    glRotatef(-a,1,0,0)
    desenhaSuperficie()
    
    glPopMatrix()
    glPushMatrix()
    
    glPopMatrix()
    glutSwapBuffers()
    a += 1
 
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(30,timer,1)

# PROGRAMA PRINCIPAL
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800,600)
glutCreateWindow("Superficie")
glutDisplayFunc(desenha)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0.,0.,0.,1.)
gluPerspective(45,800.0/600.0,0.1,100.0)
glTranslatef(0.0,0.0,-10)
glutTimerFunc(50,timer,1)
glutMainLoop()