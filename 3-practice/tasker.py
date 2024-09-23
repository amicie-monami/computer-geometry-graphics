import glfw
import numpy as np
import glm
from OpenGL.GL import *
from random import random as rand

import utils
from shader import Shader
from shapes.figure import Figure

from window import SCREEN_WIDTH, SCREEN_HEIGHT

SCALE_X = SCREEN_HEIGHT / SCREEN_WIDTH
SCALE_Y = 1.0

POINT_SIZE = 10
POINT_SMOOTH = GL_POINT_SMOOTH # || None

LINE_THICKNESS = 3
LINE_SMOOTH = GL_LINE_SMOOTH # || None


class Tasker:

    def __init__(self, window):
        self.objects = []
        self.window = window
        
        self.last_task = self.first_task
        self.paragraph = glfw.KEY_A

        self.vertices_number = 5
        
        self.shader = Shader("shaders/vertex.glsl", "shaders/fragment.glsl")
        self.flat_shader = Shader("shaders/flat_vertex.glsl", "shaders/flat_fragment.glsl")
        self.transform_shader = Shader("shaders/transf_vertex.glsl", "shaders/fragment.glsl")

        self.tasks_keys = [glfw.KEY_1, glfw.KEY_2, glfw.KEY_3]
        tasks_handlers  = [self.first_task, self.second_task, self.third_task]
        
        self.tasks = {key: task for key, task in zip(self.tasks_keys, tasks_handlers)}
        glfw.set_key_callback(window.window, self.handle_input)


    def render_objects(self):
        """
        Returning current scene 
        objects for rendering
        """

        if self.last_task == self.third_task:
            line = self.objects[0]
            line.transform_reset()

            line.transform(glm.scale(glm.vec3(SCALE_X, SCALE_Y, 1.0)))
            
            #start (vertical line)
            #left bottom 
            line.transform(glm.translate(glm.vec3(-0.2, 0.3, 0.0)))
            line.draw()

            #right 
            line.transform(glm.translate(glm.vec3(0.4, 0.0, 0.0)))
            line.draw()

            #down
            line.transform(glm.translate(glm.vec3(0.0, -0.8, 0.0)))
            line.draw()

            # left
            line.transform(glm.translate(glm.vec3(-0.4, 0.0, 0.0)))
            line.draw()

            #up left
            line.transform(glm.translate(glm.vec3(-0.4, 0.4, 0.0)))
            line.draw()

            #right
            line.transform(glm.translate(glm.vec3(1.2, 0.0, 0.0)))
            line.draw()

            #start (horizontal line)
            #right bottom
            line.transform(glm.rotate(glm.radians(90), glm.vec3(0.0, 0.0, 1.0)))
            line.draw()

            #up
            line.transform(glm.translate(glm.vec3(0.4, 0.0, 0.0)))
            line.draw()

            #left bottom
            line.transform(glm.translate(glm.vec3(0.4, 0.4, 0.0)))
            line.draw()

            #down
            line.transform(glm.translate(glm.vec3(-1.2, 0.0, 0.0)))
            line.draw()

            #up left 
            line.transform(glm.translate(glm.vec3(0.8, 0.4, 0.0)))
            line.draw()

            #down
            line.transform(glm.translate(glm.vec3(-0.4, 0.0, 0.0)))
            line.draw()

        else:
            for object in self.objects:
                object.draw()


    def handle_input(self, window, key, scancode, action, mods):
        """
        Proccesses keyboard input and
        switches between tasks 
        """

        for key in self.tasks_keys:
            if self.window.get_key(key) == glfw.PRESS:
                self.tasks[key]()

        keys = [glfw.KEY_A, glfw.KEY_B, glfw.KEY_C, glfw.KEY_D]
        for key in keys:
            if (self.window.get_key(key) == glfw.PRESS) and (self.last_task in [self.first_task]):
                self.paragraph = key
                self.last_task()

        if self.window.get_key(glfw.KEY_UP) == glfw.PRESS:
            if self.last_task == self.first_task:
                self.vertices_number += 1
                self.last_task()
                return

            elif self.last_task == self.second_task:
                alpha = 20
                betta = -15
                kx, ky = 2, 1.5
                p = (0.2, 0.5)
                x, y = 3, 3

                self.objects[0].transform(glm.translate(glm.vec3(p, 0)) @ glm.scale(glm.vec3(kx, ky, 0)))
                self.objects[1].transform(glm.rotate(glm.radians(alpha), glm.vec3(0, 0, 1)))
                self.objects[2].transform(glm.rotate(glm.radians(betta), glm.vec3(x, y, 0)))


        elif self.window.get_key(glfw.KEY_DOWN) == glfw.PRESS:
            if self.last_task == self.first_task:
                self.vertices_number -= 1
                if self.vertices_number < 2:
                    self.vertices_number = 2
                self.last_task()
                return

            elif self.last_task == self.second_task:
                for obj in self.objects:
                    obj.transform_reset()


    def first_task(self):
        """
        Construct a regular n-gon using elements buffer
        a) all non-intersecting triangles
        b) all intersecting lines
        c) n-polygon contour
        d) line connecting all even vertices
        """
        vertices_coords = utils.calculate_polygon_vertices(self.vertices_number, SCALE_X, SCALE_Y)        
        vertices = utils.prepare_vertices(vertices_coords)

        vertices_number = len(vertices) // 6

        match self.paragraph:
            case glfw.KEY_A:
                """
                tetragon
                0 1 2
                0 2 3

                pentagon
                0 1 2
                0 2 3
                0 3 4

                [0, x+1, x+2], where x = [0..N-2]
                """
                traversal_order = [(0, x+1, x+2) for x in range(vertices_number - 2)]
                indices = np.array(traversal_order, dtype=np.uint32).flatten()
                self.objects = [Figure(GL_TRIANGLES, self.flat_shader, vertices, indices)]
            
            case glfw.KEY_B:
                """
                tetragon
                (x, (x+2)%4)
                0 2
                1 3

                pentagon
                [x, (x+2)%5]
                [x, (x+3)%5]
                0 2     1 3     2 4   
                0 3     1 4     2 0

                hexagon
                [x, (x+2)%6], 
                [x, (x+3)%6], 
                [x, (x+4)%6]
                0 2     1 3     2 4     3 1  
                0 3     1 4     2 5     3 0
                0 4     1 5     2 0     3 5

                [x, (x+num) % N], where num = [2..N-2]
                """
                traversal_order = [(x, (x+2+num)%vertices_number) for x in range(vertices_number) for num in range(vertices_number-3)]
                indices = np.array(traversal_order, dtype=np.uint32).flatten()
                self.objects = [Figure(GL_LINES, self.flat_shader, vertices, indices)]

            case glfw.KEY_C:
                """
                [x, (x+1) % N]
                """
                traversal_order = [(x, (x+1)%vertices_number) for x in range(vertices_number)]
                indices = np.array(traversal_order, dtype=np.uint32).flatten()
                self.objects = [Figure(GL_LINES, self.flat_shader, vertices, indices)]

            case glfw.KEY_D:
                #FIX COLORS
                """ 
                hexagon 
                0 2

                pentagon
                0 2
                0 4
                2 4

                """
                traversal_order = []
                for idx in range(0, vertices_number-1, 2):
                    for idx2 in range(2, vertices_number, 2):
                        if idx != idx2:
                            pair = (min(idx, idx2), max(idx, idx2))
                            if pair not in traversal_order:
                                traversal_order.append(pair)

                indices = np.array(traversal_order, dtype=np.uint32).flatten()
                self.objects = [Figure(GL_LINES, self.shader, vertices, indices)]

        self.last_task = self.first_task


    def second_task(self):
        triangle_verticles = [
            -0.5, -0.2, 0.0, 1.0, 0.0, 0.0,
            -0.4,  0.2, 0.0, 0.0, 1.0, 0.0,
            -0.3, -0.2, 0.0, 0.0, 0.0, 1.0,  
        ]
        vertices = np.array(triangle_verticles, dtype=np.float32)
        triangle = Figure(GL_TRIANGLES, self.transform_shader, vertices) 

        line_vertices = [
            -0.1, -0.4, 0.0, 1.0, 0.0, 0.0,
             0.5, -0.4, 0.0, 0.0, 1.0, 1.0
        ]

        vertices  = np.array(line_vertices, dtype=np.float32)
        line = Figure(GL_LINES, self.transform_shader, vertices)

        rectangle_verticles = [
            0.1, 0.5, 0.0, 1.0, 0.0, 0.0,
            0.1, 0.2, 0.0, 0.0, 1.0, 0.0,
            0.5, 0.5, 0.0, 0.0, 0.0, 1.0,
            0.5, 0.2, 0.0, 1.0, 1.0, 1.0,
        ]

        vertices  = np.array(rectangle_verticles, dtype=np.float32)
        indices   = np.array([0,1,2,1,2,3], dtype=np.uint32)
        rectangle = Figure(GL_TRIANGLES, self.transform_shader, vertices, indices)

        self.objects=[triangle, line, rectangle]

        for object in self.objects:
            object.transform(glm.scale(glm.vec3(SCALE_X, SCALE_Y, 1.0)))

        self.last_task = self.second_task

    def third_task(self):
        vertices_with_colors = np.array([
            0.0, 0.0, 0.0, rand(), rand(), rand(),
            0.0, 0.4, 0.0, rand(), rand(), rand(),
        ], dtype=np.float32)
        
        line = Figure(GL_LINES, self.transform_shader, vertices_with_colors, size=LINE_THICKNESS)

        self.objects = [line]
        self.last_task = self.third_task