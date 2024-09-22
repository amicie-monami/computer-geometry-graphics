import glfw
import numpy as np
import glm
from OpenGL.GL import *
from random import random as rand

import utils
from shader import Shader
from shapes.figure import Figure


SCALE_X = 0.70
SCALE_Y = 0.95

POINT_SIZE = 10
POINT_SMOOTH = GL_POINT_SMOOTH # || None
LINE_THICKNESS = 2
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

        self.tasks_keys = [glfw.KEY_1]
        tasks_handlers  = [self.first_task]
        
        self.tasks = {key: task for key, task in zip(self.tasks_keys, tasks_handlers)}
        glfw.set_key_callback(window.window, self.handle_input)


    def actual_objects(self):
        """
        Return current scene 
        objects for rendering
        """
        return self.objects


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

        
        keys = [glfw.KEY_DOWN, glfw.KEY_DOWN, glfw.KEY_UP]
        for idx in range(len(keys)):
            if self.window.get_key(keys[idx]) == glfw.PRESS:
                magnifier = (-1 + idx)
                self.vertices_number += magnifier
                
                if self.vertices_number < 0:
                    self.vertices_number = 0

                self.last_task()
                break


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


