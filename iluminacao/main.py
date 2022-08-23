from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
from prisma import *
import sys

total_sides = 5
max_sides = 15
min_sides = 3

angle = 0

prism = Prism(total_sides)

def draw():
	global angle

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	
	glPushMatrix()
	glRotatef(angle,3,3,5)
	prism.draw()
	glPopMatrix()
	
	angle += 1

	glutSwapBuffers()

def mouse_click_effects(button, state, x, y):
	global height, total_sides

	if button == 0 and state == 0 and total_sides < max_sides:
		total_sides += 1
	elif button == 2 and state == 0 and total_sides > min_sides:
		total_sides -= 1
	prism.generate_new_vertex(total_sides)

def timer(i):
	glutPostRedisplay()
	glutTimerFunc(50,timer,1)

def reshape(w,h):
	glViewport(0,0,w,h)
	glMatrixMode(GL_PROJECTION)
	gluPerspective(45,float(w)/float(h),0.1,50.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	where = (10,0,0)
	to = (0,0,0)
	direction = (0,1,0)
	# Camera Virtual
	#		  onde	Pra onde 
	gluLookAt( *where, *to,	 *direction )

def init():
	mat_ambient = (0.0, 0.7, 0.0, 1.0)
	mat_diffuse = (0.0, 1.0, 0.0, 1.0)
	mat_specular = (0.0, 1.0, 0.0, 1.0)
	mat_shininess = (50,)
	light_position = (10, 50, -10)
	glClearColor(0.0,0.0,0.0,0.0)
	glShadeModel(GL_FLAT)
	# glShadeModel(GL_SMOOTH)

	glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
	glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
	glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
	glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, light_position)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_MULTISAMPLE)

def config():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
	glutInitWindowSize(800,600)
	glutCreateWindow("Prisma iluminado")
	glutMouseFunc(mouse_click_effects)
	glutReshapeFunc(reshape)
	glutDisplayFunc(draw)
	glutTimerFunc(50,timer,1)
	init()
	glutMainLoop()

if __name__ == '__main__':
	config()