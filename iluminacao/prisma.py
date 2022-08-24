from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import sys

class Prism:
    def __init__(self, polygon_sides, width = 1 ,height = 3):
        self.polygon_sides = polygon_sides
        self.height = height
        self.width = width
        self.vertex = self._get_vertex(polygon_sides)
        self.faces = self._get_faces(self.vertex)

    def _get_vertex(self, polygon_sides):
        vertex = []
        base = []
        top = []
        for i in range(polygon_sides):
            angle = (i/polygon_sides) * 2 * math.pi
            x = self.width * math.sin(angle)
            y = self.width * math.cos(angle)
            aux = self.height/2
            top.append((x,y,aux))
            base.append((x,y,-aux))

        vertex = [*top, *base]
        return vertex

    def _get_faces(self, vertex):
        faces = []
        middle = len(vertex)//2
        base = []
        top = []
        for i in range(middle):
            base.append(i)
            top.append(i + middle)
        
        faces = [tuple(base), tuple(top)]
        for i in range(0,middle - 1):
            faces.append((i, i + 1, middle + i + 1, middle + i))

        faces.append((i + 1, 0, middle, middle + i + 1))

        return faces

    def generate_new_vertex(self, polygon_sides, width = None, height = None):
        self.polygon_sides = polygon_sides
        self.height = self.height if height is None else height
        self.width = self.width if width is None else width
        self.vertex = self._get_vertex(polygon_sides)
        self.faces = self._get_faces(self.vertex)

    def get_normal(self, face_index):
        x = 0
        y = 1
        z = 2
        v0 = self.vertex[self.faces[face_index][0]]
        v1 = self.vertex[self.faces[face_index][1]]
        v2 = self.vertex[self.faces[face_index][2]]
        U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
        V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
        N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
        NLength = math.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
        return (N[x]/NLength, N[y]/NLength, N[z]/NLength)

    def draw(self):
        for index, face in enumerate(self.faces[:2:]):
            glNormal3fv(self.get_normal(index))
            glBegin(GL_POLYGON)

            for index in face:
                glVertex3fv(self.vertex[index])
            glEnd()
    
        for index, face in enumerate(self.faces[2::]):
            glNormal3fv(self.get_normal(index))
            glBegin(GL_QUADS)
            for jindex in face:
                glVertex3fv(self.vertex[jindex])
            glEnd()

total_sides = 8
max_sides = 15
min_sides = 3

angle = 0

prism = Prism(total_sides,width = .5 ,height = 2)

def draw():
	global angle

	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	
	glPushMatrix()
	glRotatef(angle,3,5,5)
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
	mat_ambient = (0.7, 0.0, 0.2, 1.0)
	mat_diffuse = (1.0, 0.0, 0.2, 1.0)
	mat_specular = (1.0, 0.0, 0.2, 1.0)
	mat_shininess = (50,)
	light_position = (20, 80, -5)
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