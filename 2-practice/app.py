from OpenGL.GL import * 
import window
import numpy
from shapes.shader import Shader 
from shapes.point import Point 
import utils


class App:

    def __init__(self):
        self.window = window.Window() 
        self.objects = []
        self.main_loop()
        return
        
    def main_loop(self):
        shader = Shader("shaders/vertex.glsl", "shaders/fragment.glsl")

        n = 6
        vertices = utils.calculate_polygon_vertices(n, scale_x=0.5, scale_y=0.5)
        for idx, (x, y) in enumerate(vertices):
            self.objects.append(Point(shader, numpy.array([x, y, 1.0], dtype=numpy.float32), numpy.array([0.5, 0.5, 1.0], dtype=numpy.float32), 5))
        
        while not self.window.should_close():
            self.window.clear()
            self.window.poll_events()

            for obj in self.objects:
                obj.draw()

            self.window.swap_buffers()
        return
    
    def draw_menu():
        pass


App()
