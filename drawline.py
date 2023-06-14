import trimesh
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

def draw_line(point1, point2):
    glBegin(GL_LINES)
    glVertex3fv(point1)
    glVertex3fv(point2)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    # Load 3D model
    mesh = trimesh.load("1.off")

    symmetrical_point_pairs = [([0.779628, -0.0415377, -0.0506292], [1.49867, 0.0542145, 0.0173255])]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_DEPTH_TEST)

        # Render 3D model
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3f(0.5, 0.5, 0.5)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, mesh.vertices)
        glNormalPointer(GL_FLOAT, 0, mesh.vertex_normals)
        glDrawElements(GL_TRIANGLES, len(mesh.faces) * 3, GL_UNSIGNED_INT, mesh.faces.ravel())
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        # Draw lines on the model
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(0.0, 1.0, 0.0)
        for point1, point2 in symmetrical_point_pairs:
            draw_line(point1, point2)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()


'''
import trimesh
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

def draw_line(point1, point2):
    glBegin(GL_LINES)
    glVertex3fv(point1)
    glVertex3fv(point2)
    glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)
    """

            VERTEX_INDEX: 5158
            x: 0.779628
            y: -0.0415377
            z: -0.0506292
         
            VERTEX_INDEX: 11573
            x: 1.49867
            y: 0.0542145
            z: 0.0173255
    """
    # Load 3D model
    mesh = trimesh.load_mesh("1.off")
    symmetrical_point_pairs = [([0.779628,-0.0415377,-0.0506292 ],[1.49867,0.0542145,0.0173255 ] )]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw lines on the model
        glColor3f(0.0, 1.0, 0.0)
        for point1, point2 in symmetrical_point_pairs:
            draw_line(point1, point2)

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()

'''