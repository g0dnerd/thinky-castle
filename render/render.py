from game.level import Level
from typing import List, Tuple
import pygame
from OpenGL import GL
from OpenGL import GLU

from render.mesh import make_level_mesh


def render_level(
    vertices: List[Tuple[int, int, int]],
    edges: List[Tuple[int, int]],
    colors: List[Tuple[int, int, int]],
):
    GL.glBegin(GL.GL_LINES)
    for i, edge in enumerate(edges):
        GL.glColor3fv(colors[i])
        for vertex in edge:
            GL.glVertex3fv(vertices[vertex])
    GL.glEnd()


def game_loop(display_width: int, display_height: int, lvl: Level):
    pygame.init()
    display = (display_width, display_height)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    # Define FoV (45), aspect ratio, znear (0.1), zfar (50.0)
    GLU.gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Move the camera back
    GL.glTranslatef(0.0, 0.0, -20)

    # Set initial rotation angles
    rot_angle = 45
    rot_x, rot_y = 2, 1
    GL.glRotatef(rot_angle, rot_x, rot_y, 0)

    # Cache the level's vertices, edges and colors
    vertices, edges, colors = make_level_mesh(lvl)

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    return
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

        render_level(vertices, edges, colors)

        pygame.display.flip()
        pygame.time.wait(10)
