import glfw
import numpy as np
from OpenGL.GL import *
from random import random as rand

import utils
from shader import Shader
from shapes.figure import Figure


VERTICES_NUMBER = 8
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
        self.last_task = None
        self.paragraph = glfw.KEY_A
        self.shader = Shader("shaders/vertex.glsl", "shaders/fragment.glsl")

        glfw.set_key_callback(window.window, self.handle_input)

        self.tasks_keys = [
            glfw.KEY_1, glfw.KEY_2, glfw.KEY_3, glfw.KEY_4, glfw.KEY_5
        ]

        tasks_handlers = [
            self.first_task,self.second_task,self.third_task,self.fourth_task, self.five_task
        ]
        
        self.tasks = {key: task for key, task in zip(self.tasks_keys, tasks_handlers)}


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

        keys = [glfw.KEY_A, glfw.KEY_B, glfw.KEY_C]
        for key in keys:
            if (self.window.get_key(key) == glfw.PRESS) and (self.last_task in [self.five_task]):
                self.paragraph = key
                self.last_task()

    def first_task(self):
        """
        Construct points located on the vertices to obtain an n-gon
        Set smoothing mode for points
        """
        vertices_coords = utils.calculate_polygon_vertices(VERTICES_NUMBER, SCALE_X, SCALE_Y)        
        vertices = utils.prepare_vertices(vertices_coords)
        
        self.objects = [Figure(self.shader, vertices, GL_POINTS, POINT_SIZE, POINT_SMOOTH)]
        self.last_task = self.first_task
    
    def second_task(self):
        """
        Using the line output primitive, draw an n-gon
        Changing line thickness
        """
        vertices_coords = utils.calculate_polygon_vertices(VERTICES_NUMBER, SCALE_X, SCALE_Y)
        vertices = utils.prepare_vertices(vertices_coords)

        self.objects = [Figure(self.shader, vertices, GL_LINE_LOOP, LINE_THICKNESS, LINE_SMOOTH)]
        self.last_task = self.second_task

    def third_task(self):
        """
        Draw a broken line
        """
        a = [-0.9,  0.4,  1.0]
        b = [-0.2,  0.8,  1.0]
        c = [ 0.0,  0.0,  1.0]
        d = [-0.5, -0.6,  1.0]
        e = [ 0.4, -0.6,  1.0]
        f = [ 0.8,  0.0,  1.0]
        
        vertices_coords = [a,b,  b,c,  c,d,  d,e,  e,f]
        vertices = utils.prepare_vertices(vertices_coords)

        self.objects = [Figure(self.shader, vertices, GL_LINE_STRIP, LINE_THICKNESS, LINE_SMOOTH)]
        self.last_task = self.third_task
    

    def fourth_task(self):
        """
        Draw a closed broken line
        """
        a = [ 0.0,  0.9, 1.0]
        b = [-0.8,  0.1, 1.0]
        c = [ 0.4, -0.5, 1.0]
        d = [ 0.8, -0.1, 1.0]
        e = [ 0.2,  0.2, 1.0]
        f = [ 0.6,  0.6, 1.0]

        vertices_coords = [a,b,  b,c,  c,d,  d,e,  e,f,  f,a]
        vertices = utils.prepare_vertices(vertices_coords)

        self.objects = [Figure(self.shader, vertices, GL_LINE_LOOP, LINE_THICKNESS, LINE_SMOOTH)]
        self.last_task = self.fourth_task
    

    def five_task(self):
        """
        Draw a polygon using a primitives: 
        a) triangles 
        b) triangle strip 
        c) triangle fans  
        """
        a = [ 0.0,  0.9, 1.0] 
        b = [-0.8,  0.1, 1.0]
        c = [ 0.4, -0.5, 1.0] 
        d = [ 0.8, -0.1, 1.0]
        e = [ 0.2,  0.2, 1.0] 
        f = [ 0.6,  0.6, 1.0]

        match self.paragraph:
            case glfw.KEY_A:
                draw_mode = GL_TRIANGLES
                vertices_coords = [a,b,c,  c,d,e,  e,f,a]  

            case glfw.KEY_B:
                draw_mode = GL_TRIANGLE_STRIP
                vertices_coords = [f, a, e, b, c, e, d]

            case glfw.KEY_C:
                draw_mode = GL_TRIANGLE_FAN
                vertices_coords = [b, a, f, e, d, c]

        shader = Shader("shaders/flat_vertex.glsl", "shaders/flat_fragment.glsl")
        vertices = utils.prepare_vertices(vertices_coords)
        
        self.objects = [Figure(shader, np.array(vertices, dtype=np.float32), draw_mode)]
        self.last_task = self.five_task

