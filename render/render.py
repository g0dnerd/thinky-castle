from typing import List, Tuple

import pygame
from OpenGL import GL, GLU

from game.level import Level
from render.mesh import make_level_mesh


def render_level(
    vertices: List[Tuple[int, int, int]],
    edges: List[Tuple[int, int]],
    colors: List[Tuple[int, int, int]],
):
    """Draws meshes in the specified colors.
    :param vertices (list): List of vertices in (x, y, z) format
    :param edges (list): List of edges defined as tuples (a, b) indexing into the list of vertices.
    :param colors (list): List of colors defined as tuples (r, g, b). colors[i] gets drawn to edges[i].
    """
    GL.glBegin(GL.GL_LINES)
    for i, edge in enumerate(edges):
        GL.glColor3fv(colors[i])
        for vertex in edge:
            GL.glVertex3fv(vertices[vertex])
    GL.glEnd()


def game_loop(display_width: int, display_height: int, lvl: Level):
    """Continuously caches level meshes and dispatches render calls.
    Handles camera transformations via arrow keys.
    """
    pygame.init()
    display = (display_width, display_height)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

    # Define FoV (45), aspect ratio, znear (0.1), zfar (50.0)
    GLU.gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Move the camera back
    GL.glTranslatef(0.0, 0.0, -20)

    # Set rotation angles
    rot_angle = 45
    rot_x, rot_y = 2, 1
    GL.glRotatef(rot_angle, rot_x, rot_y, 0)

    # Compute the level's vertices, edges and colors
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
                            GL.glTranslatef(-0.5, 0, 0)  # move left
                        case pygame.K_RIGHT:
                            GL.glTranslatef(0.5, 0, 0)  # move right
                        case pygame.K_UP:
                            GL.glTranslatef(0, 0.5, 0)  # move up
                        case pygame.K_DOWN:
                            GL.glTranslatef(0, -0.5, 0)  # move down

        # Clear the screen
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # Render meshes
        render_level(vertices, edges, colors)

        pygame.display.flip()
        pygame.time.wait(10)
