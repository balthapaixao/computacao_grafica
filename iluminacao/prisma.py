from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import pprint as pp

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