from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import png

class Texture:

    def __init__(self, texture_files, window_title, width, height):

        self.width = width
        self.height = height
        self.window_title = window_title
        self.textures_files = texture_files
        self.textures = {}

    def __LoadTextures(self):
    
        for texture in self.textures_files.keys():

            self.textures[texture] = glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, self.textures[texture])
            reader = png.Reader(filename=self.textures_files[texture])
            w, h, pixels, metadata = reader.read_flat()
            if(metadata['alpha']):
                modo = GL_RGBA
            else:
                modo = GL_RGB
            glPixelStorei(GL_UNPACK_ALIGNMENT,1)

            glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
            
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

            #   ou

            #    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            #    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


    def __InitGL(self, Width, Height):             
        self.__LoadTextures()
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.0, 0.0, 0.0, 0.0) 
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)               
        glEnable(GL_DEPTH_TEST)            
        glShadeModel(GL_SMOOTH)            
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def __ReSizeGLScene(self, Width, Height):
        if Height == 0:                        
            Height = 1
        glViewport(0, 0, Width, Height)      
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def __timer(self,i):
        glutPostRedisplay()
        glutTimerFunc(50,self.__timer,1)

    def main(self, draw, keyPressed = None, specialKeyPressed = None):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)    
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(self.window_title)
        glutDisplayFunc(draw)
        glutIdleFunc(draw)
        glutReshapeFunc(self.__ReSizeGLScene)
        if keyPressed is not None:
            glutKeyboardFunc(keyPressed)
        if specialKeyPressed is not None:
            glutSpecialFunc(specialKeyPressed)
        self.__InitGL(640, 480)
        glutTimerFunc(50,self.__timer,1)
        glutMainLoop()