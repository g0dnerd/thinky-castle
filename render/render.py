from game.map import Level
from typing import List, Tuple
import pygame
from OpenGL import GL
from OpenGL import GLU

from render.convert import prerender_level

colors = [
    (1, 0, 0),  # red
    (0, 1, 0),  # green
    (0, 0, 1),  # blue
    (0, 1, 0),  # green
    (1, 1, 1),  # white
    (0, 1, 1),  # cyan
    (1, 0, 0),  # red
    (0, 1, 0),  # green
    (0, 0, 1),  # blue
    (1, 0, 0),  # red
    (1, 1, 1),  # white
    (0, 1, 1),  # cyan
]


def rect(
    vertices: List[Tuple[int, int, int]],
    edges: List[Tuple[int, int]],
):
    GL.glBegin(GL.GL_LINES)
    for edge in edges:
        for vertex in edge:
            GL.glVertex3fv(vertices[vertex])
    GL.glEnd()


def game_loop(display_width: int, display_height: int, level: Level):
    vertices, edges = prerender_level(level)
    pygame.init()
    display = (display_width, display_height)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    # Define FoV (45), aspect ratio, znear (0.1), zfar (50.0)
    GLU.gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Move the camera back
    GL.glTranslatef(0.0, 0.0, -20)

    # Rotate the camera
    GL.glRotatef(45, 2, 1, 0)

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    quit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_LEFT:
                            GL.glTranslatef(-0.5, 0, 0)
                        case pygame.K_RIGHT:
                            GL.glTranslatef(0.5, 0, 0)
                        case pygame.K_UP:
                            GL.glTranslatef(0, 1, 0)
                        case pygame.K_DOWN:
                            GL.glTranslatef(0, -1, 0)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        rect(vertices, edges)

        pygame.display.flip()
        pygame.time.wait(10)
