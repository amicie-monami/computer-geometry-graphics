import glfw
import numpy as np
from random import random as rand

import utils
from window import Window
from shader import Shader
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
        
    def first_task(self):
        """
        Construct points located on the vertices to obtain an n-gon
        Set smoothing mode for points
        """
        
        vertices = utils.calculate_polygon_vertices(VERTICES_NUMBER, SCALE_X, SCALE_Y)
        shader = Shader("shaders/vertex.glsl", "shaders/fragment.glsl")
        
        self.objects = []
        for x, y in vertices:
            position = np.array([x, y, 1.0], dtype=np.float32)
            color = np.array([rand() for _ in range(3)], dtype=np.float32)
            self.objects.append(Point(shader, position, color, POINT_SIZE, POINT_SMOOTH))
    

    def second_task(self):
        """
        Using the line output primitive, draw an n-gon
        Changing line thickness
        """
        
        shader = Shader("shaders/vertex.glsl", "shaders/fragment.glsl")
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

        self.objects = [Polygon(shader, vertices_coords, vertices_colors, LINE_THICKNESS, LINE_SMOOTH)]

    