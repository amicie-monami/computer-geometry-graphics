import glfw
import numpy as np
from random import random as rand

import utils
from shader import Shader
from shapes.line import Line
from shapes.broken_line import BrokenLine
from shapes.point import Point
from shapes.polygon import Polygon

VERTICES_NUMBER = 8
SCALE_X = 0.8
SCALE_Y = 0.9
LINE_THICKNESS = 2
LINE_SMOOTH = True
POINT_SIZE = 10
POINT_SMOOTH = False

class Tasker:

    def __init__(self, window):
        self.objects = []
        self.window = window
        self.shader = Shader("shaders/vertex.glsl", "shaders/fragment.glsl")

    def actual_objects(self):
        """
        Return current scene objects for rendering
        """
        return self.objects

    def handle_input(self):
        """
        Proccesses keyboard input and
        switches between tasks 
        """
        if self.window.get_key(glfw.KEY_1) == glfw.PRESS:
            self.first_task()

        elif self.window.get_key(glfw.KEY_2) == glfw.PRESS:
            self.second_task()

        elif self.window.get_key(glfw.KEY_3) == glfw.PRESS:
            self.third_task()

        elif self.window.get_key(glfw.KEY_4) == glfw.PRESS:
            self.fourth_task()


    def first_task(self):
        """
        Construct points located on the vertices to obtain an n-gon
        Set smoothing mode for points
        """
        
        vertices = utils.calculate_polygon_vertices(VERTICES_NUMBER, SCALE_X, SCALE_Y)
        
        self.objects = []
        for x, y in vertices:
            position = np.array([x, y, 1.0], dtype=np.float32)
            color = np.array([rand() for _ in range(3)], dtype=np.float32)
            self.objects.append(Point(self.shader, position, color, POINT_SIZE, POINT_SMOOTH))
    

    def second_task(self):
        """
        Using the line output primitive, draw an n-gon
        Changing line thickness
        """
        
        vertices = utils.calculate_polygon_vertices(VERTICES_NUMBER, SCALE_X, SCALE_Y)

        vertices_coords = []
        vertices_colors = []

        for idx in range(len(vertices)):
            x1, y1 = vertices[idx]
            vertices_coords.append([x1, y1, 1.0])
            colors = [rand() for _ in range(3)]
            vertices_colors.append(colors)

        vertices_coords = np.array(vertices_coords, dtype=np.float32)
        vertices_colors = np.array(vertices_colors, dtype=np.float32)

        self.objects = [Polygon(self.shader, vertices_coords, vertices_colors, LINE_THICKNESS, LINE_SMOOTH)]
    
    def third_task(self):
        """
        Draw a broken line
        """

        vertices = [
            # x1    y1    z1    x2    y2    z2
            -0.9,  0.4,  1.0, -0.2,  0.8,  1.0,
            -0.2,  0.8,  1.0,  0.0,  0.0,  1.0,
             0.0,  0.0,  1.0, -0.5, -0.6,  1.0,
            -0.5, -0.6,  1.0,  0.4, -0.6,  1.0,
             0.4, -0.6,  1.0,  0.8,  0.0,  1.0,
        ]

        self.objects = []


        coords = np.array(vertices, dtype=np.float32)
        random_rgb = [rand() for _ in range(len(vertices))]
        colors = np.array(random_rgb, dtype=np.float32)
        
        self.objects.append(BrokenLine(self.shader, coords, colors, LINE_THICKNESS, LINE_SMOOTH))        
    
    def fourth_task(self):
        """
        Draw a closed broken line
        """

        vertices = [
            # x1    y1    z1    x2    y2    z2
             0.0,  1.0,  1.0, -0.7,  -0.1,  1.0,
            -0.7, -0.1,  1.0,  0.3,  -0.8,  1.0,
             0.3, -0.8,  1.0,  0.7,  -0.1,  1.0,
             0.7, -0.1,  1.0,  0.25,  0.2,  1.0,
             0.25,  0.2,  1.0, 0.5,   0.7,  1.0,
        ]

        self.objects = []

        coords = np.array(vertices, dtype=np.float32)
        random_rgb = [rand() for _ in range(len(vertices))]
        colors = np.array(random_rgb, dtype=np.float32)
        
        self.objects.append(Polygon(self.shader, coords, colors, LINE_THICKNESS, LINE_SMOOTH))        
    
